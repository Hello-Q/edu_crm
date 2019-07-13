from . import models
from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from rest_framework.serializers import raise_errors_on_nested_writes, model_meta, traceback


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """用户组"""

    class Meta:
        model = Group
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    """角色组"""
    # resources = serializers.PrimaryKeyRelatedField(source='resource', many=True, queryset=models.Resource.objects.all())

    class Meta:
        model = models.Role
        fields = '__all__'


class UserInfoSerializer(serializers.ModelSerializer):

    roles = serializers.PrimaryKeyRelatedField(source='role', many=True, read_only=True)
    roles_name = serializers.StringRelatedField(source='role', many=True, read_only=True)
    department_name = serializers.StringRelatedField(source='department')
    menus = serializers.SerializerMethodField()
    buttons = serializers.SerializerMethodField()

    def get_menus(self, ojb):
        user = models.User.objects.get(pk=ojb.id)
        roles = user.role.all()
        # print(roles)
        resource = models.Resource.objects.none()
        for role in roles:
            resource = resource | role.resource.filter(resource_type=1)
        resource = user.resource.filter(resource_type=1) | resource
        menu_list = []
        for menu in resource.values():
            menu_list.append(menu.get('resource_name'))
        return menu_list

    def get_buttons(self, ojb):
        user = models.User.objects.get(pk=ojb.id)
        roles = user.role.all()
        # print(roles)
        resource = models.Resource.objects.none()
        for role in roles:
            resource = resource | role.resource.filter(resource_type=2)
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

    class Meta:
        model = models.User
        fields = ['id', 'username', 'nickname', 'head_pic', 'password', 'menus', 'roles', 'roles_name', 'department_name', 'buttons']


class UserSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['id', 'username', 'nickname', 'head_pic', 'password']

    def create(self, validated_data):
        """
        We have a bit of extra checking around this in order to provide
        descriptive messages when something goes wrong, but this method is
        essentially just:

            return ExampleModel.objects.create(**validated_data)

        If there are many to many fields present on the instance then they
        cannot be set until the model is instantiated, in which case the
        implementation is like so:

            example_relationship = validated_data.pop('example_relationship')
            instance = ExampleModel.objects.create(**validated_data)
            instance.example_relationship = example_relationship
            return instance

        The default implementation also does not handle nested relationships.
        If you want to support writable nested relationships you'll need
        to write an explicit `.create()` method.
        """
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
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
        fields = ['id', 'name', 'tel', 'type', 'superior', 'superior_name', 'remark']


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