from apps.sys.models import User
from rest_framework import viewsets
from . import models
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.query import QuerySet
from rest_framework.response import Response
from apps.sys.models import Department
from rest_framework import status
from utils.views import FalseDelModelViewSet
from . import filters
# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.filter(del_flag__exact=False)
    serializer_class = serializers.DetailedCourseSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('subjects',)


class SubjectsViewSet(viewsets.ModelViewSet):
    queryset = models.Subjects.objects.filter(del_flag__exact=False)
    serializer_class = serializers.SubjectsSerializer
    pagination_class = None


class SubjectsCourseViewSet(viewsets.ModelViewSet):
    queryset = models.Subjects.objects.filter(del_flag__exact=False)
    serializer_class = serializers.SubjectsCourseSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id',)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = models.Teacher.objects.filter(del_flag__exact=False)
    serializer_class = serializers.TeacherSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )
    # filterset_fields = ('user__department',)
    filterset_class = filters.TeacherFilter


class StudentViewSet(FalseDelModelViewSet):
    queryset = models.Student.objects.filter(del_flag__exact=False)
    serializer_class = serializers.StudentSerializer

