# Generated by Django 2.0 on 2019-07-11 01:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clue', '0016_auto_20190710_2201'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='channel',
            options={'ordering': ['id'], 'verbose_name': '渠道', 'verbose_name_plural': '渠道管理'},
        ),
        migrations.RenameField(
            model_name='channel',
            old_name='channel_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='channel',
            old_name='channel_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='channel',
            name='channel_type',
        ),
        migrations.AddField(
            model_name='channel',
            name='type',
            field=models.ForeignKey(help_text='渠道分类id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='clue.ChannelType', verbose_name='渠道分类'),
        ),
        migrations.AlterField(
            model_name='visit',
            name='date',
            field=models.DateField(help_text='安排日期', verbose_name='日期'),
        ),
        migrations.AlterField(
            model_name='visit',
            name='time',
            field=models.TimeField(help_text='安排时间', verbose_name='时间'),
        ),
    ]
