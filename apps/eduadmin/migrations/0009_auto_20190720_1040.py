# Generated by Django 2.0 on 2019-07-20 02:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eduadmin', '0008_auto_20190720_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(default=1, help_text='员工id', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='教师姓名'),
            preserve_default=False,
        ),
    ]
