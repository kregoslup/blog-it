from django.db import models
from django.contrib.auth.models import User
import datetime
from apps.posts.models import Post


class GithubUser(models.Model):
    user = models.OneToOneField(User, related_name='user')
    github_username = models.CharField(blank=False)
    access_token = models.TextField(blank=True)
    refresh_token = models.CharField(blank=True)


class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    github_url = models.URLField()


    def __unicode__(self):
        return '%s' % self.title
