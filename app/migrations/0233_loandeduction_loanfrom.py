# Generated by Django 3.2.3 on 2021-11-19 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0232_alter_loans_amountpaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='loandeduction',
            name='loanFrom',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
