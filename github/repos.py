import github3
from urllib.parse import urljoin
import requests
import json
from apps.blog import credentials


def create_webhook(token, repo_name):
    gh = github3.GitHub(token=token)
    webhook_url = urljoin(credentials.DOMAIN, 'webhook')
    repository = gh.repository(gh.me(), repo_name)
    config = {"url": webhook_url, "content_type": "json"}
    repository.create_hook(name='web', config=config, events=list('push'))


def download_file(url, token):
    headers = {'Authorization': 'token ' + token}
    r = requests.get(url=url, headers=headers)
    return r.text


def parse_existing_repository(gh, repo_name, username, token):
    repository = gh.repository(username, repo_name)
    contents_url = repository.as_dict().get("contents_url").replace('{+path}', '')
    download_urls = [(url.get("download_url"), url.get("name"))
                     for url in json.loads(repository._get(contents_url).text)]
    if download_urls:
        files = [dict(text=download_file(url, token), name=name) for (url, name) in download_urls]
        return files
