from django.db import models

from utils.base_modle import BaseModel


# Create your models here.


class ChannelType(BaseModel):
    channel_type_id = models.AutoField(primary_key=True, verbose_name='渠道分类编号', help_text='渠道分类id')
    cha_type_name = models.CharField(max_length=10, unique=True, verbose_name='渠道分类名称', help_text='渠道分类名称')
    del_flag = models.BooleanField('删除标记', default=False)

    def __str__(self):
        return self.cha_type_name

    class Meta:
        verbose_name = '渠道类型'
        verbose_name_plural = '渠道类型管理'


class Channel(BaseModel):
    channel_id = models.AutoField(primary_key=True)
    cha_name = models.CharField(max_length=10, verbose_name='渠道名称', unique=True,
                                help_text='渠道名称')
    channel_type_id = models.ForeignKey('clue.ChannelType', on_delete=models.SET_NULL,
                                        null=True, verbose_name='渠道分类',
                                        help_text='渠道分类id')
    del_flag = models.BooleanField('删除标记', default=False)

    def __str__(self):
        return self.cha_name

    class Meta:
        verbose_name = '渠道'
        verbose_name_plural = '渠道管理'


class Clue(BaseModel):
    clue_id = models.AutoField(primary_key=True)
    channel_id = models.ForeignKey('clue.Channel', on_delete=models.DO_NOTHING, verbose_name='来源渠道',
                                   help_text='来源渠道')
    name = models.CharField(max_length=10, verbose_name='姓名', help_text='姓名')
    tel = models.CharField(max_length=15, verbose_name='电话', help_text='电话')
    age = models.IntegerField(verbose_name='年龄', help_text='年龄', null=True, blank=True)
    sex = models.IntegerField(choices=((0, '女'), (1, '男'),), null=True, blank=True,
                              verbose_name='性别', help_text='性别,0:女,1:男,未知留空')
    add = models.CharField(max_length=40, verbose_name='地址', help_text='地址', null=True, blank=True)

    update_user = models.ForeignKey('user.UserProfile', related_name='channel_user_type_update',
                                    on_delete=models.DO_NOTHING, verbose_name='更新人')
    delete_user = models.ForeignKey('user.UserProfile', related_name='channel_user_type_delete',
                                    on_delete=models.DO_NOTHING, verbose_name='删除人')
    create_user = models.ForeignKey('user.UserProfile', related_name='channel_user_type_create',
                                    on_delete=models.DO_NOTHING, verbose_name='创建人')

    def __str__(self):
        return self.name
