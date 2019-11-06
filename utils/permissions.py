from rest_framework.permissions import DjangoModelPermissions, BasePermission, DjangoObjectPermissions
from rest_framework import exceptions
SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
from django.http.response import Http404
from django.contrib.auth.models import Permission
from apps.sys.models import Role


class DataPermission(object):

    data_filter_map = [
        'clue',
    ]
    authenticated_users_only = True

    def get_data_permission(self, model_cls):
        # 无需校验数据,直接返回公司数据权限
        if not model_cls._meta.model_name in self.data_filter_map:
            return 30
        """获取权限名称"""
        kwargs = {
            'model_name': model_cls._meta.model_name
        }
        perm_codename = 'view_%(model_name)s' % kwargs
        # 获取权限
        perm = Permission.objects.get(codename__exact=perm_codename)
        # 获取角色
        roles = set(Role.objects.filter(resources__permissions=perm))
        data_permission = max([role.data_permission for role in roles])
        return data_permission

    def get_perm_queryset(self, model_cls, request, queryset):
        """获取符合用户权限的queryset"""
        data_permission = self.get_data_permission(model_cls)
        if data_permission == 0:
            queryset = queryset.filter(creator=request.user)
        elif data_permission == 10:
            department = request.user.department.all()
            queryset = queryset.filter(creator__department__in=department).distinct()
        elif data_permission == 30:
            organization = request.user.organization
            queryset = queryset.filter(organization=organization)
        return queryset


class ExpandDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    authenticated_users_only = True

    def get_required_permissions(self, method, model_cls):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name
        }

        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm % kwargs for perm in self.perms_map[method]]

    # 什么都没改
    def _queryset(self, view):
        assert hasattr(view, 'get_queryset') \
            or getattr(view, 'queryset', None) is not None, (
            'Cannot apply {} on a view that does not set '
            '`.queryset` or have a `.get_queryset()` method.'
        ).format(self.__class__.__name__)

        if hasattr(view, 'get_queryset'):
            queryset = view.get_queryset()
            assert queryset is not None, (
                '{}.get_queryset() returned None'.format(view.__class__.__name__)
            )
            return queryset
        return view.queryset

    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if not request.user or (
           not request.user.is_authenticated and self.authenticated_users_only):
            return False

        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset.model)
        return request.user.has_perms(perms)
