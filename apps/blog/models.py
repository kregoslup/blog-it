from django.db import models
from urllib.parse import urljoin


class GithubUser(models.Model):
    username = models.CharField(blank=False, null=False, max_length=200)
    access_token = models.TextField(blank=True, null=False, max_length=300)
    refresh_token = models.TextField(blank=False, null=False, max_length=300)


class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True, null=False, blank=False)
    owner = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, null=False, blank=False)

    @property
    def name(self):
        return urljoin('http://github.com', self.owner.username + '/' + self.name)

    def __repr__(self):
        return '<Blog: %r>' % self.title
