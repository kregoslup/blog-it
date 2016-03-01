from apps.blog.serializers import UserSerializer, BlogSerializer
from apps.blog.models import User, Blog
from github import oauth2, profile
from rest_framework import generics
from django.shortcuts import redirect


class BlogsList(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


def chose_repo(request):
    if request.method == 'POST':
        repo = request.POST['repository']
        title = request.POST['title']
        owner = request.session['username']
        serializer = BlogSerializer(title=title, owner=owner, repo=repo)
        if serializer.is_valid():
            serializer.save()
# create hook


def profile_info(request):
    token = request.session['token']
    user, gh = profile.get_username(token['access_token'])
    data = {"username": user.as_dict().get("login"),
            "access_token": token['access_token']}
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    repos = profile.get_all_repos(gh)
    return redirect({(serializer.username, serializer.id): repos})


def oauth_callback(request):
    token = oauth2.get_token(request)
    request.session['token'] = token
    return redirect('/profile/')


def oauth_login(request):
    return redirect(oauth2.get_authorization_url())
