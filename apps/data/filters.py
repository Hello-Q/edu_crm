from django_filters import rest_framework as filters
from apps.clue.models import Clue


class FunnelFilter(filters.FilterSet):
    channel_type = filters.CharFilter(method="get_channel_type")

    class Meta:
        model = Clue
        fields = ['channel', 'intended_school', 'follow_up_person']

    def get_channel_type(self, queryset, name, value):
        queryset = queryset.filter(channel__type=value)
        return queryset
