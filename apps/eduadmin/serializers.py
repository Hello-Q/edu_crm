from . import models
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

class SubjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Subjects
        fields = "__all__"


class DetailedCourseSerializer(serializers.ModelSerializer):
    subjects_info = SubjectsSerializer(source='subjects', read_only=True)

    class Meta:
        model = models.Course
        fields = ['id',  'name', 'type', 'subjects', 'subjects_info']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['id',  'name']


class SubjectsCourseSerializer(WritableNestedModelSerializer):
    course = CourseSerializer(source='course_set', many=True)

    class Meta:
        model = models.Subjects
        fields = ['id', 'name', 'course']



class BaseCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Course
        fields = ['id', 'name']


class TeacherSerializer(serializers.ModelSerializer):
    teacher_name = serializers.StringRelatedField(source='user')

    class Meta:
        model = models.Teacher
        fields = ['id', 'user', 'teacher_name', 'course']


class BaseTeacherSerializer(serializers.ModelSerializer):
    nickname = serializers.StringRelatedField(source='user')

    class Meta:
        model = models.Teacher
        fields = ['id', 'nickname']


class StudentSerializer(serializers.ModelSerializer):
    birthday = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", allow_null=True)
    status = serializers.ReadOnlyField()

    class Meta:
        model = models.Student
        fields = ['id', 'name', 'tel', 'clue', 'school', 'birthday', 'sex', 'father_name', 'father_tel',
                  'mother_name', 'mother_tel', 'status']
