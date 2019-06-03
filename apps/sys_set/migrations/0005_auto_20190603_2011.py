# Generated by Django 2.0.5 on 2019-06-03 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys_set', '0004_auto_20190603_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='department',
            name='del_flag',
            field=models.BooleanField(default=False, help_text='已删除', verbose_name='已删除'),
        ),
        migrations.AlterField(
            model_name='department',
            name='remark',
            field=models.CharField(blank=True, help_text='备注', max_length=150, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='department',
            name='update_time',
            field=models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='del_flag',
            field=models.BooleanField(default=False, help_text='已删除', verbose_name='已删除'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='remark',
            field=models.CharField(blank=True, help_text='备注', max_length=150, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='update_time',
            field=models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='del_flag',
            field=models.BooleanField(default=False, help_text='已删除', verbose_name='已删除'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='remark',
            field=models.CharField(blank=True, help_text='备注', max_length=150, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='update_time',
            field=models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间'),
        ),
    ]
