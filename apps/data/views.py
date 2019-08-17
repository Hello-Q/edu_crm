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

class Funnel(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Clue.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.FunnelFilter
    data_permission_class = DataPermission

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(del_flag=False)
        """根据数据权限过滤queryset"""
        if not request.user.is_superuser:
            data_permission = self.data_permission_class()
            queryset = data_permission.get_perm_queryset(queryset.model, request, queryset)

        queryset = (queryset.aggregate(
            clue_num_proportion=Count('id', output_field=FloatField())/Count('id', output_field=FloatField()),
            clue_num_count=Count('id'),
            contact_again_proportion=(Count('id', filter=Q(status=1) | Q(status=2) | Q(status=3) | Q(status=5), output_field=FloatField()))/Count('id', output_field=FloatField()),
            contact_again_count=Count('id', filter=Q(status=1) | Q(status=2) | Q(status=3) | Q(status=5)),
            ordered_visit_proportion=(Count('id', filter=Q(status=2) | Q(status=3) | Q(status=5), output_field=FloatField()))/Count('id', output_field=FloatField()),
            ordered_visit_count=Count('id', filter=Q(status=2) | Q(status=3) | Q(status=5)),
            visit_proportion=((Count('id', filter=Q(status=3) | Q(status=5), output_field=FloatField()))/Count('id', output_field=FloatField())),
            visit_proportion_count=Count('id', filter=Q(status=3) | Q(status=5)),
            enroll_proportion=(Count('id', filter=Q(status=5), output_field=FloatField()))/Count('id', output_field=FloatField()),
            enroll_proportion_count=Count('id', filter=Q(status=5))
        ))

        # 调整数据格式
        for key in queryset:
            if isinstance(queryset[key], float):
                queryset[key] = round(queryset[key]*100, 2)
        # queryset['intended_school'] = intended_school.name
        return Response(queryset)

