# Generated by Django 2.0 on 2019-05-31 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sys_set', '0001_initial'),
        ('edu_admin', '0002_auto_20190531_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='branchschool',
            name='org_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='sys_set.Organization'),
            preserve_default=False,
        ),
    ]