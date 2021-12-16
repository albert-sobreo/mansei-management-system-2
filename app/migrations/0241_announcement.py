# Generated by Django 3.2.3 on 2021-12-11 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0240_notepad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('contents', models.TextField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branchannouncement', to='app.branch')),
            ],
        ),
    ]