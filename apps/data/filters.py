from django_filters import rest_framework as filters
from apps.clue.models import Clue


class FunnelFilter(filters.FilterSet):
    channel_type = filters.CharFilter(method="get_channel_type")
    consult_date_min = filters.DateFilter(field_name='consult_date', lookup_expr='gte')
    consult_date_max = filters.DateFilter(field_name='consult_date', lookup_expr='lte')

    class Meta:
        model = Clue
        fields = ['channel', 'intended_school', 'follow_up_person']

    def get_channel_type(self, queryset, name, value):
        queryset = queryset.filter(channel__type=value)
        return queryset


class ConversionFilter(filters.FilterSet):
    channel_type = filters.CharFilter(method="get_channel_type")
    consult_date_min = filters.DateFilter(field_name='consult_date', lookup_expr='gte')
    consult_date_max = filters.DateFilter(field_name='consult_date', lookup_expr='lte')

    class Meta:
        model = Clue
        fields = ['channel']

    def get_channel_type(self, queryset, name, value):
        queryset = queryset.filter(channel__type=value)
        return queryset



