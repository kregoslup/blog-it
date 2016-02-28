import github3


def get_username(request):
    gh = github3.login(token=request.session['token'])
    user = gh.me()['login']
    return user
