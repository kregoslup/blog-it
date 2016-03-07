from apps.blog.models import Blog, User
from apps.posts.models import Commit, Post
from celery.task import task
import github3
from github.repos import download_file
from django.core.exceptions import ObjectDoesNotExist


# TODO: Sanity checks


@task
def sync_posts(data):
    u = User.objects.get(username=data['username'])
    b = Blog.objects.get(name=data['repo'], owner=u)
    posts_bulk_create_data = []
    for file in data['files']:
        post_body = download_file(file['raw_url'], u.access_token)
        posts_bulk_create_data.append(Post(title=file['filename'].split('.')[-1],
                                           body=post_body, blog=b, author=u))
    Post.objects.bulk_create(posts_bulk_create_data,
                             batch_size=len(posts_bulk_create_data))


@task
def sync_commits(data):
    u = User.objects.get(username=data['username'])
    b = Blog.objects.get(name=data['repo'], owner=u)
    commit_bulk_create_data = []
    for commit in data:
        commit_bulk_create_data.append(Commit(hash=commit['hash'],
                                              title=commit['title'], blog=b))
    if commit_bulk_create_data:
        Post.objects.bulk_create(commit_bulk_create_data,
                                 batch_size=len(commit_bulk_create_data))

    gh = github3.GitHub(token=u.access_token)
    gh_repo = gh.repository(u.username, b.name)
    commit_additional_data = gh_repo.commit(data['hash'])
    data.update({"files": commit_additional_data.as_dict()['files']})
    sync_posts.delay(data)


@task
def parse_webhook(request_data):
    commits = [commit for commit in request_data['commits']]
    repo = request_data["repository"]['name']
    username = request_data['owner']['name']
    commits_data = []
    for commit in commits:
        commits_data.append({"hash": commit['id'], "title": commit['message'],
                            "blog": repo, "username": username})
    sync_commits.delay(commits_data)
