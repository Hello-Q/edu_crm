from apps.user import models
from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin


class UserSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.UserProfile
        fields = ["username", "password"]

    def create(self, validated_data):
        user = models.UserProfile.objects.create_user(**validated_data)  # 这里新增玩家必须用create_user,否则密码不是秘文
        return user

