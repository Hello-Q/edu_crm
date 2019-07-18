# Generated by Django 2.0 on 2019-07-13 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys', '0010_auto_20190713_1110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='role_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='role',
            old_name='role_name',
            new_name='name',
        ),
        migrations.AddField(
            model_name='role',
            name='type',
            field=models.IntegerField(choices=[(0, '普通'), (1, '客服'), (2, '课程顾问')], default=0, help_text="角色类型((0, '普通'), (1, '客服'), (2, '课程顾问'))", verbose_name='角色类型'),
        ),
    ]