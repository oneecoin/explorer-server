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


class PublicUser(APIView):
    def get(self, request):
        """get information about user"""
        pass
