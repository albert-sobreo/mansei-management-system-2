# Generated by Django 3.2.3 on 2021-06-27 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0059_alter_poitemsmerch_qtyreceived'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='qqitemsmerch',
            options={'verbose_name': 'QQ Items Merch', 'verbose_name_plural': 'QQ Items Merchs'},
        ),
        migrations.AlterModelOptions(
            name='quotations',
            options={'verbose_name': 'Quotation', 'verbose_name_plural': 'Quotations'},
        ),
        migrations.AddField(
            model_name='qqitemsmerch',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=18, null=True),
        ),
    ]
