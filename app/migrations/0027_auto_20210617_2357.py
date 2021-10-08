# Generated by Django 3.2.3 on 2021-06-17 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20210617_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='taxRate',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='taxType',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
