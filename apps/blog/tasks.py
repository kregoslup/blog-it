from apps.posts.models import Post
from apps.blog.models import Blog, User
import github3
from celery.task import task
import json
from github.repos import download_file
from apps.posts.tasks import sync_posts


@task
def parse_existing_repository(data):
    u = User.objects.get(acccess_token=data['token'])
    b = Blog.objects.get(name=data['repo_name'])
    bulk_posts = []
    for file in data['d_urls']:
        body = download_file(file[0], data['token'])
        if '.' in file[1]:
            post_title = file[1].split('.')[-1]
        else:
            post_title = file[1]
        bulk_posts.append(Post(title=post_title, body=body, blog=b, author=u))
    if len(bulk_posts) > 1:
        Post.objects.bulk_create(bulk_posts, batch_size=len(bulk_posts))
    else:
        p = bulk_posts[0]
        p.save()


@task
def check_existing_repository(request_data):
    token = request_data['access_token']
    repo_name = request_data['repo_name']
    gh = github3.GitHub(token=token)
    repository = gh.repository(request_data['username'], repo_name)
    contents_url = repository.as_dict().get("contents_url").replace('{+path}', '')
    download_urls = [(url.get("download_url"), url.get("name"))
                     for url in json.loads(repository._get(contents_url).text)]
    if download_urls:
        data = {"d_urls": download_urls, "token": token, "repo_name": repo_name}
        sync_posts.delay(data)
