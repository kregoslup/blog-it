from apps.blog.tools import *
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from apps.blog.serializers import UserSerializer
from apps.blog.models import User


class TenPerDayUserThrottle(UserRateThrottle):
    rate = '10/day'


class ApiEndpoint(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    signer = {}

    @throttle_classes([TenPerDayUserThrottle])
    def get(self, request, format=None):
        if request.META.code is None:
            authorization_url, state, signer = sign_up(CLIENT_ID,
                                                       AUTHORIZATION_URL)
            self.signer.update({state: signer})
            # TODO: Redirect to authorization_url
        else:
            signer = self.signer.get(request.META.state)
            token = fetch_token(signer, token_url=TOKEN_URL,
                                client_secret=CLIENT_SECRET)
