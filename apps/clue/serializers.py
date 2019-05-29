from rest_framework import serializers
from apps.clue import models


class SourceChannelSerializer(serializers.ModelSerializer):
    channel_superior_name = serializers.CharField(max_length=15, source='channel_superior.name', required=False,
                                                  help_text='上级渠道名称')

    class Meta:
        model = models.Channel
        fields = "__all__"


class ClueSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Clue
        fields = "__all__"
