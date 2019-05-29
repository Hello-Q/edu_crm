from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.clue import views

# from rest_framework.schemas import get_schema_view
# schema_view = get_schema_view(title='Example API')
router = DefaultRouter()
router.register('channel', views.ChannelViewSet)
router.register('clue', views.ClueViewSet)
router.register('channel-type', views.ChannelTypeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('schema/', schema_view),
]
