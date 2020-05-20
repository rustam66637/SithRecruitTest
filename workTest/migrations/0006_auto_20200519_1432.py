# Generated by Django 3.0.4 on 2020-05-19 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workTest', '0005_auto_20200518_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruit',
            name='result',
        ),
        migrations.AddField(
            model_name='question',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Задавать ли'),
        ),
        migrations.AddField(
            model_name='recruit',
            name='reviewed',
            field=models.BooleanField(default=False, verbose_name='Отбор'),
        ),
    ]