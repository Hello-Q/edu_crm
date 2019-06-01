from django.db import models
from utils.base_modle import BaseModel
# Create your models here.


class Department(BaseModel):
    dep_id = models.AutoField(primary_key=True, verbose_name='部门编号', help_text='部门id')
    org_id = models.ForeignKey('sys_set.Organization', on_delete=models.DO_NOTHING,
                               verbose_name='公司名称', help_text='公司id')
    dep_type = models.IntegerField('类型', choices=((0, '分公司'), (1, '校区'), (2, '部门'), ), null=True)
    superior_id = models.ForeignKey('personnel.Department', verbose_name='上级部门', on_delete=models.DO_NOTHING,
                                    null=True, blank=True)
    dep_name = models.CharField(max_length=10, verbose_name='部门名称', help_text='部门名称')
    dep_tel = models.CharField(max_length=15, verbose_name='电话', help_text='电话', null=True)

    def __str__(self):
        return self.dep_name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门管理'
