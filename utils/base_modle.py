from django.db import models


class BaseModel(models.Model):
    organization = models.ForeignKey('sys.Organization', on_delete=models.CASCADE, verbose_name='归属公司', help_text='公司id')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')
    del_flag = models.BooleanField('已删除', default=False, help_text='已删除')
    remark = models.CharField('备注', max_length=150, null=True, blank=True, help_text='备注')

    class Meta:
        abstract = True
