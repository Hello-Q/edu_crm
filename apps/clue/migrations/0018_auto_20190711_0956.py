# Generated by Django 2.0 on 2019-07-11 01:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clue', '0017_auto_20190711_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='type',
            field=models.ForeignKey(default=1, help_text='渠道分类id', on_delete=django.db.models.deletion.CASCADE, to='clue.ChannelType', verbose_name='渠道分类'),
            preserve_default=False,
        ),
    ]