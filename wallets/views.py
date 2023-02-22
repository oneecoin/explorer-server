from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class MyWallet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ok if private key sent is valid"""

    def put(self, request):
        """replace whole wallet"""
        pass


class SimplePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """create smiple password"""
        pass

    def put(self, request):
        """get private key from simple password"""
        pass
