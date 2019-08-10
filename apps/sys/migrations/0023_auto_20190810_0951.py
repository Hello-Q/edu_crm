# Generated by Django 2.0 on 2019-08-10 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys', '0022_user_qywxid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datapermissions',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='datapermissions',
            name='operator',
        ),
        migrations.RemoveField(
            model_name='datapermissions',
            name='organization',
        ),
        migrations.AddField(
            model_name='role',
            name='data_permissions',
            field=models.IntegerField(choices=[(0, '个人数据'), (1, '部门数据'), (2, '公司数据')], default=1, verbose_name='可访问数据'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='DataPermissions',
        ),
    ]
