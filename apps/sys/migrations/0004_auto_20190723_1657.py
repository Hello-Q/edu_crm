# Generated by Django 2.0 on 2019-07-23 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys', '0003_role_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='data_permissions',
        ),
        migrations.AlterField(
            model_name='role',
            name='resource',
            field=models.ManyToManyField(blank=True, help_text='可访问资源', null=True, to='sys.Resource', verbose_name='可访问资源'),
        ),
    ]