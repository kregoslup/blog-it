from requests_oauthlib import OAuth2Session
from apps.blog.credentials import *


class OAuth2Signup:
    signer = {}
    client_id = CLIENT_ID
    scope = SCOPE
    authorization_base_url = AUTHORIZATION_URL
    redirect_uri = REDIRECT_URL
    token_url = TOKEN_URL
    client_secret = CLIENT_SECRET

    @staticmethod
    def sign_up():
        signer = OAuth2Session(OAuth2Signup.client_id, scope=OAuth2Signup.scope)
        authorization_url, state = signer.authorization_url(
            OAuth2Signup.authorization_base_url)
        OAuth2Signup.signer.update({state: signer})
        return authorization_url

    @staticmethod
    def fetch_token(request):
        signer = OAuth2Signup.signer.get(request.META.state)
        token = signer.fetch_token(OAuth2Signup.token_url,
                                        client_secret=OAuth2Signup.client_secret,
                                        authorization_response=OAuth2Signup.redirect_uri)

        return token, signer

    @staticmethod
    def get_username(signer):
        username = signer.get('https://api.github.com/user').json().get(
            "login")
        return username
