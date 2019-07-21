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
    id = models.AutoField(primary_key=True, verbose_name='科系编号', help_text='科系id')
    name = models.CharField(max_length=10, verbose_name='科系名称', help_text='科系名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '科系'
        verbose_name_plural = '科系管理'


class Course(models.Model):

    TYPE = (
        (0, '一对一'),
        (1, '班课'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15, verbose_name='课程名称', help_text='课程名称')
    type = models.IntegerField('课程类型', choices=TYPE, help_text='{}'.format(TYPE))
    subjects = models.ForeignKey('eduadmin.Subjects', verbose_name='科系', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程管理'


class Teacher(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='教师编号', help_text='教师id')
    user = models.OneToOneField('sys.User', verbose_name='教师姓名', help_text='员工id',
                             on_delete=models.DO_NOTHING)
    course = models.ManyToManyField('eduadmin.Course', verbose_name='所授课程')

    def __str__(self):
        return self.user.nickname

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = '教师管理'
