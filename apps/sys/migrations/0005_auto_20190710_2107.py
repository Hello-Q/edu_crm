# Generated by Django 2.0 on 2019-07-10 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sys', '0004_auto_20190710_2106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='org',
            new_name='organization',
        ),
    ]