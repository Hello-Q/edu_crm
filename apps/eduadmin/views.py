from apps.sys.models import User
from rest_framework import viewsets
from . import models
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
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


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        department_id = request.GET.get('department')
        if department_id:
            department_id = int(department_id)
            department = Department.objects.filter(id=department_id)
            if not department:
                data = {
                    'department': "选择一个有效的选项： 该选择不在可用的选项中。"
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            tea_queryset = self.queryset
            queryset = []
            for teacher in tea_queryset:
                departments = teacher.user.department.all()
                for department in departments:
                    if department.id == department_id:
                        queryset.append(teacher)
        else:
            queryset = self.queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




