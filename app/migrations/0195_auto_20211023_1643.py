# Generated by Django 3.2.3 on 2021-10-23 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0194_alter_payroll_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='phicemployeededuction',
            old_name='amount',
            new_name='ee',
        ),
        migrations.RemoveField(
            model_name='phiccontributionrate',
            name='rate',
        ),
        migrations.AddField(
            model_name='phiccontributionrate',
            name='ee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='phiccontributionrate',
            name='er',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='phicemployeededuction',
            name='er',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
    ]