from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()

router.register('course', views.CourseViewSet)
router.register('subjects', views.SubjectsViewSet)
router.register('subjects-course', views.SubjectsCourseViewSet)
router.register('teacher', views.TeacherViewSet)
router.register('student', views.StudentViewSet)
# router.register('base-teacher', views.BaseTeacher)


urlpatterns = [
    path('', include(router.urls)),
]
