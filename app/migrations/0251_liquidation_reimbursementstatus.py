# Generated by Django 3.2.3 on 2022-01-03 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0250_auto_20211220_0159'),
    ]

    operations = [
        migrations.AddField(
            model_name='liquidation',
            name='reimbursementStatus',
            field=models.BooleanField(default=False),
        ),
    ]
