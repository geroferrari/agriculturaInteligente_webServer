# Generated by Django 2.2.24 on 2022-03-31 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0007_configurationfieldmodel_cantidad_sensores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configurationfieldmodel',
            name='cantidad_sensores',
            field=models.IntegerField(blank=True),
        ),
    ]
