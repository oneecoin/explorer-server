from django.urls import path
from . import views as user_views
from wallets import views as wallet_views
from inbox import views as inbox_views

urlpatterns = [
    path("search", user_views.SearchUsers.as_view()),
    path("me", user_views.Me.as_view()),
    path("me/tiny", user_views.TinyMe.as_view()),
    path("me/inbox", inbox_views.AllMessages.as_view()),
    path("me/inbox/@<int:id>", inbox_views.AMessage.as_view()),
    path("me/wallet", wallet_views.MyWallet.as_view()),
    path("me/wallet/simple-password", wallet_views.SimplePassword.as_view()),
    path("@<int:id>", user_views.PublicUser.as_view()),
]
