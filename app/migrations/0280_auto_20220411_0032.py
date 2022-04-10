# Generated by Django 3.2.3 on 2022-04-11 00:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0279_notifications_datetimecreated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manufacturinginventory',
            options={'verbose_name': 'Manufacturing Inventory', 'verbose_name_plural': 'Manufacturing Inventories'},
        ),
        migrations.AddField(
            model_name='cheques',
            name='party',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.party'),
        ),
        migrations.AddField(
            model_name='cheques',
            name='transactionCode',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
