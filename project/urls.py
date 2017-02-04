from project.apps.blog.views import BlogsList, profile_info, oauth_login, oauth_callback
from django.conf.urls import url, include
from rest_framework_nested import routers

from project.apps.posts.views import PostViewSet, webhook

router = routers.SimpleRouter()
router.register(r'blogs', BlogsList)

blogs_router = routers.NestedSimpleRouter(router, r'blogs', lookup='blog')
blogs_router.register(r'posts', PostViewSet, base_name='blog-posts')


urlpatterns = [
    url(r'^github/login/$', oauth_login),
    url(r'^github/login/callback/$', oauth_callback),
    url(r'^profile/$', profile_info),
    url(r'^webhook/$', webhook),
    url(r'^', include(router.urls)),
    url(r'^', include(blogs_router.urls)),
]