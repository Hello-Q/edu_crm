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


class FailingType(BaseModel):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=25, verbose_name='无法成交原因类型')


class Clue(BaseModel):
    STATUS = (
        # (0, '待跟进'),
        # (1, '待联系'),
        # (2, '已约访'),
        # (3, '已到访'),
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
    intended_school = models.ForeignKey('sys.Department', related_name='clue_intended_school', verbose_name='意向校区', help_text='意向校区', on_delete=models.CASCADE, null=True, blank=True)
    follow_up_person = models.ForeignKey('sys.User', related_name='clue_follow_up_people', verbose_name='跟进人', help_text='跟进人', on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField('线索状态', help_text='线索状态{}'.format(STATUS), default=0, choices=STATUS)
    next_time = models.DateTimeField(verbose_name='下次联系时间', help_text='下次联系时间', null=True, blank=True)
    failing_type = models.ForeignKey('clue.FailingType', on_delete=models.CASCADE, verbose_name='未成交原因类型', null=True, blank=True)
    failing_cause = models.CharField(max_length=240, verbose_name='未成交原因', null=True, blank=True)
    is_importance = models.NullBooleanField(verbose_name='重要客户', help_text='是否重要客户', null=True, blank=True)
    # 附加信息
    creator = models.ForeignKey('sys.User', related_name='clue_creator', on_delete=models.DO_NOTHING, verbose_name='创建人', null=True, blank=True)
    operator = models.ForeignKey('sys.User', related_name='clue_operator', on_delete=models.DO_NOTHING, verbose_name='更新人', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '线索'
        verbose_name_plural = '线索管理'
        ordering = ['-create_time']
        # unique_together = ('tel', 'organization')


class Visit(BaseModel):
    VISIT_TYPE = (
        (0, '约访'),
        (1, '试听'),
    )
    STATUS = (
        (0, '约访'),
        (1, '到访'),
        (2, '取消'),
        (3, '改约')
    )
    id = models.AutoField(primary_key=True, )
    clue = models.ForeignKey('clue.Clue', verbose_name='线索', on_delete=models.CASCADE)
    type = models.IntegerField('访问类型', help_text='访问类型{}'.format(VISIT_TYPE), choices=VISIT_TYPE)
    visit_time = models.DateTimeField('安排时间', help_text='安排时间')
    # school = models.ForeignKey('sys.Department', related_name='clue_plan_school', verbose_name='安排校区', help_text='安排校区', on_delete=True)
    # ordered_reception = models.ForeignKey('sys.User', related_name='clue_plan_reception', verbose_name='安排接待', help_text='安排接待', on_delete=models.CASCADE)
    ordered_teacher = models.ForeignKey('eduadmin.Teacher', related_name='clue_plan_teacher', verbose_name='安排老师', help_text='安排校区', on_delete=models.CASCADE, null=True, blank=True)
    ordered_course = models.ForeignKey('eduadmin.Course', related_name='clue_plan_course', verbose_name='安排课程', help_text='安排课程', on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField('访问状态', choices=STATUS, default=0)
    revocatory_reason = models.CharField(max_length=200, verbose_name='未到访原因', null=True, blank=True)
    creator = models.ForeignKey('sys.User', related_name='visit_creator', on_delete=models.DO_NOTHING, verbose_name='创建人')
    operator = models.ForeignKey('sys.User', related_name='visit_operator', on_delete=models.DO_NOTHING, verbose_name='更新人')


    class Meta:
        ordering = ['-create_time']


class FollowRecord(BaseModel):
    id = models.AutoField(primary_key=True)
    clue = models.ForeignKey('clue.Clue', on_delete=models.CASCADE, verbose_name='关联线索')
    # clue_status = models.CharField(max_length=240)
    follow_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    content = models.TextField(max_length=1000)
    creator = models.ForeignKey('sys.User', related_name='follow_creator', on_delete=models.DO_NOTHING, verbose_name='创建人')
    operator = models.ForeignKey('sys.User', related_name='follow_operator', on_delete=models.DO_NOTHING, verbose_name='更新人')

