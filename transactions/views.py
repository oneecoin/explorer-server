import datetime
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TransactionSerializer, CreateTransactionSerializer
from .models import Transaction
from inbox.models import Message
from users.models import User


class Transactions(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateTransactionSerializer(data=request.data)
        if serializer.is_valid():
            # count++
            transaction = Transaction.objects.get(date=datetime.datetime.now().date())
            transaction.count += 1
            transaction.save()

            # inbox
            try:
                data = serializer.data
                user = User.objects.get(wallet__public_key=data.get("receiver"))
                Message.create_transaction_message(
                    user,
                    request.user.wallet.public_key,
                    data.get("amount"),
                )
            except User.DoesNotExist:
                pass
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TransactionsCount(APIView):
    def get(self, request):
        """see transactions count"""
        scope = request.GET.get("scope")
        now = datetime.datetime.now().date()
        if scope == "week":
            # get last 7 days
            transactions = Transaction.objects.filter(
                Q(date__lte=now) & Q(date__gte=now - datetime.timedelta(days=7))
            )
        elif scope == "month":
            # get last 30 days
            transactions = Transaction.objects.filter(
                Q(date__lte=now) & Q(date__gte=now - datetime.timedelta(days=30))
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
