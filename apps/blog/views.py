from rest_framework.decorators import throttle_classes, api_view
from rest_framework.throttling import UserRateThrottle
from apps.blog.serializers import UserSerializer
from apps.blog.models import User
from apps.blog.tools import authorization


class TenPerDayUserThrottle(UserRateThrottle):
    rate = '10/day'


@throttle_classes([TenPerDayUserThrottle])
@api_view(['GET'])
def token_query(request):
    token, username = authorization(request)
    serializer = UserSerializer
    if serializer.is_valid():
        serializer.save(username=username, access_token=token)
