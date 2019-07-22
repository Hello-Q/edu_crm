# Create your views here.
from django.contrib.auth.models import Permission, Group
from jwt import exceptions
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework_jwt.views import ObtainJSONWebToken, VerifyJSONWebToken, RefreshJSONWebToken
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser, FileUploadParser
from django_filters.rest_framework import DjangoFilterBackend
from apps.sys import models
from apps.sys import serializers
from utils import views


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    操作公司数据
    """
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    部门数据
    """
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('type', )


class UserViewSet(views.FalseDelModelViewSet):
    """
    对系统用户进行数据操作
    """
    queryset = models.User.objects.filter(del_flag__exact=False)
    serializer_class = serializers.UserSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('role', 'department', 'role__name')


# class UserBaseView(mixins.ListModelMixin,
#                    viewsets.GenericViewSet):
#     """
#     基础用户信息
#     """
#     queryset = models.User.objects.all()


class PermissionViewSet(viewsets.ModelViewSet):
    """
    权限列表
    """
    queryset = Permission.objects.all()
    serializer_class = serializers.PermissionSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    用户组
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class RoleViewSet(viewsets.ModelViewSet):
    """
    角色
    """
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    """资源"""
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer


# class