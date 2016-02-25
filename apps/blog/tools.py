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

    def sign_up(self):
        signer = OAuth2Session(self.client_id, scope=self.scope)
        authorization_url, state = signer.authorization_url(
            self.authorization_base_url)
        self.signer.update({state: signer})
        return authorization_url

    def fetch_token(self, request):
        signer = self.signer.get(request.META.state)
        token = signer.fetch_token(self.token_url,
                                        client_secret=self.client_secret,
                                        authorization_response=self.redirect_uri)

        return token

    def get_username(self):
        username = self.signer.get('https://api.github.com/user').json().get(
            "login")
        return username
