# Generated by Django 2.0 on 2019-08-11 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clue', '0025_auto_20190810_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clue',
            name='status',
            field=models.IntegerField(choices=[(0, '待跟进'), (1, '待联系'), (2, '已约访'), (3, '已到访'), (4, '无法成交'), (5, '已报名')], default=0, help_text="线索状态((0, '待跟进'), (1, '待联系'), (2, '已约访'), (3, '已到访'), (4, '无法成交'), (5, '已报名'))", verbose_name='线索状态'),
        ),
    ]