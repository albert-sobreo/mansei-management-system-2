# Generated by Django 3.2.3 on 2021-07-13 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0102_auto_20210713_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='warehouseItems',
            field=models.ManyToManyField(blank=True, to='app.WarehouseItems'),
        ),
    ]