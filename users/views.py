from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from . import serializers


class SearchUsers(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """see list of users"""
        query = request.GET.get("q")
        users = User.objects.filter(
            Q(username__icontains=query) | Q(wallet__public_key__icontains=query)
        )
        if len(users) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ListUserSerializer(users, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class TinyMe(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """see my info on common"""
        serializer = serializers.CommonUserSerializer(request.user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """see my info"""
        serializer = serializers.PrivateUserSerializer(request.user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request):
        """change my info"""
        serializer = serializers.UpdateUserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(
                    status=status.HTTP_200_OK,
                    data=serializers.PrivateUserSerializer(user).data,
                )
            except Exception:
                return Response(
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class PublicUser(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        """get information about user"""
        try:
            user = User.objects.get(pk=pk)
            serializer = serializers.PublicUserSerializer(user)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
