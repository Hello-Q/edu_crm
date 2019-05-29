from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.clue import views

# from rest_framework.schemas import get_schema_view
# schema_view = get_schema_view(title='Example API')
router = DefaultRouter()
router.register('channel', views.SourceChannelViewSet)
router.register('clue', views.ClueViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('schema/', schema_view),
]
