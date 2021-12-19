# Generated by Django 3.2.3 on 2021-12-20 01:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0249_auto_20211219_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='liquidation',
            name='change',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='liquidation',
            name='payable',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='liquidationentries',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.party'),
        ),
    ]
