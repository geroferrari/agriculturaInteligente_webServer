# Generated by Django 2.2.24 on 2022-03-31 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0009_auto_20220331_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configurationfieldmodel',
            name='cantidad_sensores',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
