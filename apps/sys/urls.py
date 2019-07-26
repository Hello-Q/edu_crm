from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()

router.register('user', views.UserViewSet)
router.register('organization', views.OrganizationViewSet)
router.register('department', views.DepartmentViewSet)
router.register('permission', views.PermissionViewSet)
router.register('role', views.RoleViewSet)
router.register('resource', views.ResourceViewSet)
# router.register('head-pic', views.HeadPortrait)
# router.register('personal-info', views.PersonalInfo)

urlpatterns = [
    # path('test/', views.test),
    path('', include(router.urls)),
]
