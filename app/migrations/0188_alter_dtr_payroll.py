# Generated by Django 3.2.3 on 2021-10-17 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0187_auto_20211017_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dtr',
            name='payroll',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dtr', to='app.payroll'),
        ),
    ]
