from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.User)

urlpatterns = [
    path('login/', views.Login.as_view()),  # 请求token
    path('token-verify/', views.TokenVerify.as_view()),  # 验证token
    path('token-refresh/', views.TokenRefresh.as_view()),  # 刷新token到期时间
    path('personal-info/', views.PersonalInfo.as_view()),  # 获取用户个人信息
    path('', include(router.urls)),
]
