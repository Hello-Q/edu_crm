# Generated by Django 2.0 on 2019-06-03 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sys_set', '0004_auto_20190603_1638'),
        ('edu_admin', '0003_auto_20190603_1658'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clue', '0005_auto_20190603_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='clue',
            name='follow_up_people',
            field=models.ForeignKey(blank=True, help_text='跟进人', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='跟进人'),
        ),
        migrations.AddField(
            model_name='clue',
            name='intended_course',
            field=models.ForeignKey(blank=True, help_text='意向课程', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='edu_admin.Course', verbose_name='意向课程'),
        ),
        migrations.AddField(
            model_name='clue',
            name='intended_school',
            field=models.ForeignKey(blank=True, help_text='意向校区', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='sys_set.Department', verbose_name='意向小区'),
        ),
    ]
