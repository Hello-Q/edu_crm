# Generated by Django 2.0 on 2019-08-27 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clue', '0039_auto_20190827_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clue',
            name='consult_date',
            field=models.DateField(auto_now_add=True, help_text='录入日期', null=True, verbose_name='录入日期'),
        ),
    ]
