# Generated by Django 2.2.24 on 2022-03-29 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0005_remove_configurationfieldmodel_cantidad_sensores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configurationfieldmodel',
            name='id',
            field=models.SmallIntegerField(primary_key=True, serialize=False),
        ),
    ]
