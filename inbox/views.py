from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import MessageSerializer
from .models import Message


class AllMessages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """get all messages"""
        messages = request.user.messages
        serializer = MessageSerializer(messages, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def delete(self, request):
        """delete all messages"""
        messages = request.user.messages
        with transaction.atomic():
            for message in messages:
                message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AMessage(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """delete a message"""
        try:
            message = Message.objects.get(pk=pk)
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
