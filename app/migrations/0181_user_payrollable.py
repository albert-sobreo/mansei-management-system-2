# Generated by Django 3.2.3 on 2021-10-16 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0180_bonusofuser_bonuspay_deminimisofuser_deminimispay'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='payrollable',
            field=models.BooleanField(default=True),
        ),
    ]