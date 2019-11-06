# 增加权限权限查询的链路，配合vue权限管理

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.backends import ModelBackend


class MyModelBackend(ModelBackend):
    def _get_user_permissions(self, user_obj):  # 就是他了!!!!
        return Permission.objects.filter(**{'resource__user': user_obj})
        # return user_obj.user_permissions.all()    # 这是原来的

    def _get_group_permissions(self, user_obj):  # 就是他了!!!!
        # user_groups_field = get_user_model()._meta.get_field('groups')
        user_groups_field = get_user_model()._meta.get_field('roles')
        user_groups_query = 'resource__role__%s' % user_groups_field.related_query_name()
        return Permission.objects.filter(**{user_groups_query: user_obj})
