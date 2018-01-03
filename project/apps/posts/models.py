import datetime
from urllib.parse import urljoin

from django.db import models

from project.apps.blog.models import Blog, User


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True, null=False,
                             blank=False)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
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

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.now()
        self.updated = datetime.datetime.now()
        return super(Post, self).save(*args, **kwargs)


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
