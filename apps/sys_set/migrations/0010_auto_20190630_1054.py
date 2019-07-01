# Generated by Django 2.0 on 2019-06-30 02:54

from django.db import migrations, models
import utils.storage


class Migration(migrations.Migration):

    dependencies = [
        ('sys_set', '0009_auto_20190628_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='nickname',
            field=models.CharField(default='张燕青', help_text='用户昵称', max_length=15, verbose_name='用户昵称'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='head_pic',
            field=models.ImageField(blank=True, null=True, storage=utils.storage.ImageStorage(), upload_to='img', verbose_name='图片url'),
        ),
    ]
