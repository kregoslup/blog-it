from rest_framework.generics import CreateAPIView

from project.apps.posts.serializers import PostSerializer
from project.apps.posts.tasks import res
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from project.apps.posts.models import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class WebhookCreateAPIView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        request_data = request.body
        if "zen" not in request_data.keys() or request_data['ref'].endswith('master'):
            commits = [commit for commit in request_data['commits']]
            repo_name = request_data["repository"]['name']
            username = request_data['repository']['owner']['name']
            res.apply_async(username, repo_name, commits)
        return Response(status=status.HTTP_200_OK)
