# Generated by Django 3.2.3 on 2022-02-06 17:09

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0270_auto_20220203_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturinginventory',
            name='qtyA',
            field=models.IntegerField(default=Decimal('0')),
        ),
        migrations.AddField(
            model_name='manufacturinginventory',
            name='qtyR',
            field=models.IntegerField(default=Decimal('0')),
        ),
        migrations.AddField(
            model_name='manufacturinginventory',
            name='qtyT',
            field=models.IntegerField(default=Decimal('0')),
        ),
    ]
