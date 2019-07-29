from django.db import models
from utils.base_modle import BaseModel
from django.contrib.auth.models import AbstractUser
from utils.storage import ImageStorage
from django.contrib.auth.models import Group, Permission

# Create your models here.


class Organization(BaseModel):
    org_id = models.AutoField(primary_key=True, verbose_name='组织编号', help_text='组织id')
    org_name = models.CharField(max_length=20, verbose_name='公司名称', help_text='公司名称')
    org_add = models.CharField(max_length=50, null=True, blank=True, verbose_name='公司地址',
                               help_text='公司地址')
    contacts_man = models.CharField(max_length=6, verbose_name='公司联系人', help_text='公司联系人')
    contacts_tel = models.CharField(max_length=30, verbose_name='联系人电话', help_text='联系人电话')
    legal_person = models.CharField(max_length=6, null=True, blank=True,
                                    verbose_name='公司法人', help_text='公司法人')
    organization = None

    def __str__(self):
        return self.org_name

    class Meta:
        verbose_name = '公司'
        verbose_name_plural = '公司管理'


class Department(BaseModel):
    TYPE = (
        (0, '分公司'),
        (1, '校区'),
        (2, '部门'),
    )
    id = models.AutoField(primary_key=True, verbose_name='部门编号', help_text='部门id')
    name = models.CharField(max_length=10, verbose_name='部门名称', help_text='部门名称')
    tel = models.CharField(max_length=15, verbose_name='电话', help_text='电话', null=True)
    type = models.IntegerField('类型', choices=TYPE)
    superior = models.ForeignKey('sys.Department', verbose_name='上级部门', on_delete=models.DO_NOTHING,
                                 null=True, blank=True)

    creator = models.ForeignKey('sys.User', related_name='department_creator', on_delete=models.DO_NOTHING, verbose_name='创建人', null=True, blank=True)
    operator = models.ForeignKey('sys.User', related_name='department_operator', on_delete=models.DO_NOTHING, verbose_name='更新人', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门管理'



class DataPermissions(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='数据权限编号')
    name = models.CharField('数据权限名称', max_length=25)
    key = models.CharField('数据权限key', max_length=25)
    creator = models.ForeignKey('sys.User', related_name='data_permissions_creator', on_delete=models.DO_NOTHING, verbose_name='创建人')
    operator = models.ForeignKey('sys.User', related_name='data_permissions_operator', on_delete=models.DO_NOTHING, verbose_name='更新人')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '数据权限'
        verbose_name_plural = '数据权限管理'


class Role(BaseModel):
    TYPE = (
        (0, '普通'),
        (1, '客服'),
        (2, '课程顾问'),
    )

    id = models.AutoField(primary_key=True, verbose_name='角色编号', help_text='角色id')
    name = models.CharField(max_length=10, verbose_name='角色名称', help_text='角色名称')
    type = models.IntegerField('角色类型', choices=TYPE, help_text='角色类型{}'.format(TYPE), default=0)
    resource = models.ManyToManyField('sys.Resource', verbose_name='可访问资源', help_text='可访问资源', blank=True)
    creator = models.ForeignKey('sys.User', related_name='role_creator', on_delete=models.DO_NOTHING, verbose_name='创建人')
    operator = models.ForeignKey('sys.User', related_name='role_operator', on_delete=models.DO_NOTHING, verbose_name='更新人')
    # data_permissions = models.ForeignKey('sys.DataPermissions', verbose_name='可访问数据', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色管理'


class Resource(BaseModel):
    resource_id = models.AutoField(primary_key=True, verbose_name='资源编号', help_text='资源id')
    resource_name = models.CharField(max_length=15, verbose_name='资源名称', help_text='资源名称')
    resource_key = models.CharField(max_length=25, verbose_name='资源key', unique=True)
    resource_type = models.IntegerField(choices=((1, '菜单权限'), (2, '按钮权限')), verbose_name='资源类型', help_text='资源类型')
    permissions = models.ManyToManyField(Permission, blank=True, verbose_name='拥有权限')

    def __str__(self):
        return self.resource_name

    class Meta:
        verbose_name = '资源'
        verbose_name_plural = '资源管理'
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.conf import settings
from django.utils.module_loading import import_string
from django.core.exceptions import ImproperlyConfigured
# from django.contrib.auth.backends import ModelBackend
#
# class MyModelBackend(ModelBackend):
#     pass

def get_backends():
    return _get_backends(return_tuples=False)
def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """

    for backend in get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


def load_backend(path):
    return import_string(path)()

def _get_backends(return_tuples=False):
    backends = []
    for backend_path in settings.AUTHENTICATION_BACKENDS:
        backend = load_backend(backend_path)
        backends.append((backend, backend_path) if return_tuples else backend)
    if not backends:
        raise ImproperlyConfigured(
            'No authentication backends have been defined. Does '
            'AUTHENTICATION_BACKENDS contain anything?'
        )
    return backends


class User(AbstractUser, BaseModel):
    age = models.IntegerField(verbose_name="年龄", default="1")
    tel = models.CharField('员工电话', max_length=12)
    department = models.ManyToManyField('sys.Department', verbose_name='所属部门', help_text='部门id',)
    head_pic = models.ImageField(upload_to='img', storage=ImageStorage(), null=True, blank=True, verbose_name='图片url')
    nickname = models.CharField(max_length=15, verbose_name='用户昵称', help_text='用户昵称')
    roles = models.ManyToManyField('Role', verbose_name='角色', blank=True)
    resources = models.ManyToManyField('Resource', verbose_name='拥有资源', help_text='拥有资源', blank=True)
    creator = models.ForeignKey('sys.User', related_name='user_creator', on_delete=models.DO_NOTHING, verbose_name='创建人')
    operator = models.ForeignKey('sys.User', related_name='user_operator', on_delete=models.DO_NOTHING, verbose_name='更新人')
    # user_permissions =

    class Meta:
        verbose_name = '员工'
        verbose_name_plural = '员工管理'

    def __str__(self):
        return self.nickname



    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """

        return all(self.has_perm(perm, obj) for perm in perm_list)

