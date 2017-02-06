from project.apps.blog.models import Blog, User
from project.apps.blog.tasks import res
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from project.github import profile, repos
from rest_framework import status, viewsets
from rest_framework.response import Response

from project.apps.blog.serializers import UserSerializer, BlogSerializer
from project.github import oauth2


class BlogsViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def perform_create(self, serializer):
        try:
            serializer.save()
            user = User.objects.get(pk=serializer.data['owner'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            repos.create_webhook(user.access_token, serializer.data['name'])
            res.apply_async(user.username, user.access_token, serializer.data['name'])


def profile_info(request):
    data = {"username": request.session['username'],
            "access_token": request.session['token']}
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        User.objects.update_or_create(username=data['username'],
                                      defaults=serializer.validated_data)
        repo_names = profile.get_all_repos(data['access_token'])
        return Response(data=[serializer.data, repo_names],
                        status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def oauth_callback(request):
    token = oauth2.get_token(request)
    request.session['token'] = token['access_token']
    request.session['username'] = \
        profile.get_username(token['access_token']).as_dict()['login']
    return redirect('/profile/')


def oauth_login(request):
    return redirect(oauth2.get_authorization_url())
