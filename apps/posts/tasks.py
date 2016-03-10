from apps.blog.models import Blog, User
from apps.posts.models import Commit, Post
from celery.task import task
import github3
from github.repos import download_file
from celery import chain

# TODO: Sanity checks


@task
def sync_posts(username, repo_name, commits_data):
    u = User.objects.get(username=username)
    b = Blog.objects.get(name=repo_name, owner=u)
    added = set()
    removed = set()
    for commit in commits_data:
        for files in commit['files']:
            if '.' in files['filename']:
                filename = files['filename'].split('.')[-1]
            else:
                filename = files['filename']
            if files['status'] is 'modified' and files['filename'] not in added:
                added.add(files['filename'])
                post_body = download_file(files['contents_url'], u.access_token)
                Post.objects.filter(title=filename, blog=b).update(body=post_body)
            elif files['status'] is 'added' and files['filename'] not in added:
                added.add(files['filename'])
                obj, created = User.objects.get_or_create(username=commit['commit_author'],
                                                          defaults={"username": commit['commit_author']})
                post_body = download_file(files['contents_url'], u.access_token)
                Post.objects.create(title=filename, body=post_body,
                                    blog=b, author=obj)
            elif files['status'] is 'removed' and files['filename'] not in added:
                removed.add(filename)
                Post.objects.filter(title=filename, blog=b).delete()


@task
def sync_commits(username, repo_name, commits_data):
    u = User.objects.get(username=username)
    b = Blog.objects.get(name=repo_name, owner=u)
    gh = github3.GitHub(token=u.access_token)
    gh_repo = gh.repository(u.username, b.name)
    commit_bulk_create_data = [
        Commit(hash=commit['hash'], title=commit['title'],
               blog=b) for commit in commits_data]
    Commit.objects.bulk_create(commit_bulk_create_data,
                               batch_size=len(commit_bulk_create_data))
    for commit in commits_data:
        commit.update(
            {"files": gh_repo.commit(commit['hash']).as_dict()['files']})

    return username, repo_name, commits_data.sort(key=lambda x: x['timestamp'])


@task
def parse_webhook(username, repo_name, commits):
    commits_data = [{"hash": commit['id'], "title": commit['message'],
                     "timestamp": commit['timestamp'],
                     "commit_author": commit['committer']['username']}
                    for commit in commits]
    return username, repo_name, commits_data


res = chain(parse_webhook, sync_commits, sync_posts)
