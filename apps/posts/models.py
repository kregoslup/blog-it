from django.db import models
from apps.blog.models import Blog


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    creation_date = models.DateField()
    body = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


    def __unicode__(self):
        return '%s' % self.title

    class Meta:
        ordering = ('creation_date',)