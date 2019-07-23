from django_filters import rest_framework as filters
from . import models


class UsersFilter(filters.FilterSet):
    role = filters.NumberFilter(field_name='groups', lookup_expr='exact')
    role_name = filters.CharFilter(field_name='groups', lookup_expr='exact')

    class Meta:
        model = models.User
        fields = ['role', 'department', 'role_name']
