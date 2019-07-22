from django_filters import rest_framework as filters
from . import models


class TeacherFilter(filters.FilterSet):
    department = filters.NumberFilter(field_name='user__department', lookup_expr='exact')

    class Meta:
        model = models.Teacher
        fields = ['department']
