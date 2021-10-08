# Generated by Django 3.2.3 on 2021-06-28 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0062_auto_20210628_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='iiadjusteditems',
            name='amount',
            field=models.DecimalField(decimal_places=5, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='iiadjusteditems',
            name='length',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='iiadjusteditems',
            name='thicc',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='iiadjusteditems',
            name='vol',
            field=models.DecimalField(decimal_places=5, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='iiadjusteditems',
            name='width',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='iiitemsmerch',
            name='amount',
            field=models.DecimalField(decimal_places=5, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='iiitemsmerch',
            name='length',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='iiitemsmerch',
            name='thicc',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='iiitemsmerch',
            name='vol',
            field=models.DecimalField(decimal_places=5, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='iiitemsmerch',
            name='width',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
