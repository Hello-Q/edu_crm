from django.db import models

# Create your models here.


class Organization(models.Model):
    org_id = models.AutoField(primary_key=True, verbose_name='组织编号', help_text='组织id')
    org_name = models.CharField(max_length=20, verbose_name='公司名称', help_text='公司名称')
    org_add = models.CharField(max_length=50, null=True, blank=True, verbose_name='公司地址',
                               help_text='公司地址')
    contacts_man = models.CharField(max_length=6, verbose_name='公司联系人', help_text='公司联系人')
    contacts_tel = models.CharField(max_length=30, verbose_name='联系人电话', help_text='联系人电话')
    legal_person = models.CharField(max_length=6, null=True, blank=True,
                                    verbose_name='公司法人', help_text='公司法人')

    class Meta:
        verbose_name = '组织'
        verbose_name_plural = verbose_name
