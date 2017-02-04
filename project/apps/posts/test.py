from project.apps.blog.credentials import thook
from project.apps.posts.tasks import sync_posts
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from project.apps.blog.tasks import *


class PostAPITest(APITestCase):
    def test_get_posts(self):
        u = User(username='kregoslup', access_token='')
        u.save()
        response = self.client.post('/blogs/',
                                    data={"title": "test", "owner": u.pk,
                                          "name": "testrepo"})
        b = Blog.objects.get(title='test')
        response = self.client.get('/blogs/' + str(b.pk) + '/' + 'posts' + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        u = User(username='kregoslup', access_token='')
        u.save()
        response = self.client.post('/blogs/',
                                    data={"title": "test", "owner": u.pk,
                                          "name": "testrepo"})
        b = Blog.objects.get(title='test')
        response = self.client.post('/blogs/' + str(b.pk) + '/' + 'posts' + '/',
                                    data={'title': 'test', 'body': 'test',
                                          'blog': b.pk, 'author': u.pk})
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_created_post(self):
        u = User(username='kregoslup', access_token='')
        u.save()
        response = self.client.post('/blogs/',
                                    data={"title": "test", "owner": u.pk,
                                          "name": "testrepo"})
        b = Blog.objects.get(title='test')
        response = self.client.post('/blogs/' + str(b.pk) + '/' + 'posts' + '/',
                                    data={'title': 'test', 'body': 'test',
                                          'blog': b.pk, 'author': u.pk})
        p = Post.objects.get(title='test')
        reponse = self.client.get('/blogs/' + str(b.pk) + '/' + 'posts' + '/' + str(p.pk),
                                  follow=True)
        self.assertEqual(reponse.status_code, status.HTTP_200_OK)


class TestCeleryTask(TestCase):

    def test_sync_posts(self):
        u = User.objects.create(username='kregoslup',
                                access_token="")
        Blog.objects.create(title='testblog', owner=u, name='testrepo')
        sync_posts('kregoslup', 'testrepo', thook)
        self.assertEqual(Post.objects.count(), 1)
