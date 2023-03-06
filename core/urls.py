from django.urls import path
from .views import GithubAuth, Logout, Refresh

urlpatterns = [
    path("github", GithubAuth.as_view()),
    path("refresh", Refresh.as_view()),
    path("logout", Logout.as_view()),
]
