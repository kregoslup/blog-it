from requests_oauthlib import OAuth2Session
from apps.blog.credentials import *


class OAuth2Signup:
    signer = {}
    client_id = CLIENT_ID
    scope = SCOPE
    authorization_base_url = AUTHORIZATION_URL
    redirect_uri = REDIRECT_URL

    def sign_up(self):
        signer = OAuth2Session(self.client_id, scope=self.SCOPE)
        authorization_url, state = signer.authorization_url(self.authorization_base_url)
        return authorization_url, state, signer

    def fetch_token(self, signer, token_url, client_secret):
        token = signer.fetch_token(token_url, client_secret=client_secret,
                                   authorization_response=self.redirect_uri)
        username = signer.get('https://api.github.com/user').json().get("login")

        return token, username
