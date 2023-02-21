from rest_framework.views import APIView


class SearchUsers(APIView):
    def get(self, request):
        """see list of users"""
        pass


class Me(APIView):
    def get(self, request):
        """see my info"""
        pass

    def put(self, request):
        """change my info"""
        pass


class Wallet(APIView):
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


class PublicUser(APIView):
    def get(self, request):
        """get information about user"""
        pass
