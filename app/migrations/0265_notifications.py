# Generated by Django 3.2.3 on 2022-01-30 22:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0264_branch_directlabor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Notification Title', max_length=1024)),
                ('subject', models.CharField(default='Notification Subject', max_length=1024)),
                ('url', models.URLField()),
                ('read', models.BooleanField(default=False)),
                ('authLevel', models.CharField(blank=True, max_length=2, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]