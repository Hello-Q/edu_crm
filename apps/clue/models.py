from django.db import models

from utils.base_modle import BaseModel


# Create your models here.


class ChannelType(BaseModel):
    channel_type_id = models.AutoField(primary_key=True, verbose_name='渠道分类编号', help_text='渠道分类id')
    cha_type_name = models.CharField(max_length=10, unique=True, verbose_name='渠道分类名称', help_text='渠道分类名称')
    del_flag = models.BooleanField('删除标记', default=False)

    def __str__(self):
        return self.cha_type_name

    def __all__(self):
        return [self.channel_type_id, self.cha_type_name, self.del_flag]

    class Meta:
        verbose_name = '渠道类型'
        verbose_name_plural = '渠道类型管理'
        permissions = (
            ('view_channeltype', 'Can view 渠道类型'),
        )


class Channel(BaseModel):
    channel_id = models.AutoField(primary_key=True)
    cha_name = models.CharField(max_length=10, verbose_name='渠道名称', unique=True,
                                help_text='渠道名称')
    channel_type = models.ForeignKey('clue.ChannelType', on_delete=models.SET_NULL,
                                        null=True, verbose_name='渠道分类',
                                        help_text='渠道分类id')
    del_flag = models.BooleanField('删除标记', default=False)

    def __str__(self):
        return self.cha_name

    class Meta:
        verbose_name = '渠道'
        verbose_name_plural = '渠道管理'


class Clue(BaseModel):
    STATUS = (
        (0, '下次联系'),
        (1, '成功约访'),
        (2, '已到访'),
        (3, '无法成交'),
        (4, '已报名'),
    )
    AUXILIARY_STATUS = (
        (0, '约访'),
        (1, '试听')
    )
    clue_id = models.AutoField(primary_key=True)
    channel = models.ForeignKey('clue.Channel', on_delete=models.DO_NOTHING, verbose_name='来源渠道',
                                   help_text='来源渠道')
    name = models.CharField(max_length=10, verbose_name='姓名', help_text='姓名')
    tel = models.CharField(max_length=15, verbose_name='电话', help_text='电话')
    age = models.IntegerField(verbose_name='年龄', help_text='年龄', null=True, blank=True)
    sex = models.IntegerField(choices=((0, '女'), (1, '男'),), null=True, blank=True,
                              verbose_name='性别', help_text='{}'.format(STATUS))
    add = models.CharField(max_length=40, verbose_name='地址', help_text='地址', null=True, blank=True)
    intended_course = models.ForeignKey('eduadmin.Course', related_name='clue_intended_course', verbose_name='意向课程', help_text='意向课程', on_delete=models.DO_NOTHING, null=True, blank=True)
    intended_school = models.ForeignKey('sys.Department', related_name='clue_intended_school', verbose_name='意向校区', help_text='意向校区', on_delete=models.DO_NOTHING, null=True, blank=True)
    follow_up_people = models.ForeignKey('sys.User', related_name='clue_follow_up_people', verbose_name='跟进人', help_text='跟进人', on_delete=models.DO_NOTHING, null=True, blank=True)
    status = models.IntegerField('线索状态', help_text='线索状态', choices=STATUS, null=True, blank=True)
    auxiliary_status = models.IntegerField('辅助状态', choices=AUXILIARY_STATUS, help_text='{}'.format(AUXILIARY_STATUS), null=True, blank=True)
    plan_date = models.DateField('安排日期', help_text='安排日期', null=True, blank=True)
    plan_time = models.TimeField('安排时间', help_text='安排时间', null=True, blank=True)
    plan_school = models.ForeignKey('sys.Department', related_name='clue_plan_school', verbose_name='安排校区', help_text='安排校区', on_delete=True, null=True, blank=True)
    plan_reception = models.ForeignKey('sys.User', related_name='clue_plan_reception', verbose_name='安排接待', help_text='安排接待', on_delete=models.DO_NOTHING, null=True, blank=True)
    plan_teacher = models.ForeignKey('eduadmin.Teacher', related_name='clue_plan_teacher', verbose_name='安排老师', help_text='安排校区', on_delete=models.DO_NOTHING, null=True, blank=True)
    plan_course = models.ForeignKey('eduadmin.Course', related_name='clue_plan_course', verbose_name='安排课程', help_text='安排课程', on_delete=models.DO_NOTHING, null=True, blank=True)
    creator = models.ForeignKey('sys.User', related_name='clue_creator', on_delete=models.DO_NOTHING, verbose_name='创建人', null=True, blank=True)
    operator = models.ForeignKey('sys.User', related_name='clue_operator', on_delete=models.DO_NOTHING, verbose_name='更新人', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '线索'
        verbose_name_plural = '线索管理'
