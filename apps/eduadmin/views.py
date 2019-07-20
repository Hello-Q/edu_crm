from apps.sys.models import User
from rest_framework import viewsets
from . import models
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.query import QuerySet
from rest_framework.response import Response
from apps.sys.models import Department
from rest_framework import status
# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('subjects',)


class SubjectsViewSet(viewsets.ModelViewSet):
    queryset = models.Subjects.objects.all()
    serializer_class = serializers.SubjectsSerializer
    pagination_class = None


from django_filters import rest_framework as filters

class SourceChannelFilter(filters.FilterSet):


    class Meta:
        model = User
        fields = ['department']



class TeacherViewSet(viewsets.ModelViewSet):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer
    pagination_class = None
    # filter_backends = (DjangoFilterBackend, )
    # filterset_class = SourceChannelFilter

    def get_queryset(self):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            department_id = self.request.GET.get("department")

            if department_id:
                # if not Department.objects.filter(id=department_id):
                #     print("department")
                #     data = {
                #             'department': "选择一个有效的选项： 该选择不在可用的选项中。"
                #             }
                #     return None
                queryset = queryset.all().filter(user__department=department_id)
            else:
                queryset = queryset.all()
        return queryset
