# Generated by Django 3.2.3 on 2021-12-19 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0248_auto_20211219_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='liquidation',
            field=models.ManyToManyField(blank=True, to='app.Liquidation'),
        ),
        migrations.AddField(
            model_name='branch',
            name='liquidationEntries',
            field=models.ManyToManyField(blank=True, to='app.LiquidationEntries'),
        ),
    ]
