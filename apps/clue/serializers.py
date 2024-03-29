import time
from rest_framework import serializers
from apps.clue import models
from apps.sys import serializers as sys_serializers
from apps.eduadmin import serializers as eduadmin_serializers


class ChannelTypeSerializer(serializers.HyperlinkedModelSerializer):
    """渠道类型"""
    class Meta:
        model = models.ChannelType
        fields = ['id', 'name']


class BaseChannelTypeSerializer(serializers.ModelSerializer):
    """基础渠道类型"""
    class Meta:
        model = models.ChannelType
        fields = ['id', 'name',  'remark']


class ChannelSerializer(serializers.ModelSerializer):
    """渠道"""
    class Meta:
        model = models.Channel
        fields = ['id', 'name', 'type', 'remark']


class BaseChannelSerializer(serializers.ModelSerializer):
    """基础渠道"""
    type_info = BaseChannelTypeSerializer(source='type')

    class Meta:
        model = models.Channel
        fields = ['id', 'name', 'type', 'type_info']


class VisitSerializer(serializers.ModelSerializer):

    visit_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = models.Visit
        fields = ['id', 'clue', 'type', 'visit_time', 'ordered_teacher',
                  'ordered_course', 'status', 'revocatory_reason']


class StrVisitSerializer(serializers.ModelSerializer):
    ordered_teacher_name = serializers.StringRelatedField(source='ordered_teacher', read_only=True)
    ordered_course_name = serializers.StringRelatedField(source='ordered_course', read_only=True)
    visit_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = models.Visit
        fields = ['id', 'type', 'visit_time', 'ordered_teacher', 'ordered_teacher_name',
                  'ordered_course', 'ordered_course_name', 'status', 'revocatory_reason', 'remark']


class FollowRecordSerializer(serializers.ModelSerializer):
    creator_name = serializers.StringRelatedField(source='creator', read_only=True)
    follow_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    clue_status = serializers.ReadOnlyField()

    class Meta:
        model = models.FollowRecord
        fields = ['id', 'follow_time', 'clue', 'clue_status', 'content', 'creator_name']


class FailingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FailingType
        fields = ['id', 'type_name']


class ClueSerializer(serializers.ModelSerializer):
    channel_info = BaseChannelSerializer(source='channel', read_only=True)
    intended_course_info = eduadmin_serializers.CourseSerializer(source='intended_course', read_only=True, many=True)
    intended_school_info = sys_serializers.DepartmentBaseSerializer(source='intended_school', read_only=True)
    follow_up_person_info = sys_serializers.BaseUserSerializer(source='follow_up_person', read_only=True)
    # plan_school_name = serializers.StringRelatedField(source='plan_school')
    # plan_reception_name = serializers.StringRelatedField(source='plan_reception')
    # plan_teacher_name = serializers.StringRelatedField(source='plan_teacher')
    # plan_course_name = serializers.StringRelatedField(source='plan_course')
    creator = serializers.StringRelatedField(read_only=True)
    Visit = StrVisitSerializer(source='visit_set', many=True, read_only=True)
    follow_info = FollowRecordSerializer(source='followrecord_set', many=True, read_only=True)
    next_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", allow_null=True)
    failing_type_info = FailingTypeSerializer(source='failing_type', read_only=True)
    enroll_course_name = serializers.StringRelatedField(source='enroll_course', read_only=True, many=True)


    class Meta:
        model = models.Clue
        # exclude = HIDE_FIELD

        fields = ['id', 'channel', 'channel_info', 'name', 'tel', 'age', 'sex', 'address', 'is_importance',
                  'consult_date', 'intended_course', 'intended_course_info', 'intended_school', 'intended_school_info',
                  'follow_up_person', 'follow_up_person_info', 'creator', 'status', 'next_time', 'enroll_course',
                  'enroll_course_name', 'enroll_date', 'enroll_sum', 'class_hour',
                  'failing_type', 'failing_type_info', 'failing_cause', 'Visit', 'follow_info', 'remark']



