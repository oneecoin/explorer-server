import datetime
from transactions.models import Transaction


def create_transaction_model():
    transaction = Transaction.objects.create(
        date=datetime.datetime.now().date(), count=0
    )
    transaction.save()


def delete_outdated_transaction():
    now = datetime.datetime.now().date()
    transaction = Transaction.objects.filter(
        date_lt=now - datetime.timedelta(days=30),
    )
    transaction.delete()
