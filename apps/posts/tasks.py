from apps.blog.models import Blog, User
from apps.posts.models import Commit
from celery.task import task
from apps.posts.serializers import CommitSerializer
import github3


@task
def sync_posts(data):
    pass


@task
def parse_webhook(request_data):
    commits = [commit for commit in request_data['commits']]
    repo = request_data["repository"]['name']
    username = request_data['owner']['name']

    u = User.objects.get(username=username)
    b = Blog.objects.get(name=repo, owner=u)
    gh = github3.GitHub(token=u.access_token)
    gh_repo = gh.repository(u.username, b.name)

    for commit in commits:
        data = {"hash": commit['id'], "title": commit['message'],
                     "blog": repo, "username": username, "token": u.access_token}
        c = Commit(hash=data['hash'], title=data['title'], blog=b)
        c.save()
        commit_additional_data = gh_repo.commit(data['hash'])
        data.update({"files": commit_additional_data.as_dict()['files']})
        sync_posts.delay(data)
