from django.db import models

from utils.base_modle import BaseModel


# Create your models here.


class ChannelType(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='渠道分类编号', help_text='渠道分类id')
    name = models.CharField(max_length=10, unique=True, verbose_name='渠道分类名称', help_text='渠道分类名称')
    creator = models.ForeignKey('sys.User', related_name='ChannelType_creator', on_delete=models.DO_NOTHING, verbose_name='创建人', null=True, blank=True)
    operator = models.ForeignKey('sys.User', related_name='ChannelType_operator', on_delete=models.DO_NOTHING, verbose_name='更新人', null=True, blank=True)
    del_flag = models.BooleanField('删除标记', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '渠道类型'
        verbose_name_plural = '渠道类型管理'
        permissions = (
            ('view_channeltype', 'Can view 渠道类型'),
        )


class Channel(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, verbose_name='渠道名称', unique=True, help_text='渠道名称')
    type = models.ForeignKey('clue.ChannelType', on_delete=models.CASCADE, verbose_name='渠道分类', help_text='渠道分类id')
    del_flag = models.BooleanField('删除标记', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '渠道'
        verbose_name_plural = '渠道管理'
        ordering = ['id']


class Clue(BaseModel):
    STATUS = (
        (0, '待跟进'),
        (1, '下次联系'),
        (2, '成功约访'),
        (3, '已到访'),
        (4, '无法成交'),
        (5, '已报名'),
    )
    AUXILIARY_STATUS = (
        (0, '约访'),
        (1, '试听')
    )
    SEX = (
        (0, '女'),
        (1, '男'),
    )
    id = models.AutoField(primary_key=True)
    channel = models.ForeignKey('clue.Channel', on_delete=models.DO_NOTHING, verbose_name='来源渠道', help_text='来源渠道')
    name = models.CharField(max_length=10, verbose_name='姓名', help_text='姓名')
    tel = models.CharField(max_length=15, verbose_name='电话', help_text='电话')
    age = models.IntegerField(verbose_name='年龄', help_text='年龄', null=True, blank=True)
    sex = models.IntegerField(choices=((0, '女'), (1, '男'),), null=True, blank=True,
                              verbose_name='性别', help_text='{}'.format(SEX))
    address = models.CharField(max_length=40, verbose_name='地址', help_text='地址', null=True, blank=True)
    consult_date = models.DateField('录入日期', help_text='录入日期',)
    intended_course = models.ManyToManyField('eduadmin.Course', related_name='clue_intended_course', verbose_name='意向课程', help_text='意向课程',  blank=True)
    intended_school = models.ManyToManyField('sys.Department', related_name='clue_intended_school', verbose_name='意向校区', help_text='意向校区', blank=True)
    follow_up_person = models.ForeignKey('sys.User', related_name='clue_follow_up_people', verbose_name='跟进人', help_text='跟进人', on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField('线索状态', help_text='线索状态{}'.format(STATUS), choices=STATUS, null=True, blank=True,)
    next_date = models.DateField(verbose_name='下次联系日期', help_text='下次联系日期', null=True, blank=True)
    next_time = models.TimeField(verbose_name='下次联系时间', help_text='下次联系时间', null=True, blank=True)
    is_importance = models.NullBooleanField(verbose_name='重要客户', help_text='是否重要客户', null=True, blank=True)
    # auxiliary_status = models.IntegerField('辅助状态', choices=AUXILIARY_STATUS, help_text='{}'.format(AUXILIARY_STATUS), null=True, blank=True)
    # plan_date = models.DateField('安排日期', help_text='安排日期', null=True, blank=True)
    # plan_time = models.TimeField('安排时间', help_text='安排时间', null=True, blank=True)
    # plan_school = models.ForeignKey('sys.Department', related_name='clue_plan_school', verbose_name='安排校区', help_text='安排校区', on_delete=True, null=True, blank=True)
    # plan_reception = models.ForeignKey('sys.User', related_name='clue_plan_reception', verbose_name='安排接待', help_text='安排接待', on_delete=models.DO_NOTHING, null=True, blank=True)
    # plan_teacher = models.ForeignKey('eduadmin.Teacher', related_name='clue_plan_teacher', verbose_name='安排老师', help_text='安排校区', on_delete=models.DO_NOTHING, null=True, blank=True)
    # plan_course = models.ForeignKey('eduadmin.Course', related_name='clue_plan_course', verbose_name='安排课程', help_text='安排课程', on_delete=models.DO_NOTHING, null=True, blank=True)
    creator = models.ForeignKey('sys.User', related_name='clue_creator', on_delete=models.DO_NOTHING, verbose_name='创建人', null=True, blank=True)
    operator = models.ForeignKey('sys.User', related_name='clue_operator', on_delete=models.DO_NOTHING, verbose_name='更新人', null=True, blank=True)
    test_time = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '线索'
        verbose_name_plural = '线索管理'


class Visit(BaseModel):

    VISIT_TYPE = (
        (0, '约访'),
        (1, '试听'),
    )

    id = models.AutoField(primary_key=True, )
    type = models.IntegerField('访问类型', help_text='访问类型{}'.format(VISIT_TYPE), choices=VISIT_TYPE)
    date = models.DateField('日期', help_text='安排日期')
    time = models.TimeField('时间', help_text='安排时间')
    school = models.ForeignKey('sys.Department', related_name='clue_plan_school', verbose_name='安排校区', help_text='安排校区', on_delete=True)
    ordered_reception = models.ForeignKey('sys.User', related_name='clue_plan_reception', verbose_name='安排接待', help_text='安排接待', on_delete=models.CASCADE)
    ordered_teacher = models.ForeignKey('eduadmin.Teacher', related_name='clue_plan_teacher', verbose_name='安排老师', help_text='安排校区', on_delete=models.CASCADE, null=True, blank=True)
    ordered_course = models.ForeignKey('eduadmin.Course', related_name='clue_plan_course', verbose_name='安排课程', help_text='安排课程', on_delete=models.CASCADE, null=True, blank=True)
    clue = models.ForeignKey('clue.Clue', verbose_name='线索', on_delete=models.CASCADE)
    is_visit = models.BooleanField('访问状态', )
    creator = models.ForeignKey('sys.User', related_name='visit_creator', on_delete=models.DO_NOTHING, verbose_name='创建人')
    operator = models.ForeignKey('sys.User', related_name='visit_operator', on_delete=models.DO_NOTHING, verbose_name='更新人')


class FollowRecord(BaseModel):
    id = models.AutoField(primary_key=True)
    clue = models.ForeignKey('clue.Clue', on_delete=models.CASCADE, verbose_name='关联线索')
    datetime = models.DateTimeField(auto_now_add=True, )
    content = models.TextField(max_length=1000)
    creator = models.ForeignKey('sys.User', related_name='follow_creator', on_delete=models.DO_NOTHING, verbose_name='创建人')
    operator = models.ForeignKey('sys.User', related_name='follow_operator', on_delete=models.DO_NOTHING, verbose_name='更新人')

