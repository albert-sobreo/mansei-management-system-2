# Generated by Django 3.2.3 on 2021-09-18 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0155_quotations_qqd'),
    ]

    operations = [
        migrations.AddField(
            model_name='qqitemsmerch',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='qqitemsmerch', to='app.warehouse'),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='soed',
            field=models.BooleanField(default=False, null=True),
        ),
    ]