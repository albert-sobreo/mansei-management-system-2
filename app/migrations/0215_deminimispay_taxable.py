# Generated by Django 3.2.3 on 2021-11-02 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0214_alter_deminimisofuser_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='deminimispay',
            name='taxable',
            field=models.BooleanField(default=False),
        ),
    ]
