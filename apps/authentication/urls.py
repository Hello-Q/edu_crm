
from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('token-verify/', views.TokenVerify.as_view()),
    path('token-refresh/', views.TokenRefresh.as_view()),
    path('personal-info/', views.PersonalInfo.as_view()),
    # path('test/', views.test),
]
