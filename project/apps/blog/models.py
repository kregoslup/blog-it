from django.contrib.auth.models import AbstractUser
from django.db import models
from urllib.parse import urljoin


class User(AbstractUser):
    username = models.CharField(blank=False, null=False, max_length=200,
                                unique=True)
    access_token = models.CharField(blank=True, null=False, max_length=300)

    def __repr__(self):
        return '<User(username=%r, a_token=%r)' % (
            self.username, self.access_token)


class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True, null=False,
                             blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=300, null=False, blank=False)

    @property
    def full_name(self):
        return urljoin('http://github.com',  '/'.join((self.owner.username, self.name)))

    def __repr__(self):
        return '<Blog(title=%s, owner=%s full_name=%s)>' % (self.title,
                                                            self.owner.username,
                                                            self.full_name)
