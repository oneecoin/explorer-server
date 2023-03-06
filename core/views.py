from hashlib import sha256
from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
import requests
from wallets.models import Wallet
from users.models import User
from inbox.models import Message
from .cron import create_transaction_model, delete_outdated_transaction


class GithubAuth(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """github login / signup"""
        try:
            # get access token
            code = request.data.get("code")
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id={settings.GH_CLIENT_ID}&client_secret={settings.GH_SECRET}",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            }

            # get user data
            user_data = requests.get(
                "https://api.github.com/user", headers=headers
            ).json()
            user_emails = requests.get(
                "https://api.github.com/user/emails", headers=headers
            ).json()

            res = Response()

            try:
                user = User.objects.get(email=user_emails[0]["email"])
                res.status_code = status.HTTP_200_OK
                res.data = {}
            except User.DoesNotExist:
                with transaction.atomic():
                    data = requests.post(f"{settings.MEMPOOL_URL}/wallets").json()
                    public_key = data.get("publicKey")
                    private_key = data.get("privateKey")
                    wallet = Wallet.objects.create(
                        public_key=public_key,
                        private_key_hash=sha256(private_key.encode()).digest(),
                    )
                    user = User.objects.create(
                        username=user_data.get("login"),
                        email=user_emails[0]["email"],
                        avatar=user_data.get("avatar_url"),
                        wallet=wallet,
                    )
                    user.set_unusable_password()

                    user.save()
                    Message.make_wallet_message(user)
                    Message.make_simple_pwd_message(user)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        res.data = dict(res.data, **{"auth": {"access": access_token}})
        res.set_cookie("refresh", refresh_token, httponly=True)
        return res


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        res = Response(status=status.HTTP_200_OK)
        res.delete_cookie("refresh")
        return res


class Refresh(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.COOKIES.get("refresh")
        try:
            token = RefreshToken(token=token, verify=True)
            data = TokenRefreshSerializer(token).data
            return Response(
                status=status.HTTP_200_OK,
                data=data,
            )
        except TokenError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
@permission_classes([AllowAny])
def do_cronjob(request):
    if request.GET.get("secretKey") != settings.SECRET_KEY:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    create_transaction_model()
    delete_outdated_transaction()
    return Response(status=status.HTTP_200_OK)
