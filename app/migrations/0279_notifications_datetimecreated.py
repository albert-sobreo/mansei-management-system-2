# Generated by Django 3.2.3 on 2022-04-06 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0278_errorlogs'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='datetimeCreated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
