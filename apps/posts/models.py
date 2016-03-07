from django.db import models
from apps.blog.models import Blog, User
from urllib.parse import urljoin
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.posts import tasks


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True, null=False,
                             blank=False)
    created = models.DateField(auto_created=True)
    updated = models.DateField(auto_now_add=True)
    body = models.TextField(max_length=3000, null=False, blank=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return 'Post: %r Author: %r>' % self.title, self.author.username

    @property
    def raw_content(self, file_name):
        return urljoin('http://raw.githubusercontent.com/repos',
                       '/'.join((self.blog.owner.username, self.blog.name,
                                 'master', file_name)))

    class Meta:
        ordering = ('created',)


class Commit(models.Model):
    hash = models.CharField(blank=False, null=False, max_length=100)
    title = models.CharField(blank=False, null=False, max_length=50)
    data = models.TextField(blank=False, null=False, max_length=3000)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __repr__(self):
        return '<Commit(hash=%r, title=%r, post=%r, author=%r)' % (self.hash,
                                                                   self.title,
                                                                   self.post,
                                                                   self.author.username)
