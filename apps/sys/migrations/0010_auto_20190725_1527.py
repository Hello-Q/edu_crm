# Generated by Django 2.0 on 2019-07-25 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys', '0009_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ManyToManyField(blank=True, to='sys.Role', verbose_name='角色'),
        ),
    ]
