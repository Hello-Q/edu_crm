# Generated by Django 2.0 on 2019-06-28 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys_set', '0007_userprofile_head_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='head_pic',
            field=models.ImageField(default=1, upload_to='static/images/%Y/%m/%d', verbose_name='图片url'),
            preserve_default=False,
        ),
    ]
