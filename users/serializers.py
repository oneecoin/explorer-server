from rest_framework import serializers
from wallets.serializers import WalletSerializer
from .models import User


class ListUserSerializer(serializers.ModelSerializer):
    public_key = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "public_key",
        )

    def get_public_key(self, user):
        return user.wallet.public_key


class PublicUserSerializer(serializers.ModelSerializer):
    public_key = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "public_key",
            "avatar",
        )

    def get_public_key(self, user):
        return user.wallet.public_key


class CommonUserSerializer(serializers.ModelSerializer):
    message_count = serializers.SerializerMethodField()
    public_key = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "message_count",
            "public_key",
            "avatar",
        )

    def get_message_count(self, user):
        return user.messages.count()

    def get_public_key(self, user):
        return user.wallet.public_key


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class PrivateUserSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()

    class Meta:
        model = User
        fields = (
            "pk",
            "email",
            "username",
            "wallet",
            "avatar",
        )
