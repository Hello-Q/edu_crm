from django.db import models

# Create your models here.


class ChannelType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, verbose_name='渠道分类',
                            help_text='渠道分类名称')
    del_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'channel_type'


class Channel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, verbose_name='渠道名称',
                            help_text='渠道名称')
    channel_superior = models.ForeignKey('clue.ChannelType', on_delete=models.SET_NULL,
                                         null=True, verbose_name='渠道分类',
                                         help_text='渠道分类id')
    del_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'channel'


class Clue(models.Model):
    id = models.AutoField(primary_key=True)
    channel = models.ForeignKey('clue.Channel', on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField()
    name = models.CharField(max_length=10, verbose_name='姓名')
    tel = models.CharField(max_length=15)
    age = models.IntegerField()
    sex = models.IntegerField(choices=((0, '女'), (1, '男'), (3, '未知')))
    add = models.CharField(max_length=40, help_text='年龄')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'clue'


