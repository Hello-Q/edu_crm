# Generated by Django 2.0 on 2019-07-26 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('sys', '0011_resource_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='group',
        ),
        migrations.AddField(
            model_name='role',
            name='name',
            field=models.CharField(default=1, help_text='角色名称', max_length=10, verbose_name='角色名称'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='拥有权限'),
        ),
    ]