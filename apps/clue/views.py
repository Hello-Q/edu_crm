# Create your views here.
from rest_framework import viewsets, status
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
from utils.permissions import ExpandDjangoModelPermissions, DjangoObjectPermissions
from utils import views
from django.shortcuts import get_object_or_404

class ChannelTypeViewSet(viewsets.ModelViewSet):
    """
    渠道分类
    """
    queryset = models.ChannelType.objects.all()
    serializer_class = serializers.ChannelTypeSerializer
    pagination_class = None
    permission_classes = (ExpandDjangoModelPermissions,)


class ChannelViewSet(viewsets.ModelViewSet):
    """
    渠道类型
    """
    queryset = models.Channel.objects.all()
    serializer_class = serializers.ChannelSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_fields = ('type',)


class ClueViewSet(views.FalseDelModelViewSet):
    """
    线索资源
    """
    queryset = models.Clue.objects.all()
    serializer_class = serializers.ClueSerializer
    pagination_class = StandardResultsSetPagination


class FollowRecordViewSet(views.FalseDelModelViewSet):
    """跟进记录"""
    queryset = models.FollowRecord.objects.filter(del_flag=0)
    serializer_class = serializers.FollowRecordSerializer

    def perform_create(self, serializer):
        # 获取线索状态并保存
        clue_id = serializer.validated_data['clue'].id
        status_id = models.Clue.objects.get(id=clue_id).status
        serializer.validated_data['clue_status'] = models.Clue.STATUS[status_id][1]
        # 自动保存创建人和更新人
        serializer.save(operator=self.request.user, creator=self.request.user)


class VisitViewSet(views.FalseDelModelViewSet):
    """访问记录"""
    queryset = models.Visit.objects.filter(del_flag=0)
    serializer_class = serializers.VisitSerializer




