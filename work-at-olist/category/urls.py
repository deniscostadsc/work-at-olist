from django.conf.urls import url, include

from rest_framework import routers

from .views import ChannelViewSet

router = routers.DefaultRouter()
router.register(r'channels', ChannelViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
