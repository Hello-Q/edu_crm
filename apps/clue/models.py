from django.db import models
from util.base_modle import BaseModel
# Create your models here.


class ChannelType(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, unique=True, verbose_name='渠道分类',
                            help_text='渠道分类')

    update_user = models.ForeignKey('user.UserProfile', related_name='channel_user_type_update',
                                    on_delete=models.SET_DEFAULT, default=0, verbose_name='更新人')
    delete_user = models.ForeignKey('user.UserProfile', related_name='channel_user_type_delete',
                                    on_delete=models.SET_DEFAULT, default=0, verbose_name='删除人')
    create_user = models.ForeignKey('user.UserProfile', related_name='channel_user_type_create',
                                    on_delete=models.SET_DEFAULT, default=0, verbose_name='创建人')

    del_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'channel_type'


class Channel(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, verbose_name='渠道名称', unique=True,
                            help_text='渠道名称')
    channel_type = models.ForeignKey('clue.ChannelType', on_delete=models.SET_NULL,
                                     null=True, verbose_name='渠道分类',
                                     help_text='渠道分类id')
    del_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'channel'


class Clue(BaseModel):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=10, verbose_name='姓名')
    tel = models.CharField(max_length=15)
    age = models.IntegerField()
    sex = models.IntegerField(choices=((0, '女'), (1, '男'), (3, '未知')))
    add = models.CharField(max_length=40, help_text='年龄')
    channel = models.ForeignKey('clue.Channel', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'clue'


