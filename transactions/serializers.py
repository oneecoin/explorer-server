from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class CreateTransactionSerializer(serializers.Serializer):
    receiver = serializers.CharField()
    amount = serializers.IntegerField(min_value=1)
