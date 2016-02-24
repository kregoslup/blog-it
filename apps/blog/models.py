from django.db import models
from urllib.parse import urljoin


class GithubUser(models.Model):
    username = models.CharField(blank=False, null=False, max_length=200)
    access_token = models.CharField(blank=True, null=False, max_length=300)
    refresh_token = models.CharField(blank=False, null=False, max_length=300)

    def __repr__(self):
        return '<User(username=%r, a_token=%r)' % self.username, self.access_token


class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True, null=False,
                             blank=False)
    owner = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300, null=False, blank=False)

    @property
    def full_name(self):
        return urljoin('http://github.com',
                       self.owner.username + '/' + self.full_name)

    def __repr__(self):
        return '<Blog(title=%r, owner=%r full_name=%r)>' % self.title,\
               self.owner.username, self.full_name
