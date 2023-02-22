from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.utils import datetime_to_epoch
from rest_framework.permissions import IsAuthenticated
import requests
from users.models import User


class GithubAuth(APIView):
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
            try:
                user = User.objects.get(email=user_emails[0]["email"])

            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    email=user_emails[0]["email"],
                    avatar=user_data.get("avatar_url"),
                )
                user.set_unusable_password()
                user.save()
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        expires = datetime_to_epoch(token.current_time + token.lifetime)

        res = Response(
            status=status.HTTP_200_OK,
            data={"access": access_token, "exp": expires},
        )
        res.set_cookie("refresh", refresh_token, httponly=True)
        return res


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        res = Response(status=status.HTTP_200_OK)
        res.delete_cookie("refresh")
        return res
