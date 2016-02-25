from django.conf.urls import url
from apps.blog.views import ApiEndpoint

urlpatterns = [
    url(r'^sign_up/$', ApiEndpoint.as_view())
]
