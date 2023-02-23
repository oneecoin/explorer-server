from django.urls import path
from .views import TransactionsCount, Transactions

urlpatterns = [
    path("", Transactions.as_view()),
    path("count", TransactionsCount.as_view()),
]
