from django.conf.urls import url, include
from apps.blog.views import profile

urlpatterns = [
    url(r'^$',),
    url(r'^profile/$', profile),
    url(r'^api/github/$', include('apps.blog.urls')),
]
