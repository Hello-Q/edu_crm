from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()

router.register('user', views.User)
# router.register('personal-info', views.PersonalInfo)



urlpatterns = [
    path('login/', views.Login.as_view()),
    path('token-verify/', views.TokenVerify.as_view()),
    path('token-refresh/', views.TokenRefresh.as_view()),
    path('personal-info/', views.PersonalInfo.as_view()),
    # path('test/', views.test),
    path('', include(router.urls)),
]
