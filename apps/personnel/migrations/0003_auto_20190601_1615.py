# Generated by Django 2.0 on 2019-06-01 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0002_auto_20190601_1537'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': '部门', 'verbose_name_plural': '部门管理'},
        ),
        migrations.AlterField(
            model_name='department',
            name='superior_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='personnel.Department'),
        ),
    ]
