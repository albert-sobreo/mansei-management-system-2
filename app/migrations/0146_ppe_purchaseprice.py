# Generated by Django 3.2.3 on 2021-09-13 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0145_repairandmaintenance_capitalized'),
    ]

    operations = [
        migrations.AddField(
            model_name='ppe',
            name='purchasePrice',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True),
        ),
    ]
