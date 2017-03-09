import github3
from urllib.parse import urljoin
import requests
import json
from project.apps.blog import credentials


def create_webhook(token, repo_name):
    gh = github3.GitHub(token=token)
    webhook_url = urljoin(credentials.DOMAIN, 'webhook')
    repository = gh.repository(gh.me(), repo_name)
    config = {
        "url": webhook_url,
        "content_type": "json"
    }
    repository.create_hook(name='web', config=config, events=list('push'))


def download_file(url, token):
    headers = {'Authorization': 'token ' + token}
    r = requests.get(url=url, headers=headers)
    return r.text
