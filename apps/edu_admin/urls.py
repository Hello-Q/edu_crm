from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()

router.register('course', views.CourseViewSet)
router.register('subjects', views.SubjectsViewSet)
router.register('teacher', views.TeacherViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
