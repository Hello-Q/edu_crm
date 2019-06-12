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


class ClueSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Clue
        exclude = []
