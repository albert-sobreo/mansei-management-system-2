# Generated by Django 3.2.3 on 2021-06-24 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_auto_20210620_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchandiseinventory',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
