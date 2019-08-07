
from django.urls import path, include
from . import views

# router.register('base-teacher', views.BaseTeacher)


urlpatterns = [
    path('verify-url/', views.CallbackService.as_view()),
    path('get-follow-use-list/', views.GetFollowUseList.as_view()),
]
