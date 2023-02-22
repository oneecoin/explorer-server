import requests
from hashlib import sha256
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from inbox.models import Message
from .serializers import ExposeWalletSerializer


class MyWallet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ok if private key sent is valid"""
        wallet = request.user.wallet
        private_key = request.data.get("private_key")
        if wallet.validate_private_key(private_key.decode()):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request):
        """replace whole wallet"""
        wallet = ExposeWalletSerializer(data=request.data).data
        res = requests.post(
            f"{settings.MEMPOOL_URL}/wallets/verify",
            data={
                "privateKey": wallet["private_key"],
                "publicKey": wallet["public_key"],
            },
        )
        if res.status_code != status.HTTP_200_OK:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request.user.wallet.update(
            public_key=wallet["public_key"],
            private_key_hash=sha256(wallet["private_key"].encode()).digest(),
            encrypted_private_key=None,
        )
        Message.make_simple_pwd_message_again(request.user)

        return Response(status=status.HTTP_200_OK)


class SimplePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """create smiple password"""
        pass

    def put(self, request):
        """get private key from simple password"""
        pass
