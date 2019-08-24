# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import copy
from apps.clue import models, serializers
from apps.eduadmin.models import Teacher, Course
from utils import views
from utils.page_num import StandardResultsSetPagination
from utils.permissions import ExpandDjangoModelPermissions
from . import filters


class ChannelTypeViewSet(views.FalseDelModelViewSet):
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
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
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
    filter_backends = (DjangoFilterBackend, )
    filter_class = filters.ClueFilters

    def status_confirmation(self, request, serializer, *args):
        """确认线索状态"""
        print()
        status = serializer.validated_data.get('status')
        if status == 4 or status == 5:
            return serializer
        elif len(args[0].visit_set.all()) == 0 and status == 0:
            return serializer
        elif serializer.validated_data.get('next_time'):
            serializer.validated_data['status'] = 1
            return serializer
        else:
            detail = {
                "status": [
                    "“{}”不是合法选项。".format(status)
                ]
            }
            return detail

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 状态确认
        serializer = self.status_confirmation(request, serializer)
        if isinstance(serializer, dict):
            return Response(serializer, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # 状态确认
        serializer = self.status_confirmation(request, serializer, instance)
        if isinstance(serializer, dict):
            return Response(serializer, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class FollowRecordViewSet(views.FalseDelModelViewSet):
    """跟进记录"""
    queryset = models.FollowRecord.objects.filter(del_flag=0)
    serializer_class = serializers.FollowRecordSerializer


class VisitViewSet(views.FalseDelModelViewSet):
    """访问记录"""
    queryset = models.Visit.objects.filter(del_flag=0)
    serializer_class = serializers.VisitSerializer

    def modify_clue_status(self, serializer):
        visit_status = serializer.validated_data.get('status') or 0
        clue = serializer.validated_data['clue']
        if visit_status == 1:
            clue.status = 3
            clue.save()
        else:
            if clue.status >= 2:
                clue.status = 2
                clue.save()

    def create(self, request, *args, **kwargs):
        """选取访问时间"""
        try:
            visit_time = request.data.get('visit_time') or request.data.get('promise_visit_time')
            request.data['visit_time'] = visit_time
        except KeyError as e:
            print(e)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 调整对应线索status
        self.modify_clue_status(serializer)
        visit_status = serializer.validated_data.get('status') or 0
        clue = serializer.validated_data['clue']
        if visit_status == 1:
            clue.status = 3
            clue.save()
        else:
            clue.status = 2
            clue.save()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
            visit_time = request.data.get('visit_time') or request.data.get('promise_visit_time')
            request.data['visit_time'] = visit_time
        except KeyError as e:
            print(e)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # 判断数据变化
        serializer = self.change_in_data(serializer, instance, partial)
        # 调整对应线索status
        self.modify_clue_status(serializer)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

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
