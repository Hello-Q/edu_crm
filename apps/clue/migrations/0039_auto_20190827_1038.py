# Generated by Django 2.0 on 2019-08-27 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clue', '0038_auto_20190824_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clue',
            name='consult_date',
            field=models.DateField(auto_now_add=True, help_text='录入日期', verbose_name='录入日期'),
        ),
    ]