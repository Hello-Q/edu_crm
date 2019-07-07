from rest_framework import serializers
from apps.clue import models


class ChannelTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.ChannelType
        fields = "__all__"


class ChannelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Channel
        fields = "__all__"


class ClueSerializer(serializers.ModelSerializer):
    channel_name = serializers.StringRelatedField(source='channel')
    follow_up_person_name = serializers.StringRelatedField(source='follow_up_person')
    auxiliary_status_name = serializers.StringRelatedField(source='auxiliary_status')
    intended_course_name = serializers.StringRelatedField(source='intended_course')
    intended_school_name = serializers.StringRelatedField(source='intended_school')
    plan_school_name = serializers.StringRelatedField(source='plan_school')
    plan_reception_name = serializers.StringRelatedField(source='plan_reception')
    plan_teacher_name = serializers.StringRelatedField(source='plan_teacher')
    plan_course_name = serializers.StringRelatedField(source='plan_course')

    class Meta:
        model = models.Clue
        exclude = ['update_time', 'create_time', 'del_flag', 'creator',  'operator']
