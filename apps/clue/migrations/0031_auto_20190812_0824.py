# Generated by Django 2.0 on 2019-08-12 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clue', '0030_auto_20190812_0824'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='channeltype',
            options={'permissions': (('view_channeltype', 'Can view 渠道类型'),), 'verbose_name': '渠道类型', 'verbose_name_plural': '渠道类型管理'},
        ),
    ]
