from apps.blog.serializers import UserSerializer, BlogSerializer
from apps.blog.models import Blog, User
from github import oauth2, profile, repos
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from django.shortcuts import redirect


class BlogsList(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


def profile_info(request):
    data = {"token": request.session['token'],
            "username": request.session['username']}
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        names = profile.get_all_repos(data['token'])
        return Response(data={serializer.data: names},
                        status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


def oauth_callback(request):
    token = oauth2.get_token(request)
    request.session['token'] = token['access_token']
    request.session['username'] = \
        profile.get_username(token['access_token']).as_dict()['login']
    return redirect('/profile/')


def oauth_login(request):
    return redirect(oauth2.get_authorization_url())
