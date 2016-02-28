from apps.blog.serializers import UserSerializer
from apps.blog.models import User
from django.shortcuts import redirect
from github import oauth2, profile


def profile_info(request):
    profile.get_username(request)


def oauth_callback(request):
    oauth2.get_token(request)
    redirect('profile')


def oauth_login(request):
    oauth2.get_authorization_url()
