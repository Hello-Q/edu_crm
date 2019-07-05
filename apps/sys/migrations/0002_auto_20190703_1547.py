# Generated by Django 2.0 on 2019-07-03 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sys', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dep',
            field=models.ForeignKey(blank=True, help_text='部门id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='sys.Department', verbose_name='所属部门'),
        ),
    ]