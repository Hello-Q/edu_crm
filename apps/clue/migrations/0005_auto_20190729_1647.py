# Generated by Django 2.0 on 2019-07-29 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sys', '0021_auto_20190729_1632'),
        ('clue', '0004_auto_20190729_1615'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='clue',
            unique_together={('tel', 'organization')},
        ),
    ]
