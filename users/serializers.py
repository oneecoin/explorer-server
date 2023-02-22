from rest_framework import serializers
from wallets.serializers import WalletSerializer
from .models import User


class ListUserSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "wallet",
        )
