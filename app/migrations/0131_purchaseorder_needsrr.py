# Generated by Django 3.2.3 on 2021-08-02 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0130_merge_0121_merge_20210731_2131_0129_rritemsother_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='needsRR',
            field=models.BooleanField(default=True),
        ),
    ]
