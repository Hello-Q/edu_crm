from . import models
from rest_framework import serializers


class CourseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Course
        fields = "__all__"


class SubjectsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Subjects
        fields = "__all__"


class TeacherSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Teacher
        fields = "__all__"

