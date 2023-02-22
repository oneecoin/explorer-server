from django.db import models


class Message(models.Model):
    class MessageType(models.TextChoices):
        TRANSACTION = "transaction", "Transaction"
        SYSTEM = "system", "System"

    receiver = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=50)
    message_type = models.CharField(max_length=20, choices=MessageType.choices)
