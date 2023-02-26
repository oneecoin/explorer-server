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

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "message_count",
            "avatar",
        )

    def get_message_count(self, user):
        return user.messages.count()


class UpdateUserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = (
            "username",
            "avatar",
        )

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        return instance


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
