from apps.blog.serializers import UserSerializer, BlogSerializer
from apps.blog.models import User
from github import oauth2, profile


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
    user, gh = profile.get_username(request)
    serializer = UserSerializer(username=user,
                                access_token=request.session['oauth2_token'])
    if serializer.is_valid():
        serializer.save()
    repos = profile.get_all_repos(gh)
    return {user: repos}


def oauth_callback(request):
    oauth2.get_token(request)


def oauth_login(request):
    oauth2.get_authorization_url()
