# Generated by Django 2.0 on 2019-07-03 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sys', '0005_auto_20190703_1730'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='dep',
            new_name='department',
        ),
    ]
