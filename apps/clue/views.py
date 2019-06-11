# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from apps.clue import models
from apps.clue import serializers
from rest_framework import generics
from utils.page_num import StandardResultsSetPagination

import coreapi
import coreschema
from rest_framework.schemas import ManualSchema, AutoSchema
from rest_framework.response import Response
from collections import OrderedDict
from django_filters.rest_framework import DjangoFilterBackend
from apps.clue import filters
from rest_framework import permissions
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, DjangoModelPermissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        print(obj)
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # Instance must have an attribute named `owner`.
        return False

class ChannelTypeViewSet(viewsets.ModelViewSet):
    """
    渠道分类
    """
    queryset = models.ChannelType.objects.all()
    serializer_class = serializers.ChannelTypeSerializer

    permission_classes = (DjangoModelPermissions,)

class ChannelViewSet(viewsets.ModelViewSet):
    """
    渠道类型
    """
    queryset = models.Channel.objects.all()
    serializer_class = serializers.ChannelSerializer
    filter_backends = (DjangoFilterBackend,)


class ClueViewSet(viewsets.ModelViewSet):
    """
    线索资源
    """
    queryset = models.Clue.objects.all()
    serializer_class = serializers.ClueSerializer
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        # 自动保存创建人和更新人
        serializer.save(operator=self.request.user, creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save(operator=self.request.user)
