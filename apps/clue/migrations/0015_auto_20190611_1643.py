# Generated by Django 2.0 on 2019-06-11 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clue', '0014_auto_20190611_1638'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='channeltype',
            options={'permissions': (('deliver_ChannelType', 'Can deliver 渠道类型'),), 'verbose_name': '渠道类型', 'verbose_name_plural': '渠道类型管理'},
        ),
    ]
