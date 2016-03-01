from django.conf.urls import url, include
from apps.blog.views import profile_info

urlpatterns = [
    url(r'^profile/$', profile_info),
    url(r'^api/', include('apps.blog.urls')),
]
