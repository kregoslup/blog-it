from rest_framework import routers

from project.apps.posts.views import PostViewSet

router = routers.SimpleRouter()
router.register(r'posts', PostViewSet)

urlpatterns = []

urlpatterns += router.urls
