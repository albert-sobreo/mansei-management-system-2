# Generated by Django 3.2.3 on 2021-10-10 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0173_auto_20211009_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dtr',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dtr', to=settings.AUTH_USER_MODEL),
        ),
    ]
