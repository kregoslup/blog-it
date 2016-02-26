from django.conf.urls import url
from apps.blog.views import token_query

urlpatterns = [
    url(r'^sign_up/$', token_query)
]
