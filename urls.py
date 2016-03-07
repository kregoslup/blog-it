from django.conf.urls import url, include
from apps.blog.views import *
from rest_framework_nested import routers
from apps.blog.views import BlogsList, profile_info
from apps.posts.views import PostViewSet


router = routers.SimpleRouter()
router.register(r'blogs', BlogsList)

blogs_router = routers.NestedSimpleRouter(router, r'blogs', lookup='blog')
blogs_router.register(r'posts', PostViewSet, base_name='blog-posts')


urlpatterns = [
    url(r'^github/login/$', oauth_login),
    url(r'^github/login/callback/$', oauth_callback),
    url(r'^profile/$', profile_info),
    url(r'^', include(router.urls)),
    url(r'^', include(blogs_router.urls)),
]
