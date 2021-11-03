# Generated by Django 3.2.3 on 2021-10-23 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0189_pagibigcontributionrate_pagibigemployeecontribution_phiccontributionrate_phicemployeededuction_sssco'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='pagibigEmployeeContribution',
            field=models.ManyToManyField(blank=True, to='app.PagibigEmployeeContribution'),
        ),
        migrations.AddField(
            model_name='branch',
            name='phicEmployeeDeduction',
            field=models.ManyToManyField(blank=True, to='app.PHICEmployeeDeduction'),
        ),
        migrations.AddField(
            model_name='branch',
            name='sssEmployeeDeduction',
            field=models.ManyToManyField(blank=True, to='app.SSSEmployeeDeduction'),
        ),
    ]