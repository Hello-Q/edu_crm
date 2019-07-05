# Generated by Django 2.0 on 2019-07-05 03:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eduadmin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.ForeignKey(blank=True, help_text='员工id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='教师姓名'),
        ),
        migrations.AddField(
            model_name='course',
            name='subjects',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='eduadmin.Subjects', verbose_name='科系'),
        ),
    ]
