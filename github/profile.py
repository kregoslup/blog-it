import github3
from rest_framework import status
from rest_framework.response import Response


def get_all_repos(gh):
    repositories = [name for name in gh.all_repositories['name']]
    if not repositories:
        return Response({"message": "No repositories"},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        return repositories


def get_username(request):
    gh = github3.login(token=request.session['token'])
    user = gh.me()['login']
    if not user:
        return Response({"message": "Invalid user"},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        request.session['username'] = user
        return user, gh
