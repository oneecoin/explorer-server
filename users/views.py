from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User
from . import serializers


class SearchUsers(APIView):
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
        pass


class PublicUser(APIView):
    def get(self, request, pk):
        """get information about user"""
        try:
            user = User.objects.get(pk=pk)
            serializer = serializers.PublicUserSerializer(user)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
