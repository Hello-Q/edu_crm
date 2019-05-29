from rest_framework import serializers
from apps.clue import models


class ChannelTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ChannelType
        fields = "__all__"


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Channel
        fields = "__all__"


class ClueSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Clue
        fields = "__all__"
