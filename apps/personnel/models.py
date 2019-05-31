from django.db import models

# Create your models here.


class Department(models.Model):
    dep_id = models.AutoField(primary_key=True, verbose_name='部门编号', help_text='部门id')
    # org_id = models.ForeignKey()
    dep_name = models.CharField(max_length=10, verbose_name='部门名称', help_text='部门名称')
