# Generated by Django 3.2.3 on 2021-06-15 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20210615_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='amountTotal',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=18),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='atcCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.atc'),
        ),
        migrations.AlterField(
            model_name='salescontract',
            name='atcCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.atc'),
        ),
    ]
