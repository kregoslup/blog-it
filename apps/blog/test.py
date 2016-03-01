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
        response = self.client.get('/api/blogs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_test_blog(self):
        u = User(username="testuser", access_token="accesstoken")
        u.save()
        data = {"title": "testitle",
                "name": "testname",
                "owner": u.pk}
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        self.assertEqual(Blog.objects.count(), 1)

    def test_api_create_blog(self):
        u = User(username="testuser", access_token="accesstoken")
        u.save()
        data = {"title": "testitle",
                "name": "testname",
                "owner": u.pk}
        response = self.client.post('/api/blogs/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_blog(self):
        u = User(username="testuser", access_token="accesstoken")
        u.save()
        b = Blog(id=1, title="sampetitle", name="samplename", owner=u)
        b.save()
        response = self.client.get('/api/blogs/1/')
        self.assertEqual(response.data, {"id": 1,
                                         "title": "sampetitle",
                                         "name": "samplename",
                                         "owner": u.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserSerializerTest(APITestCase):
    def test_create_user(self):
        data = {"username": "testusername",
                "access_token": "testoken"}
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        self.assertEqual(User.objects.count(), 1)
