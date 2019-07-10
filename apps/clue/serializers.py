from rest_framework import serializers
from apps.clue import models
from edu_crm.settings import HIDE_FIELD

class ChannelTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.ChannelType
        fields = "__all__"


class ChannelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Channel
        fields = "__all__"


class VisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Visit
        exclude = HIDE_FIELD


class ClueSerializer(serializers.ModelSerializer):
    channel_name = serializers.StringRelatedField(source='channel')
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


