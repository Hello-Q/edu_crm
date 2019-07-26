from . import models
from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from rest_framework.serializers import raise_errors_on_nested_writes, model_meta, traceback
from drf_writable_nested import WritableNestedModelSerializer


class RoleSerializer(WritableNestedModelSerializer):
    """角色组"""
    # resources = serializers.PrimaryKeyRelatedField(source='resource', many=True, queryset=models.Resource.objects.all())

    class Meta:
        model = models.Role
        fields = ['id', 'name', 'resource']


class UserInfoSerializer(serializers.ModelSerializer):

    roles = serializers.PrimaryKeyRelatedField(source='groups', many=True, read_only=True)
    roles_name = serializers.StringRelatedField(source='groups', many=True, read_only=True)
    department_name = serializers.StringRelatedField(source='department', many=True, read_only=True)
    menus = serializers.SerializerMethodField()
    buttons = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ['id', 'username', 'nickname', 'head_pic', 'password',  'department_name', 'roles', 'roles_name','menus', 'buttons']

    def get_menus(self, ojb):
        user = models.User.objects.get(pk=ojb.id)
        groups = user.groups.all()
        # print(roles)
        resource = models.Resource.objects.none()
        for group in groups:
            resource = resource | group.role.resource.filter(resource_type=1)
        resource = user.resource.filter(resource_type=1) | resource
        menu_list = []
        for menu in resource.values():
            menu_list.append(menu.get('resource_name'))
        return menu_list

    def get_buttons(self, ojb):
        user = models.User.objects.get(pk=ojb.id)
        groups = user.groups.all()
        # print(roles)
        resource = models.Resource.objects.none()
        for group in groups:
            resource = resource | group.role.resource.filter(resource_type=2)
        resource = user.resource.filter(resource_type=2) | resource
        button_list = []
        for menu in resource.values():
            button_list.append(menu.get('resource_name'))
        return button_list

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)

            if attr == 'password':
                instance.set_password(value)

            else:
                setattr(instance, attr, value)
        instance.save()

        return instance


class UserSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['id', 'username', 'nickname', 'head_pic', 'password', 'tel']

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)
        ModelClass = self.Meta.model
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create_user(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'nickname', 'tel']


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Organization
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    superior_name = serializers.StringRelatedField(source='superior', read_only=True)
    # organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = models.Department
        fields = ['id', 'name', 'tel', 'type', 'superior', 'superior_name', 'organization', 'remark']


class DepartmentBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Department
        fields = ["id", 'name', 'tel']


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ["name", 'codename']


class ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Resource
        fields = "__all__"