from django.shortcuts import render
from rest_framework.generics import ListAPIView
# Create your views here.
from apps.clue.models import Clue
from django.db.models import Sum, Count, FloatField, Avg, DecimalField, BooleanField, Q
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from django.db.models import IntegerField
from apps.sys.models import Department
from django.utils.datastructures import MultiValueDictKeyError
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from rest_framework import viewsets
from . import filters
from utils.permissions import DataPermission


class DataView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    data_permission_class = DataPermission

    def filter_data_to_perm(self, queryset, request):
        if not request.user.is_superuser:
            data_permission = self.data_permission_class()
            queryset = data_permission.get_perm_queryset(queryset.model, request, queryset)

        return queryset


class FunnelView(DataView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Clue.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.FunnelFilter
    data_permission_class = DataPermission

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(del_flag=False)
        """根据数据权限过滤queryset"""
        queryset = self.filter_data_to_perm(queryset, request)

        queryset = queryset.aggregate(
            clue_num_proportion=Count('id', output_field=FloatField())/Count('id', output_field=FloatField()),
            clue_num_count=Count('id'),
            contact_again_proportion=(Count('id', filter=Q(status=1) | Q(status=2) | Q(status=3) | Q(status=5), output_field=FloatField()))/Count('id', output_field=FloatField()),
            contact_again_count=Count('id', filter=Q(status=1) | Q(status=2) | Q(status=3) | Q(status=5)),
            ordered_visit_proportion=(Count('id', filter=Q(status=2) | Q(status=3) | Q(status=5), output_field=FloatField()))/Count('id', output_field=FloatField()),
            ordered_visit_count=Count('id', filter=Q(status=2) | Q(status=3) | Q(status=5)),
            visit_proportion=(Count('id', filter=Q(status=3) | Q(status=5), output_field=FloatField())/Count('id', output_field=FloatField())),
            visit_proportion_count=Count('id', filter=Q(status=3) | Q(status=5)),
            enroll_proportion=(Count('id', filter=Q(status=5), output_field=FloatField()))/Count('id', output_field=FloatField()),
            enroll_proportion_count=Count('id', filter=Q(status=5))
        )

        # 调整数据格式
        for key in queryset:
            if isinstance(queryset[key], float):
                queryset[key] = round(queryset[key]*100, 2)
        return Response(queryset)


class ConversionView(DataView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Clue.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.ConversionFilter
    data_permission_class = DataPermission

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(del_flag=False)
        """根据数据权限过滤queryset"""
        queryset = self.filter_data_to_perm(queryset, request)

        queryset = queryset.values('intended_school', 'intended_school__name').annotate(
            clue_num_count=Count('id'),
            visit_proportion_count=Count('id', filter=Q(status=3) | Q(status=5)),
            visit_rate=(Count('id', filter=Q(status=3) | Q(status=5), output_field=FloatField())/Count('id', output_field=FloatField())),
            enroll_proportion_count=Count('id', filter=Q(status=5)),
            enroll_rate=(Count('id', filter=Q(status=5), output_field=FloatField()))/Count('id', output_field=FloatField()),

        ).order_by()

        # 调整格式
        queryset = list(queryset)
        for i, school in enumerate(queryset):
            school['visit_rate'] = round(school['visit_rate']*100, 2)
            school['enroll_rate'] = round(school['enroll_rate']*100, 2)
            queryset[i] = school

        return Response(queryset)


class SummarizedView(DataView):

    queryset = Clue.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(del_flag=False)
        """根据数据权限过滤queryset"""
        queryset = self.filter_data_to_perm(queryset, request)
        """"""
        if request.query_params.get('group_by') == 'follow_up_person':
            queryset = queryset.values('intended_school', 'intended_school__name', 'follow_up_person', 'follow_up_person__nickname')
        elif request.query_params.get('group_by') == 'intended_school':
            queryset = queryset.values('intended_school', 'intended_school__name')
        else:
            detail = {
                'detail': '请指定正确的数据分组方式'
            }
            return Response(detail, status=status.HTTP_400_BAD_REQUEST)

        queryset = queryset.annotate(
            clue_num_count=Count('id'),

            contact_again_count=Count('id', filter=Q(status=1) | Q(status=2) | Q(status=3) | Q(status=5)),

            ordered_visit_count=Count('id', filter=Q(status=2) | Q(status=3) | Q(status=5)),

            visit_proportion_count=Count('id', filter=Q(status=3) | Q(status=5)),

            enroll_proportion_count=Count('id', filter=Q(status=5)),

            fail_count=Count('id', filter=Q(status=4)),

            enroll_sum=Sum('enroll_sum', filter=Q(status=5))

        ).order_by('-enroll_sum')



        return Response(queryset)

