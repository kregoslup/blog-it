import json

import github3
from apps.blog.models import Blog, User
from celery import chain
from celery.task import task
from celery.utils.log import get_task_logger
from django.core.exceptions import ObjectDoesNotExist

from project.apps.posts.models import Post
from project.github.repos import download_file

logger = get_task_logger(__name__)


@task
def parse_existing_repository(data):
    try:
        user = User.objects.get(acccess_token=data['token'])
        blog = Blog.objects.get(name=data['repo_name'])
    except ObjectDoesNotExist as exc:
        logger.info('{} : {} does not exist'.format(data['token'],
                                                    data['repo_name']))
        raise parse_existing_repository.retry(exc=exc)
    else:
        bulk_posts = []
        for file in data['d_urls']:
            body = download_file(file[0], data['token'])
            if '.' in file[1]:
                post_title = file[1].split('.')[-1]
            else:
                post_title = file[1]
            bulk_posts.append(Post(title=post_title, body=body, blog=blog,
                                   author=user))
        Post.objects.bulk_create(bulk_posts, batch_size=len(bulk_posts))


@task
def check_existing_repository(username, token, repo_name):
    gh = github3.GitHub(token=token)
    repository = gh.repository(username, repo_name)
    contents_url = repository.as_dict().get("contents_url").replace('{+path}', '')
    download_urls = [(url.get("download_url"), url.get("name"))
                     for url in json.loads(repository._get(contents_url).text)]
    if download_urls:
        data = {"d_urls": download_urls, "token": token, "repo_name": repo_name}
        return data


res = chain(check_existing_repository, parse_existing_repository)
