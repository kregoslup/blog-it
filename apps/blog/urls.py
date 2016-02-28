from django.conf.urls import url
from apps.blog.views import oauth_login, oauth_callback

urlpatterns = [
    url(r'^/login$', oauth_login),
    url(r'^login/callback$/', oauth_callback),
]
