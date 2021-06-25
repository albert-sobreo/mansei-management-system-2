# Generated by Django 3.2.3 on 2021-06-25 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_scatc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scitemsmerch',
            name='outputVat',
        ),
        migrations.RemoveField(
            model_name='scitemsmerch',
            name='purchasingPrice',
        ),
        migrations.RemoveField(
            model_name='scitemsmerch',
            name='totalPrice',
        ),
        migrations.AddField(
            model_name='scitemsmerch',
            name='cbm',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='scitemsmerch',
            name='pricePerCubic',
            field=models.DecimalField(decimal_places=5, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='scitemsmerch',
            name='totalCost',
            field=models.DecimalField(decimal_places=5, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='scitemsmerch',
            name='vol',
            field=models.DecimalField(decimal_places=5, max_digits=10, null=True),
        ),
    ]
