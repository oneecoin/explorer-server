from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None

    wallet = models.OneToOneField(
        "wallets.Wallet", on_delete=models.CASCADE, related_name="user"
    )
    email = models.EmailField(unique=True)
    avatar = models.URLField(null=True)

    REQUIRED_FIELDS = ["email", "wallet"]
