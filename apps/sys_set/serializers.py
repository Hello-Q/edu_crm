from . import models
from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin
from django.contrib.auth.models import Permission

class UserSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.UserProfile
        # exclude = []
        fields = ['username', 'first_name', 'last_name']

    def create(self, validated_data):
        user = models.UserProfile.objects.create_user(**validated_data)  # 这里新增玩家必须用create_user,否则密码不是秘文
        return user


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Organization
        fields = "__all__"


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Department
        fields = "__all__"


class PermissionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Permission
        fields = ["name", 'codename']
