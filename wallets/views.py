from rest_framework.views import APIView


class MyWallet(APIView):
    def post(self, request):
        """ok if private key sent is valid"""

    def put(self, request):
        """replace whole wallet"""
        pass


class SimplePassword(APIView):
    def post(self, request):
        """create smiple password"""
        pass

    def put(self, request):
        """get private key from simple password"""
        pass
