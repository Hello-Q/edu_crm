from rest_framework import serializers
from apps.clue import models
from edu_crm.settings import HIDE_FIELD
from apps.sys.serializers import DepartmentBaseSerializer


class ChannelTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.ChannelType
        fields = "__all__"


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Channel
        exclude = HIDE_FIELD


class BaseChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Channel
        fields = ['channel_id', 'channel_name']


class VisitSerializer(serializers.ModelSerializer):
    visit_school = DepartmentBaseSerializer()

    class Meta:
        model = models.Visit
        exclude = HIDE_FIELD


class ClueSerializer(serializers.ModelSerializer):
    channel = BaseChannelSerializer()
    follow_up_person_name = serializers.StringRelatedField(source='follow_up_person')
    intended_course_name = serializers.StringRelatedField(source='intended_course', read_only=True, many=True)
    intended_school_name = serializers.StringRelatedField(source='intended_school', read_only=True, many=True)
    plan_school_name = serializers.StringRelatedField(source='plan_school')
    plan_reception_name = serializers.StringRelatedField(source='plan_reception')
    plan_teacher_name = serializers.StringRelatedField(source='plan_teacher')
    plan_course_name = serializers.StringRelatedField(source='plan_course')
    Visit = VisitSerializer(source='visit_set', many=True)


    class Meta:
        model = models.Clue
        exclude = HIDE_FIELD


