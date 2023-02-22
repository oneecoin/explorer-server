from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import ListUserSerializer


class SearchUsers(APIView):
    def get(self, request):
        """see list of users"""
        query = request.GET.get("q")
        users = User.objects.filter(
            Q(username__icontains=query) | Q(wallet__public_key__icontains=query)
        )
        serializer = ListUserSerializer(users, many=True)
        return serializer.data


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """see my info"""
        pass

    def put(self, request):
        """change my info"""
        pass


class PublicUser(APIView):
    def get(self, request):
        """get information about user"""
        pass
