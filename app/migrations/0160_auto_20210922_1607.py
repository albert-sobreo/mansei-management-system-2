# Generated by Django 3.2.3 on 2021-09-22 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0159_completionreport_crvendors'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='completionReport',
            field=models.ManyToManyField(blank=True, to='app.CompletionReport'),
        ),
        migrations.AddField(
            model_name='branch',
            name='crVendors',
            field=models.ManyToManyField(blank=True, to='app.CRVendors'),
        ),
        migrations.AlterField(
            model_name='crvendors',
            name='cr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='crvendors', to='app.completionreport'),
        ),
        migrations.AlterField(
            model_name='crvendors',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='crvendors', to='app.party'),
        ),
    ]
