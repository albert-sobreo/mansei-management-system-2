# Generated by Django 3.2.3 on 2021-07-02 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0074_alter_branchdefaultchildaccount_advancestosupplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, null=True)),
                ('datetimeCreated', models.DateTimeField(null=True)),
                ('paymentDate', models.DateField(null=True)),
                ('remarks', models.TextField(null=True)),
                ('datetimeApproved', models.DateTimeField(null=True)),
                ('paymentMethod', models.CharField(max_length=50, null=True)),
                ('wep', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('amountPaid', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('approvedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='siApprovedBy', to=settings.AUTH_USER_MODEL)),
                ('createdBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='siCreatedBy', to=settings.AUTH_USER_MODEL)),
                ('journal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='salesinvoice', to='app.journal')),
                ('salesContract', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='salesinvoice', to='app.salescontract')),
                ('salesOrder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='salesinvoice', to='app.salesorder')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentVoucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, null=True)),
                ('datetimeCreated', models.DateTimeField(null=True)),
                ('paymentDate', models.DateField(null=True)),
                ('remarks', models.TextField(null=True)),
                ('datetimeApproved', models.DateTimeField(null=True)),
                ('paymentMethod', models.CharField(max_length=50, null=True)),
                ('wep', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('amountPaid', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('approvedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vApprovedBy', to=settings.AUTH_USER_MODEL)),
                ('createdBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vCreatedBy', to=settings.AUTH_USER_MODEL)),
                ('journal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='paymentvoucher', to='app.journal')),
                ('purchaseOrder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='paymentvoucher', to='app.purchaseorder')),
                ('receivingReport', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='paymentvoucher', to='app.receivingreport')),
            ],
        ),
        migrations.AddField(
            model_name='branch',
            name='paymentVoucher',
            field=models.ManyToManyField(blank=True, to='app.PaymentVoucher'),
        ),
        migrations.AddField(
            model_name='branch',
            name='salesInvoice',
            field=models.ManyToManyField(blank=True, to='app.SalesInvoice'),
        ),
    ]
