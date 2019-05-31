# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.clue import models
from apps.clue import serializers
from util.page_num import StandardResultsSetPagination


class ChannelTypeViewSet(viewsets.ModelViewSet):
    """
    渠道分类
    """
    queryset = models.ChannelType.objects.all()
    serializer_class = serializers.ChannelTypeSerializer


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
