# Generated by Django 2.0 on 2019-07-10 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sys', '0003_auto_20190710_2051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='dep_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='dep_type',
            new_name='type',
        ),
    ]
