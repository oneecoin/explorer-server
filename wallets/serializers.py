from rest_framework import serializers
from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = (
            "public_key",
            "private_key_hash",
        )


class ExposeWalletSerializer(serializers.Serializer):
    public_key = serializers.CharField(max_length=128)
    private_key = serializers.CharField(max_length=300)


class SimplePasswordSerializer(serializers.Serializer):
    simple_password = serializers.CharField(max_length=32)
    private_key = serializers.CharField(max_length=300)


class GetPrivateKeySerializer(serializers.Serializer):
    simple_password = serializers.CharField(max_length=32)
