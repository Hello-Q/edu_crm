from django_filters import rest_framework as filters


class SourceChannelFilter(filters.FilterSet):

    class Meta:
        filter_fields = ['name']