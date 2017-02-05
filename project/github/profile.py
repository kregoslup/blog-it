import github3
from rest_framework import status
from rest_framework.response import Response


def get_all_repos(token):
    gh = github3.GitHub(token=token)
    repositories = [repo for repo in gh.repositories("owner")]
    if not repositories:
        return Response({"message": "No repositories"},
                        status=status.HTTP_400_BAD_REQUEST)
    return [repo.as_dict().get("name") for repo in repositories]


def get_username(token):
    gh = github3.GitHub(token=token)
    user = gh.me()
    if not user:
        return Response({"message": "Invalid user"},
                        status=status.HTTP_400_BAD_REQUEST)
    return user
