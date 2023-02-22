from django.db import models


class Message(models.Model):
    class MessageType(models.TextChoices):
        TRANSACTION = "transaction", "Transaction"
        SYSTEM = "system", "System"

    to = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="messages"
    )

    title = models.CharField(max_length=30)
    content = models.CharField(max_length=50)
    message_type = models.CharField(max_length=20, choices=MessageType.choices)

    @classmethod
    def make_simple_pwd_message(self, user):
        message = Message.objects.create(
            to=user,
            title="간편 비밀번호를 설정하세요!",
            content="Private key 대신 간편 비밀번호로 거래할 수 있습니다",
            message_type=Message.MessageType.SYSTEM,
        )
        message.save()
