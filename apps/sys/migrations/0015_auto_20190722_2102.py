# Generated by Django 2.0 on 2019-07-22 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys', '0014_auto_20190722_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='type',
            field=models.IntegerField(choices=[(0, '分公司'), (1, '校区'), (2, '部门')], default=2, verbose_name='类型'),
            preserve_default=False,
        ),
    ]