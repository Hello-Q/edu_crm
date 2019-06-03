from django.db import models
# Create your models here.


# class CourseType(models.Model):
#     cou_type_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=15, verbose_name='课程类型', help_text='课程类型')
#
#     class Meta:
#         verbose_name = '课程类型'
#         verbose_name_plural = '课程类型'


class Subjects(models.Model):
    sub_id = models.AutoField(primary_key=True, verbose_name='科系编号', help_text='科系id')
    sub_name = models.CharField(max_length=10, verbose_name='科系名称', help_text='科系名称')

    def __str__(self):
        return self.sub_name

    class Meta:
        verbose_name = '科系'
        verbose_name_plural = '科系管理'


class Course(models.Model):
    cou_id = models.AutoField(primary_key=True)
    cou_type = models.IntegerField('课程类型', choices=((0, '一对一'), (1, '班课')))
    course_subjects = models.ForeignKey('edu_admin.Subjects', verbose_name='科系', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=15, verbose_name='课程名称', help_text='课程名称')

    class Meta:
        verbose_name = '课程表'
        verbose_name_plural = '课程表'


class Teacher(models.Model):
    tea_id = models.AutoField(primary_key=True, verbose_name='教师编号', help_text='教师id')
    user_id = models.ForeignKey('sys_set.UserProfile', verbose_name='员工编号', help_text='员工id',
                                on_delete=models.DO_NOTHING, null=True, blank=True)
    tea_name = models.CharField(max_length=6, verbose_name='教师姓名', help_text='教师姓名')
