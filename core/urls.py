from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import GithubAuth

urlpatterns = [
    path("github", GithubAuth.as_view()),
    path("refresh", TokenRefreshView.as_view()),
]
