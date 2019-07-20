from apps.sys.models import User
from rest_framework import viewsets
from . import models
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
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

    # def get_queryset(self):
    #     queryset = self.queryset
    #     teachers = []
    #     for teacher in queryset:
    #         departments = teacher.user.department.all()
    #         for department in departments:
    #             print(department.name)
    #             if department.name == '中山校区':
    #                 print(department)
    #                 teachers.append(teacher)
    #                 print(teachers)

    def list(self, request, *args, **kwargs):
        department_id = int(request.GET.get('department'))

        queryset = self.queryset
        teachers = []
        for teacher in queryset:
            departments = teacher.user.department.all()
            for department in departments:
                if department.id == department_id:
                    teachers.append(teacher)

        page = self.paginate_queryset(teachers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(teachers, many=True)
        return Response(serializer.data)




