# Generated by Django 2.0 on 2019-07-23 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('sys', '0002_auto_20190723_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='group',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]
