# Generated by Django 2.0 on 2019-08-09 03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clue', '0017_auto_20190808_1557'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visit',
            options={'ordering': ['-create_time']},
        ),
    ]
