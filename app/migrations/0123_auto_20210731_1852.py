# Generated by Django 3.2.3 on 2021-07-31 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0122_pritemsmerch_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pritemsmerch',
            name='type',
        ),
        migrations.AddField(
            model_name='pritemsother',
            name='type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
