# Generated by Django 2.0 on 2019-06-03 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edu_admin', '0002_auto_20190603_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branchschool',
            name='org_id',
        ),
        migrations.DeleteModel(
            name='BranchSchool',
        ),
    ]
