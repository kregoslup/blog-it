from django.db import models
from apps.posts.models import Post


class Comments(models.Model):
    post = models.ForeignKey(Post)
    title = models.CharField(max_length=100)
    body = models.TextField()
    pub_date = models.DateField()
    nickname = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s' % self.title

    class Meta:
        ordering = ('pub_date',)