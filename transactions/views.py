import datetime
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TransactionSerializer
from .models import Transaction


class TransactionsCount(APIView):
    def get(self, request):
        """see transactions count"""
        scope = request.GET.get("scope")
        now = datetime.datetime.now().date()
        if scope == "week":
            # get last 7 days
            transactions = Transaction.objects.filter(
                Q(date__lte=now) & Q(date_gte=now - datetime.timedelta(days=7))
            )
        elif scope == "month":
            # get last 30 days
            transactions = Transaction.objects.filter(
                Q(date__lte=now) & Q(date_gte=now - datetime.timedelta(days=30))
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
