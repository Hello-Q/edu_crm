# Generated by Django 2.0 on 2019-07-04 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys', '0010_auto_20190704_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ManyToManyField(to='sys.Role', verbose_name='角色'),
        ),
    ]