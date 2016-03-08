from requests_oauthlib import OAuth2Session
from rest_framework.test import APITestCase
from github.oauth2 import *
from rest_framework import status
from django.test.client import Client
from django.test import mock
from django.core.urlresolvers import reverse
from importlib import import_module
from django.conf import settings
from apps.blog.models import User, Blog
from apps.blog.serializers import UserSerializer, BlogSerializer

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


class BlogSerializerTest(APITestCase):
    def test_get_blogs(self):
        response = self.client.get('/blogs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_blog_post(self):
        u = User(username='test', access_token='testtoken')
        u.save()
        response = self.client.post('/blogs/', data={"title": "test", "owner": u.pk,
                                                     "name": "test"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_created_blog(self):
        u = User(username='test', access_token='testtoken')
        u.save()
        response = self.client.post('/blogs/', data={"title": "test", "owner": u.pk,
                                    "name": "test"})
        b = Blog.objects.get(title='test')
        response = self.client.get('/blogs/' + str(b.pk), follow=True)
        self.assertEqual(response.data, {'name': 'test', 'id': 2, 'title': 'test',
                                         'owner': 2})


class UserCreateTest(APITestCase):
    def testcase(self):
        u = User(username="testowy", access_token="pleple")
        u.save()
        data = {"username": 'testowy', "access_token": 'pleple1'}
        ser = UserSerializer(data=data)
        if ser.is_valid():
            obj, created = User.objects.update_or_create(username="testowy", defaults=ser.validated_data)
            obj.save()
            u = User.objects.get(access_token='pleple1')
            response = Response(data=ser.data)
            self.assertEqual(response.data, ser.data)
            self.assertEqual(User.objects.count(), 1)
