from django.db import models
from apps.blog.models import Blog


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True, null=False, blank=False)
    creation = models.DateField()
    update = models.DateField()
    body = models.TextField(max_length=3000, null=False, blank=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __unicode__(self):
        return '%s' % self.title

    class Meta:
        ordering = ('creation_date',)


class Commit(models.Model):
    hash = models.CharField(blank=False, null=False, max_length=10)
    title = models.CharField(blank=False, null=False, max_length=50)
    data = models.TextField(blank=False, null=False, max_length=3000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
