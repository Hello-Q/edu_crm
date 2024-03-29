# Generated by Django 2.0 on 2019-08-09 06:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eduadmin', '0005_auto_20190803_1720'),
        ('clue', '0018_auto_20190809_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='clue',
            name='class_hour',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clue',
            name='enroll_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='eduadmin.Course', verbose_name='报名课程'),
        ),
        migrations.AddField(
            model_name='clue',
            name='enroll_date',
            field=models.DateField(blank=True, null=True, verbose_name='报名日期'),
        ),
        migrations.AddField(
            model_name='clue',
            name='enroll_sum',
            field=models.FloatField(blank=True, null=True, verbose_name='报名价格'),
        ),
        migrations.AlterField(
            model_name='clue',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clue_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建人'),
        ),
        migrations.AlterField(
            model_name='clue',
            name='operator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clue_operator', to=settings.AUTH_USER_MODEL, verbose_name='更新人'),
        ),
    ]
