# Generated by Django 2.0 on 2019-07-26 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('sys', '0010_auto_20190725_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='拥有权限'),
        ),
    ]