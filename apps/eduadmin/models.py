from django.db import models
# Create your models here.
from utils.base_modle import BaseModel



# class CourseType(models.Model):
#     cou_type_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=15, verbose_name='课程类型', help_text='课程类型')
#
#     class Meta:
#         verbose_name = '课程类型'
#         verbose_name_plural = '课程类型'


class Subjects(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='科系编号', help_text='科系id')
    name = models.CharField(max_length=10, verbose_name='科系名称', help_text='科系名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '科系'
        verbose_name_plural = '科系管理'


class Course(BaseModel):

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


class Teacher(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='教师编号', help_text='教师id')
    user = models.OneToOneField('sys.User', verbose_name='对应员工', help_text='员工id',
                             on_delete=models.DO_NOTHING)
    course = models.ManyToManyField('eduadmin.Course', verbose_name='所授课程')

    def __str__(self):
        return self.user.nickname

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = '教师管理'


class Student(BaseModel):
    SEX = (
        (0, '女'),
        (1, '男'),
    )
    STATUS = (
        (0, '新签'),
        (1, '已缴费'),
        (2, '上课中'),
        (3, '停课'),
        (4, '结课'),
    )
    id = models.AutoField(primary_key=True, verbose_name='学员编号')
    name = models.CharField('学员姓名', max_length=7)
    tel = models.CharField('联系电话', max_length=12)
    clue = models.ForeignKey('clue.Clue', verbose_name='关联线索', on_delete=models.CASCADE)
    school = models.ForeignKey('sys.Department', verbose_name='归属校区', on_delete=models.CASCADE)
    birthday = models.DateField('学员生日', null=True, blank=True)
    sex = models.IntegerField(choices=SEX, null=True, blank=True, verbose_name='性别', help_text='{}'.format(SEX))
    father_name = models.CharField('父亲姓名', max_length=5, null=True, blank=True)
    father_tel = models.CharField('父亲电话', max_length=12, null=True, blank=True)
    mother_name = models.CharField('母亲姓名', max_length=5, null=True, blank=True)
    mother_tel = models.CharField('母亲电话', max_length=12, null=True, blank=True)
    status = models.IntegerField('学员状态', choices=STATUS, default=0)


