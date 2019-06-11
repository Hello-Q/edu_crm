from django.db import models
from utils.base_modle import BaseModel
from django.contrib.auth.models import AbstractUser

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
    org_id = models.ForeignKey('sys_set.Organization', on_delete=models.DO_NOTHING,
                               verbose_name='公司名称', help_text='公司id')
    dep_type = models.IntegerField('类型', choices=((0, '分公司'), (1, '校区'), (2, '部门'), ), null=True)
    superior_id = models.ForeignKey('sys_set.Department', verbose_name='上级部门', on_delete=models.DO_NOTHING,
                                    null=True, blank=True)
    dep_name = models.CharField(max_length=10, verbose_name='部门名称', help_text='部门名称')
    dep_tel = models.CharField(max_length=15, verbose_name='电话', help_text='电话', null=True)

    creator = models.ForeignKey('sys_set.UserProfile', related_name='department_creator', on_delete=models.DO_NOTHING, verbose_name='创建人', null=True, blank=True)
    operator = models.ForeignKey('sys_set.UserProfile', related_name='department_operator', on_delete=models.DO_NOTHING, verbose_name='更新人', null=True, blank=True)

    def __str__(self):
        return self.dep_name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门管理'


class UserProfile(AbstractUser, BaseModel):
    age = models.IntegerField(verbose_name="年龄", default="1")
    # org_id = models.ForeignKey('sys_set.Organization', verbose_name='所属公司', help_text='所属公司id',
    #                            on_delete=models.DO_NOTHING)
    # dep_id = models.ForeignKey('sys_set.Department', verbose_name='所属部门', help_text='部门id',
    #                            on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '员工'
        verbose_name_plural = '员工管理'
