# Generated by Django 2.0 on 2019-07-23 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eduadmin', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(help_text='员工id', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='对应员工'),
        ),
        migrations.AddField(
            model_name='course',
            name='subjects',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='eduadmin.Subjects', verbose_name='科系'),
        ),
    ]