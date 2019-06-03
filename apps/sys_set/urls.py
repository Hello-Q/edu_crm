from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()

router.register('user', views.User)
router.register('organization', views.OrganizationViewSet)
router.register('department', views.DepartmentViewSet)
# router.register('personal-info', views.PersonalInfo)



urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('token-verify/', views.TokenVerify.as_view()),
    path('token-refresh/', views.TokenRefresh.as_view()),
    path('personal-info/', views.PersonalInfo.as_view()),
    # path('test/', views.test),
    path('', include(router.urls)),
]
