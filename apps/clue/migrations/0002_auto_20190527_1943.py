# Generated by Django 2.0.5 on 2019-05-27 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clue',
            name='add',
            field=models.CharField(help_text='年龄', max_length=40),
        ),
        migrations.AlterField(
            model_name='clue',
            name='age',
            field=models.IntegerField(),
        ),
    ]
