from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class AllMessages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """get all messages"""
        pass

    def delete(self, request):
        """delete all messages"""
        pass


class AMessage(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """delete a message"""
        pass
