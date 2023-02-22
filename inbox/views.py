from rest_framework.views import APIView


class AllMessages(APIView):
    def get(self, request):
        """get all messages"""
        pass

    def delete(self, request):
        """delete all messages"""
        pass


class AMessage(APIView):
    def delete(self, request):
        """delete a message"""
        pass
