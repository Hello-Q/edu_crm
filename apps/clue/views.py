# Create your views here.
from rest_framework import viewsets, status
from rest_framework.views import APIView
from apps.clue import models
from apps.clue import serializers
from rest_framework import generics
from utils.page_num import StandardResultsSetPagination

from rest_framework.views import APIView
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
from rest_framework.permissions import IsAuthenticated
from utils import views
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError


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
            try:
            self.perform_create(serializer)
        except Exception as e:
            tel = request.data.get('tel')
            clue = models.Clue.objects.get(tel=tel)
            create_user = clue.creator.nickname
            try:
                follow_up_person = clue.follow_up_person.nickname
            except AttributeError:
                detail = {
                    'detail': "线索中联系方式重复, 线索创建人为{0}".format(create_user)
                }
                return Response(detail, status=status.HTTP_400_BAD_REQUEST)
            detail = {
                'detail': "线索中联系方式重复, 线索创建人为{0}, 当前跟进人为{1}".format(create_user, follow_up_person)
            }
            return Response(detail, status=status.HTTP_400_BAD_REQUEST)
    """
    queryset = models.Clue.objects.all()
    serializer_class = serializers.ClueSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        clue_status = request.data.get('status')
        next_time = request.data.get('next_time')
        print(next_time == '')
        # if not clue_status or clue_status in ['4', '5']:
        #     pass

        if next_time != '':
            serializer.validated_data['status'] = 2

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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

    def create(self, request, *args, **kwargs):
        try:
            visit_time = request.data['visit_time']
            if visit_time:
                request.data['visit_time'] = visit_time
            else:
                request.data['visit_time'] = request.data['promise_visit_time']
        except KeyError:
            request.data['visit_time'] = request.data['promise_visit_time']

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ClueDuplicateCheck(APIView):
    """线索查重"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        tel = request.query_params.get('tel')
        if not tel:
            detail = {
                'detail': '请输入客户电话'
            }
            return Response(detail, status=status.HTTP_400_BAD_REQUEST)
        try:
            clue = models.Clue.objects.get(tel=tel)
        except models.Clue.DoesNotExist:
            detail = {
                'detail': '没有发现重复'
            }
            return Response(detail)
        creator = clue.creator.nickname
        detail = {
            'detail': '发现重复线索，创建人为{}'.format(creator)
        }
        return Response(detail)
