import requests
from hashlib import sha256
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from inbox.models import Message
from .serializers import (
    ExposeWalletSerializer,
    SimplePasswordSerializer,
    GetPrivateKeySerializer,
)


class MyWallet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ok if private key sent is valid"""
        wallet = request.user.wallet
        private_key = request.data.get("private_key")
        if type(private_key) is not str:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if wallet.validate_private_key(private_key.encode()):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request):
        """replace whole wallet"""
        wallet = ExposeWalletSerializer(data=request.data)
        if wallet.is_valid():
            wallet = wallet.data
            res = requests.post(
                f"{settings.MEMPOOL_URL}/wallets/verify",
                json={
                    "privateKey": wallet.get("private_key"),
                    "publicKey": wallet.get("public_key"),
                },
            )
            if res.status_code != status.HTTP_200_OK:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            instance = request.user.wallet
            instance.public_key = wallet.get("public_key")
            instance.private_key_hash = sha256(
                wallet.get("private_key").encode()
            ).digest()
            instance.encrypted_private_key = None
            instance.save()

            Message.make_simple_pwd_message_again(request.user)

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SimplePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """create smiple password"""
        serializer = SimplePasswordSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            wallet = request.user.wallet
            try:
                wallet.create_simple_password(
                    data.get("simple_password"), data.get("private_key")
                )
                return Response(status=status.HTTP_201_CREATED)
            except Exception:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """get private key from simple password"""
        serializer = GetPrivateKeySerializer(data=request.data)
        if serializer.is_valid():
            wallet = request.user.wallet
            private_key = wallet.get_private_key(serializer.data["simple_password"])
            if wallet.validate_private_key(private_key):
                return Response(
                    status=status.HTTP_200_OK,
                    data={"private_key": private_key.decode()},
                )
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
