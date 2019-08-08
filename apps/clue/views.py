# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import copy
from apps.clue import models, serializers
from apps.eduadmin.models import Teacher, Course
from apps.sys.models import Department, User
from utils import views
from utils.page_num import StandardResultsSetPagination
from utils.permissions import ExpandDjangoModelPermissions


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
    # try:
    #     self.perform_create(serializer)
    # except Exception as e:
    #     tel = request.data.get('tel')
    #     clue = models.Clue.objects.get(tel=tel)
    #     create_user = clue.creator.nickname
    #     try:
    #         follow_up_person = clue.follow_up_person.nickname
    #     except AttributeError:
    #         detail = {
    #             'detail': "线索中联系方式重复, 线索创建人为{0}".format(create_user)
    #         }
    #         return Response(detail, status=status.HTTP_400_BAD_REQUEST)
    #     detail = {
    #         'detail': "线索中联系方式重复, 线索创建人为{0}, 当前跟进人为{1}".format(create_user, follow_up_person)
    #     }
    #     return Response(detail, status=status.HTTP_400_BAD_REQUEST)
    queryset = models.Clue.objects.all()
    serializer_class = serializers.ClueSerializer
    pagination_class = StandardResultsSetPagination



    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print(queryset.filter(creator=request.user))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        clue_status = request.data.get('status')
        next_time = request.data.get('next_time')
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

    def change_in_data(self, serializer, instance, partial):
        # 判断约访是否发生变化
        # 提取老数据
        old = copy.deepcopy(self.get_serializer(instance).data)
        new = copy.deepcopy(serializer.initial_data)
        if new['status'] != 0:
            return serializer
        for key in ['id', 'clue', 'status', 'revocatory_reason']:
            old.pop(key, 404)
            new.pop(key, 404)
        if old == new:
            return serializer
        # try:
        revocatory_reason = str()
        if old['type'] != new['type']:
            for old_id in models.Visit.VISIT_TYPE:
                if old_id[0] == old['type']:
                    old_type = old_id[1]
            for new_id in models.Visit.VISIT_TYPE:
                if new_id[0] == new['type']:
                    new_type = new_id[1]

            revocatory_reason += '客户约访类型由{0}改为{1},'.format(old_type, new_type)
        if old['visit_time'] != new['visit_time']:
            revocatory_reason += '客户约访时间由{0}改为{1},'.format(old['visit_time'], new['visit_time'])

        if old['ordered_teacher'] != new['ordered_teacher']:
            old_tea = old['ordered_teacher']
            new_tea = new['ordered_teacher']
            if old_tea and new_tea:
                revocatory_reason += '客户试听老师由{0}改为{1},'.format(Teacher.objects.get(id=old_tea).user.nickname,
                                                               Teacher.objects.get(id=new_tea).user.nickname)
            if old_tea and not new_tea:
                revocatory_reason += '客户取消了试听老师{},'.format(Teacher.objects.get(id=old_tea).user.nickname)
            if not old_tea and new_tea:
                revocatory_reason += '客户添加试听老师{},'.format(Teacher.objects.get(id=new_tea).user.nickname)

        if old['ordered_course'] != new['ordered_course']:
            old_course = old['ordered_course']
            new_course = new['ordered_course']

            if old_course and new_course:
                revocatory_reason += '客户试听课程由{0}改为{1},'.format(Course.objects.get(id=old_course).name,
                                                               Course.objects.get(id=new_course).name)
            if old_course and not new_course:
                revocatory_reason += '客户取消了试听课程{},'.format(Course.objects.get(id=old_course).name)
            if not old_course and new_course:
                revocatory_reason += '客户添加试听课程{},'.format(Course.objects.get(id=new_course).name)
        # except Exception as e:
        #     print(e)
        old_data = self.get_serializer(instance).data
        old_data['revocatory_reason'] = revocatory_reason
        old_data['status'] = 3
        old_serializer = self.get_serializer(instance, data=old_data, partial=partial)
        new_serializer = self.get_serializer(data=serializer.initial_data)
        new_serializer.is_valid()
        self.perform_create(new_serializer)
        return old_serializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old = self.get_serializer(instance).data
        if old['status'] != 0:
            detail = {
                'detail': '该访问已结束,无法再次修改'
            }
            return Response(detail, status=status.HTTP_404_NOT_FOUND)
        try:
            visit_time = request.data['visit_time']
            if visit_time:
                request.data['visit_time'] = visit_time
            else:
                request.data['visit_time'] = request.data['promise_visit_time']
        except KeyError:
            pass
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # 判断数据变化
        serializer = self.change_in_data(serializer, instance, partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


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
