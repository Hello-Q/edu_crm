from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.User)


urlpatterns = [
    path('login/', views.Login.as_view()),  # 请求token
    path('token-verify/', views.TokenVerify.as_view()),  # 验证token
    path('token-refresh/', views.TokenRefresh.as_view()),  # 刷新token到期时间
    path('user-info/', views.GetUserInfo.as_view()),
    path('', include(router.urls)),
    # path('user/', views.CreateUser),
]
