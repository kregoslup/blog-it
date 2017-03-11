import github3


def get_all_repositories(token):
    gh = github3.GitHub(token=token)
    repositories = [repo for repo in gh.repositories("owner")]
    return [repo.as_dict().get("name") for repo in repositories]
