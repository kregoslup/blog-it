from apps.blog.tools import *
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from apps.blog.serializers import UserSerializer
from apps.blog.models import User
from apps.blog.tools import OAuth2Signup


class TenPerDayUserThrottle(UserRateThrottle):
    rate = '10/day'


class ApiEndpoint(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    sign_client = OAuth2Signup

    @throttle_classes([TenPerDayUserThrottle])
    def get(self, request):
        if request.META.code is None:
            authorization_url = self.sign_client.sign_up()
            # TODO: Redirect to authorization_url
        else:
            token, username = self.sign_client.fetch_token(request)
            # TODO: Drop sign_client.signer dict entry where state is the same
            # as in request.get.META.state after serializing and saving to database
