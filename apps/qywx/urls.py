
from django.urls import path, include
from . import views

# router.register('base-teacher', views.BaseTeacher)


urlpatterns = [
    path('verify_url/', views.CallbackService.as_view()),
]
