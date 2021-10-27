# Generated by Django 3.2.3 on 2021-10-27 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0203_auto_20211027_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incometaxtable',
            name='fixedDeduction',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=16, null=True),
        ),
        migrations.AlterField(
            model_name='incometaxtable',
            name='lowerLimit',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=16, null=True),
        ),
        migrations.AlterField(
            model_name='incometaxtable',
            name='percentDeduction',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='incometaxtable',
            name='upperLimit',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=16, null=True),
        ),
    ]
