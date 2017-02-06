from django.conf.urls import url
from rest_framework import routers
from djoser import views as djoser

from project.apps.blog.views import BlogsViewSet

router = routers.SimpleRouter()
router.register(r'blogs', BlogsViewSet)

urlpatterns = [
    url(r'^auth/login', djoser.LoginView.as_view()),
    url(r'^auth/register', djoser.RegistrationView.as_view()),
    url(r'^auth/login', djoser.LogoutView.as_view()),
]

urlpatterns += router.urls
