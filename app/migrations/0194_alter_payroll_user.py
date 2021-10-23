# Generated by Django 3.2.3 on 2021-10-23 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0193_alter_phiccontributionrate_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payroll',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payroll', to=settings.AUTH_USER_MODEL),
        ),
    ]
