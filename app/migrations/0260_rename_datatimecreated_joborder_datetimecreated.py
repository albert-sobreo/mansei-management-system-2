# Generated by Django 3.2.3 on 2022-01-25 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0259_auto_20220125_1734'),
    ]

    operations = [
        migrations.RenameField(
            model_name='joborder',
            old_name='datatimeCreated',
            new_name='datetimeCreated',
        ),
    ]