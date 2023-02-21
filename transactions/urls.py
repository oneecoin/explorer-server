from django.urls import path
from .views import TransactionsCount

urlpatterns = [
    path("count", TransactionsCount.as_view()),
]
