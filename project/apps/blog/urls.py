from rest_framework import routers

from project.apps.blog.views import BlogsViewSet

router = routers.SimpleRouter()
router.register(r'blogs', BlogsViewSet)

urlpatterns = []

urlpatterns += router.urls
