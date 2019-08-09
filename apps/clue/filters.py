from django_filters import rest_framework as filters
from apps.clue import models
from .models import ChannelType


class SourceChannelFilter(filters.FilterSet):

    class Meta:
        model = models.Channel
        fields = ['name']


class ClueFilters(filters.FilterSet):
    """线索过滤器"""

    channel_type = filters.CharFilter(method="get_channel_type")
    channel = filters.CharFilter(method="get_channel")
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    tel = filters.CharFilter(field_name='tel', lookup_expr='icontains')
    consult_date_min = filters.DateFilter(field_name='consult_date', lookup_expr='gte')
    consult_date_max = filters.DateFilter(field_name='consult_date', lookup_expr='lte')
    next_time_min = filters.DateFilter(field_name='next_time', lookup_expr='gte')
    next_time_max = filters.DateFilter(field_name='next_time', lookup_expr='lte')

    def get_channel_type(self, queryset, name, value):
        queryset = queryset.filter(channel__type=value)
        return queryset

    def get_channel(self, queryset, name, value):
        channel_lsit = list(value)
        queryset = queryset.filter(channel__in=channel_lsit)
        return queryset

    class Meta:
        model = models.Clue
        fields = ['intended_school', 'status', 'is_importance']
