from django.db import models
from utils.base_modle import BaseModel
from django.contrib.auth.models import AbstractUser
from utils.storage import ImageStorage
from django.contrib.auth.models import Group
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

    def __str__(self):
        return self.org_name

    class Meta:
        verbose_name = '公司'
        verbose_name_plural = '公司管理'


class Department(BaseModel):
    dep_id = models.AutoField(primary_key=True, verbose_name='部门编号', help_text='部门id')
    org = models.ForeignKey('sys.Organization', on_delete=models.DO_NOTHING,
                            verbose_name='公司名称', help_text='公司id')
    dep_type = models.IntegerField('类型', choices=((0, '分公司'), (1, '校区'), (2, '部门'), ), null=True)
    superior = models.ForeignKey('sys.Department', verbose_name='上级部门', on_delete=models.DO_NOTHING,
                                 null=True, blank=True)
    dep_name = models.CharField(max_length=10, verbose_name='部门名称', help_text='部门名称')
    dep_tel = models.CharField(max_length=15, verbose_name='电话', help_text='电话', null=True)

    creator = models.ForeignKey('sys.User', related_name='department_creator', on_delete=models.DO_NOTHING, verbose_name='创建人', null=True, blank=True)
    operator = models.ForeignKey('sys.User', related_name='department_operator', on_delete=models.DO_NOTHING, verbose_name='更新人', null=True, blank=True)

    def __str__(self):
        return self.dep_name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门管理'


class Role(BaseModel):
    role_id = models.AutoField(primary_key=True, verbose_name='角色编号', help_text='角色id')
    role_name = models.CharField(max_length=10, verbose_name='角色名称', help_text='角色名称')
    resource = models.ManyToManyField('sys.Resource', verbose_name='可访问资源', help_text='可访问资源')

    def __str__(self):
        return self.role_name

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色管理'


class Resource(BaseModel):
    resource_id = models.AutoField(primary_key=True, verbose_name='资源编号', help_text='资源id')
    resource_name = models.CharField(max_length=15, verbose_name='资源名称', help_text='资源名称')
    resource_key = models.CharField(max_length=25, verbose_name='资源key', unique=True)
    resource_type = models.IntegerField(choices=((1, '菜单权限'), (2, '按钮权限')), verbose_name='资源类型', help_text='资源类型')

    def __str__(self):
        return self.resource_name

    class Meta:
        verbose_name = '资源'
        verbose_name_plural = '资源管理'


class User(AbstractUser, BaseModel):
    age = models.IntegerField(verbose_name="年龄", default="1")
    department = models.ForeignKey('sys.Department', verbose_name='所属部门', help_text='部门id', null=True, blank=True, on_delete=models.DO_NOTHING)
    head_pic = models.ImageField(upload_to='img', storage=ImageStorage(), null=True, blank=True, verbose_name='图片url')
    nickname = models.CharField(max_length=15, verbose_name='用户昵称', help_text='用户昵称')
    role = models.ManyToManyField('Role', verbose_name='角色')
    resource = models.ManyToManyField('Resource', verbose_name='拥有资源', help_text='拥有资源')

    class Meta:
        verbose_name = '员工'
        verbose_name_plural = '员工管理'

    def __str__(self):
        return self.nickname

