# Generated by Django 2.0 on 2019-06-11 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clue', '0011_auto_20190611_1626'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='channeltype',
            options={'permissions': (('visit_渠道类型', 'Can visit channeltype'),), 'verbose_name': '渠道类型', 'verbose_name_plural': '渠道类型管理'},
        ),
    ]