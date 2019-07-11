from rest_framework import serializers
from apps.clue import models
from edu_crm.settings import HIDE_FIELD
from apps.sys import serializers as sys_serializers
from apps.eduadmin import serializers as eduadmin_serializers


class ChannelTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.ChannelType
        fields = "__all__"


class BaseChannelTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ChannelType
        fields = ['id', 'name']


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Channel
        exclude = HIDE_FIELD


class BaseChannelSerializer(serializers.ModelSerializer):
    channel_type_info = BaseChannelTypeSerializer(source='channel_type', read_only=True)

    class Meta:
        model = models.Channel
        fields = ['channel_id', 'channel_name', 'channel_type', 'channel_type_info']


class StrVisitSerializer(serializers.ModelSerializer):
    school_name = serializers.StringRelatedField(source='school', read_only=True)
    ordered_reception_name = serializers.StringRelatedField(source='ordered_reception', read_only=True)
    ordered_teacher_name = serializers.StringRelatedField(source='ordered_teacher', read_only=True)
    ordered_course_name = serializers.StringRelatedField(source='ordered_course', read_only=True)

    class Meta:
        model = models.Visit
        fields = ['id', 'type', 'date', 'time', 'school_name', 'ordered_reception_name', 'ordered_teacher_name',
                  'ordered_course', 'ordered_course_name', 'is_visit', 'remark']


class ClueSerializer(serializers.ModelSerializer):
    channel_info = BaseChannelSerializer(source='channel', read_only=True)
    intended_course_info = eduadmin_serializers.CourseSerializer(source='intended_course', read_only=True, many=True)
    intended_school_info = sys_serializers.DepartmentBaseSerializer(source='intended_school', read_only=True, many=True)
    follow_up_person_info = sys_serializers.BaseUserSerializer(source='follow_up_person', read_only=True)
    # plan_school_name = serializers.StringRelatedField(source='plan_school')
    # plan_reception_name = serializers.StringRelatedField(source='plan_reception')
    # plan_teacher_name = serializers.StringRelatedField(source='plan_teacher')
    # plan_course_name = serializers.StringRelatedField(source='plan_course')
    Visit = StrVisitSerializer(source='visit_set', many=True, read_only=True)

    class Meta:
        model = models.Clue
        # exclude = HIDE_FIELD

        fields = ['id', 'channel', 'channel_info', 'name', 'tel', 'age', 'sex', 'address', 'input_time',
                  'intended_course', 'intended_course_info', 'intended_school', 'intended_school_info',
                  'follow_up_person', 'follow_up_person_info', 'Visit', 'remark']

    # def update(self, instance, validated_data):