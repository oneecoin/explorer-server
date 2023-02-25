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

    @classmethod
    def make_simple_pwd_message_again(self, user):
        message = Message.objects.create(
            to=user,
            title="지갑 정보가 바뀌었습니다!",
            content="간편 비밀번호가 초기화 되었습니다",
            message_type=Message.MessageType.SYSTEM,
        )
        message.save()

    @classmethod
    def create_transaction_message(self, user, sender: str, amount: int):
        message = Message.objects.create(
            to=user,
            title=f"당신의 지갑에 추가된 금액: {amount:,}",
            content=f"{sender}에서 {amount:,}OCN을 송금하였습니다",
            message_type=Message.MessageType.SYSTEM,
        )
        message.save()

    @classmethod
    def make_wallet_message(self, user):
        message = Message.objects.create(
            to=user,
            title="지갑을 만들어 주세요!",
            content="새로운 계정에는 지갑이 만들어져있지 않습니다",
            message_type=Message.MessageType.SYSTEM,
        )
        message.save()
