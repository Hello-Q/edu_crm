# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from apps.clue import models
from apps.clue import serializers
from rest_framework import generics
from util.page_num import StandardResultsSetPagination

import coreapi
import coreschema
from rest_framework.schemas import ManualSchema, AutoSchema
from rest_framework.response import Response
from collections import OrderedDict
from django_filters.rest_framework import DjangoFilterBackend
from apps.clue import filters


class SourceChannelViewSet(viewsets.ModelViewSet):
    """
    渠道类型
    list: 列出渠道类型，未传参讲返回所有渠道，渠道筛选时，可以先请求一级分类，然后
    """
    queryset = models.Channel.objects.all()
    serializer_class = serializers.SourceChannelSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.SourceChannelFilter


class ClueViewSet(viewsets.ModelViewSet):
    queryset = models.Clue.objects.all()
    serializer_class = serializers.ClueSerializer
    pagination_class = StandardResultsSetPagination



