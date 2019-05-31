from django.db import models
# Create your models here.


class CourseType(models.Model):
    cou_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15, verbose_name='课程类型', help_text='课程类型')

    class Meta:
        verbose_name = '课程类型'
        verbose_name_plural = '课程类型'


class Subjects(models.Model):
    sub_id = models.AutoField(primary_key=True, verbose_name='科系编号', help_text='科系id')
    sub_name = models.CharField(max_length=10, verbose_name='科系名称', help_text='科系名称')


class Course(models.Model):
    cou_id = models.AutoField(primary_key=True)
    cou_type = models.IntegerField(choices=((0, '一对一'), (1, '班课')))
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
        verbose_name_plural = '校区管理'


class Teacher(models.Model):
    tea_id = models.AutoField(primary_key=True, verbose_name='教师编号', help_text='教师id')
    user_id = models.ForeignKey('user.UserProfile', verbose_name='员工编号', help_text='员工id',
                                on_delete=models.DO_NOTHING, null=True, blank=True)
    tea_name = models.CharField(max_length=6, verbose_name='教师姓名', help_text='教师姓名')

