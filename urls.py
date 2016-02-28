from django.conf.urls import url, include
from apps.blog.views import profile_info

urlpatterns = [
    url(r'^$',),
    url(r'^profile/$', profile_info),
    url(r'^api/github/$', include('apps.blog.urls')),
]
