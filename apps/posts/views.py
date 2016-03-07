from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from apps.posts.models import Post
from apps.posts.serializers import PostSerializer
from rest_framework.decorators import api_view
from apps.posts.tasks import parse_webhook


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@api_view(['POST'])
def webhook(request):
    request_data = request.body
    if ["zen"] in request_data:
        return Response(status=status.HTTP_200_OK)
    else:
        parse_webhook.delay(request_data, serializer='json')
        return Response(status=status.HTTP_200_OK)
