# Generated by Django 2.2.24 on 2021-12-04 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherAPI', '0005_remove_historicweathermodel_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicweathermodel',
            name='humidity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='historicweathermodel',
            name='temperature',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='historicweathermodel',
            name='temperature_max',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='historicweathermodel',
            name='temperature_min',
            field=models.IntegerField(),
        ),
    ]
