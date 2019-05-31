from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.clue import views

router = DefaultRouter()
router.register('channel-type', views.ChannelTypeViewSet)
router.register('channel', views.ChannelViewSet)
router.register('clue', views.ClueViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
