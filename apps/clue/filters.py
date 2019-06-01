from django_filters import rest_framework as filters
from apps.clue import models


class SourceChannelFilter(filters.FilterSet):

    class Meta:
        model = models.Channel
        fields = ['cha_name']
