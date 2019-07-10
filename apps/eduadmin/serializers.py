from . import models
from rest_framework import serializers


class SubjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Subjects
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    subjects_info = SubjectsSerializer(source='subjects', read_only=True)

    class Meta:
        model = models.Course
        fields = ['id',  'name', 'type', 'subjects', 'subjects_info']


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Teacher
        fields = "__all__"

