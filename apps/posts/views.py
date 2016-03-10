from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from apps.posts.models import Post
from apps.posts.serializers import PostSerializer
from rest_framework.decorators import api_view
from apps.posts.tasks import res


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@api_view(['POST'])
def webhook(request):
    request_data = request.body
    if "zen" in request_data.keys() or not request_data['ref'].endswith('master'):
        return Response(status=status.HTTP_200_OK)
    else:
        commits = [commit for commit in request_data['commits']]
        repo_name = request_data["repository"]['name']
        username = request_data['repository']['owner']['name']
        res.apply_acync(username, repo_name, commits)
        return Response(status=status.HTTP_200_OK)
