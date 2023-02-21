from django.urls import path

urlpatterns = [
    path("search"),
    path("me"),
    path("me/wallet"),
    path("me/wallet/simple-password"),
    path("@<int:id>"),
]
