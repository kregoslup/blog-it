from django.db import models
from apps.blog.models import Blog, GithubUser


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True, null=False, blank=False)
    created = models.DateField()
    updated = models.DateField()
    body = models.TextField(max_length=3000, null=False, blank=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(GithubUser, on_delete=models.CASCADE)

    def __repr__(self):
        return 'Post: %r Author: %r>' % self.title, self.author.username

    class Meta:
        ordering = ('creation_date',)


class Commit(models.Model):
    hash = models.CharField(blank=False, null=False, max_length=40)
    title = models.CharField(blank=False, null=False, max_length=50)
    data = models.TextField(blank=False, null=False, max_length=3000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.OneToOneField(GithubUser, on_delete=models.CASCADE)

    def __repr__(self):
        return '<Commit(hash=%r, title=%r, post=%r, author=%r)' % self.hash,\
               self.title, self.post, self.author.username

