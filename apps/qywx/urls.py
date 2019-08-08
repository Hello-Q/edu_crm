
from django.urls import path, include
from . import views

# router.register('base-teacher', views.BaseTeacher)


urlpatterns = [
    path('verify-url/', views.CallbackService.as_view()),
    path('follow-user/', views.FollowUseList.as_view()),
    path('external-contact/', views.ExternalContactList.as_view()),
    path('external-contact-detail/', views.ExternalContactDetail.as_view()),
]
