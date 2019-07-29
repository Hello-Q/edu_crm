# Generated by Django 2.0 on 2019-07-27 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sys', '0019_auto_20190726_1550'),
        ('clue', '0002_auto_20190723_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clue',
            name='intended_school',
        ),
        migrations.AddField(
            model_name='clue',
            name='intended_school',
            field=models.ForeignKey(blank=True, help_text='意向校区', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clue_intended_school', to='sys.Department', verbose_name='意向校区'),
        ),
    ]