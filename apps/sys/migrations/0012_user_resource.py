# Generated by Django 2.0 on 2019-07-04 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sys', '0011_auto_20190704_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='resource',
            field=models.ForeignKey(blank=True, help_text='拥有资源', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='sys.Resource', verbose_name='拥有资源'),
        ),
    ]