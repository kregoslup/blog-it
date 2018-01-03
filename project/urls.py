from project.apps.blog.views import profile_info, oauth_login, oauth_callback
from django.conf.urls import url, include

from project.apps.posts.views import webhook

urlpatterns = [
    url(r'^github/login/$', oauth_login),
    url(r'^github/login/callback/$', oauth_callback),
    url(r'^profile/$', profile_info),
    url(r'^webhook/$', webhook),
    include('project.apps.blog.urls'),
    include('project.apps.posts.urls')
]
