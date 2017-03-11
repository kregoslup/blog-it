import github3
from django.http.response import Http404
from django.views.generic.base import RedirectView
from rest_framework.generics import RetrieveAPIView

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


class ProfileInfoView(RetrieveAPIView):
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        data = {
            "username": request.session['username'],
            "access_token": request.session['token']
        }
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        User.objects.update_or_create(
            username=data['username'],
            defaults=serializer.validated_data
        )
        repositories = profile.get_all_repositories(data['access_token'])
        return Response(data=[serializer.data, repositories],
                        status=status.HTTP_200_OK)


class OauthCallback(RedirectView):
    url = '/profile'

    def get(self, request, *args, **kwargs):
        token = oauth2.get_token(request)
        request.session['token'] = token['access_token']
        gh = github3.GitHub(token=token)
        user = gh.user()
        if not user:
            raise Http404()
        request.session['username'] = user.as_dict()['login']
        return super(OauthCallback, self).get(request, *args, **kwargs)


def oauth_login(request):
    return redirect(oauth2.get_authorization_url())
