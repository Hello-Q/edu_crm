# Generated by Django 2.0 on 2019-07-25 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys', '0008_remove_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ManyToManyField(to='sys.Role', verbose_name='角色'),
        ),
    ]
