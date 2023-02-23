from django.db import models


class Transaction(models.Model):
    date = models.DateField()
    count = models.PositiveIntegerField()
