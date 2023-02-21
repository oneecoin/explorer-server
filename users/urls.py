from django.urls import path
from . import views

urlpatterns = [
    path("search", views.SearchUsers.as_view()),
    path("me", views.Me.as_view()),
    path("me/wallet", views.Wallet.as_view()),
    path("me/wallet/simple-password", views.SimplePassword.as_view()),
    path("@<int:id>", views.PublicUser.as_view()),
]
