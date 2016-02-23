from django.db import models
from django.contrib.auth.models import User
from urllib.parse import urljoin
from apps.posts.models import Post


class GithubUser(models.Model):
    github_username = models.CharField(blank=False, null=False, max_length=200)
    access_token = models.TextField(blank=True, null=False, max_length=300)
    refresh_token = models.TextField(blank=False, null=False, max_length=300)


class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True, null=False, blank=False)
    owner = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    _repository_name = models.CharField(max_length=300, null=False, blank=False)

    @property
    def repository_name(self):
        return self._repository_name

    @repository_name.setter
    def repository_name(self, value):
        self._repository_name = urljoin(self.owner.github_username, value)

    def __unicode__(self):
        return '%s' % self.title
