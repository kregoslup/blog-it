from requests_oauthlib import OAuth2Session
from apps.blog.credentials import *
from django.shortcuts import redirect

token_dict = {}


def sign_up():
    signer = OAuth2Session(CLIENT_ID, scope=SCOPE)
    authorization_url, state = signer.authorization_url(
        AUTHORIZATION_URL)
    token_dict.update({state: signer})
    return authorization_url


def fetch_token(request):
    signer = token_dict.get(request.META.state)
    token = signer.fetch_token(TOKEN_URL,
                               client_secret=CLIENT_SECRET,
                               authorization_response=REDIRECT_URL)

    return token, signer


def get_username(signer):
    username = signer.get('https://api.github.com/user').json().get(
        "login")
    return username


def authorization(request):
    if request.json().get("code") is None:
        return redirect(sign_up())
    else:
        token, signer = fetch_token(request)
        username = get_username(signer)
        return token, username
