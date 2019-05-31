from django.db import models
# Create your models here.


class CourseType(models.Model):
    cou_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15, verbose_name='课程类型', help_text='课程类型')

    class Meta:
        verbose_name = '课程类型'
        verbose_name_plural = '课程类型'


class Course(models.Model):
    cou_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15, verbose_name='课程名称', help_text='课程名称'),
    course_type = models.ForeignKey('edu_admin.CourseType', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '课程表'
        verbose_name_plural = '课程表'


class BranchSchool(models.Model):
    sch_id = models.AutoField(primary_key=True, verbose_name='校区编号', help_text='校区id')
    org_id = models.ForeignKey('sys_set.Organization', on_delete=models.DO_NOTHING)
    sch_name = models.CharField(max_length=20, verbose_name='校区名称', help_text='校区名称')

    class Meta:
        verbose_name = '校区'
        verbose_name_plural = '小区管理'
