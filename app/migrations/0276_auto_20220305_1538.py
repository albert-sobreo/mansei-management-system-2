# Generated by Django 3.2.3 on 2022-03-05 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0275_alter_merchandiseinventory_vol'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exportitemsmerch',
            old_name='pricePerCubic',
            new_name='sellingPrice',
        ),
        migrations.RenameField(
            model_name='qqitemsmerch',
            old_name='pricePerCubic',
            new_name='sellingPrice',
        ),
        migrations.RenameField(
            model_name='scitemsmerch',
            old_name='pricePerCubic',
            new_name='sellingPrice',
        ),
        migrations.RenameField(
            model_name='soitemsmerch',
            old_name='pricePerCubic',
            new_name='sellingPrice',
        ),
    ]
