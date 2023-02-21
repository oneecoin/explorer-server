from django.urls import path
from .views import GithubAuth

urlpatterns = [
    path("github", GithubAuth.as_view()),
]
