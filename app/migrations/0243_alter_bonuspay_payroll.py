# Generated by Django 3.2.3 on 2021-12-14 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0242_auto_20211213_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonuspay',
            name='payroll',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bonuspay', to='app.payroll'),
        ),
    ]
