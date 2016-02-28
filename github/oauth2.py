from requests_oauthlib import OAuth2Session
from apps.blog.credentials import *
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import redirect
from importlib import import_module
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


def get_authorization_url():
    github = OAuth2Session(CLIENT_ID, scope=SCOPE)
    authorization_url, state = github.authorization_url(
        AUTHORIZATION_URL)
    s = SessionStore()
    s['state'] = state
    if not all((authorization_url, state)):
        return Response({"message": "Invalid authorization url"},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        redirect(authorization_url)


def get_token(request):
    code = request.GET['code']
    state = request.session['state']
    github = OAuth2Session(CLIENT_ID, scope=SCOPE, state=state)
    token = github.fetch_token(TOKEN_URL,
                               client_secret=CLIENT_SECRET,
                               authorization_response=REDIRECT_URL,
                               code=code)

    if not all((code, state, token)):
        return Response(data={"message": "Invalid token"},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        request.session['oauth_token'] = token
        redirect('profile')

