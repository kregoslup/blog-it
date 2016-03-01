from django.conf.urls import url
from apps.blog.views import *


urlpatterns = [
    url(r'^github/login/$', oauth_login),
    url(r'^github/login/callback/$', oauth_callback),
    url(r'^blogs/$', BlogsList.as_view()),
    url(r'^blogs/(?P<pk>[0-9]+)/$', BlogDetail.as_view()),

]
