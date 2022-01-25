# Generated by Django 3.2.3 on 2022-01-19 21:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0253_branch_deminimis'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('datetimeCreated', models.DateTimeField()),
                ('dateSold', models.DateField()),
                ('amountPaid', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('amountDue', models.DecimalField(decimal_places=5, max_digits=20, null=True)),
                ('amountTotal', models.DecimalField(decimal_places=5, max_digits=20)),
                ('discountPercent', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('discountPeso', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('taxType', models.CharField(blank=True, max_length=20, null=True)),
                ('taxRate', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('taxPeso', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('paymentMethod', models.CharField(blank=True, max_length=50, null=True)),
                ('paymentPeriod', models.CharField(blank=True, max_length=50, null=True)),
                ('chequeNo', models.CharField(blank=True, max_length=50, null=True)),
                ('dueDate', models.DateField(blank=True, null=True)),
                ('bank', models.CharField(blank=True, max_length=50, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('datetimeApproved', models.DateTimeField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False, null=True)),
                ('voided', models.BooleanField(default=False, null=True)),
                ('datetimeVoided', models.DateTimeField(blank=True, null=True)),
                ('fullyPaid', models.BooleanField(blank=True, default=False, null=True)),
                ('runningBalance', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('wep', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('approvedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exportsapprovedby', to=settings.AUTH_USER_MODEL)),
                ('createdBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exportscreatedby', to=settings.AUTH_USER_MODEL)),
                ('journal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exports', to='app.journal')),
                ('party', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exports', to='app.party')),
                ('voidedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exportsvoidedby', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Export',
                'verbose_name_plural': 'Exports',
            },
        ),
        migrations.CreateModel(
            name='ExportOtherFees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.DecimalField(decimal_places=5, max_digits=20)),
                ('description', models.CharField(max_length=255, null=True)),
                ('export', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exportotherfees', to='app.exports')),
            ],
        ),
        migrations.CreateModel(
            name='ExportItemsMerch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remaining', models.IntegerField()),
                ('qty', models.IntegerField()),
                ('cbm', models.CharField(max_length=10, null=True)),
                ('vol', models.DecimalField(decimal_places=5, max_digits=20, null=True)),
                ('pricePerCubic', models.DecimalField(decimal_places=5, max_digits=20, null=True)),
                ('totalCost', models.DecimalField(decimal_places=5, max_digits=20, null=True)),
                ('delivered', models.BooleanField(default=False, null=True)),
                ('export', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exportitemsmerch', to='app.exports')),
                ('merchInventory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exportitemsmerch', to='app.merchandiseinventory')),
            ],
            options={
                'verbose_name': 'Export Items Merch',
                'verbose_name_plural': 'Export Items Merchs',
            },
        ),
        migrations.CreateModel(
            name='Exportatc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amountWithheld', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exportatc', to='app.atc')),
                ('export', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exportatc', to='app.exports')),
            ],
        ),
    ]