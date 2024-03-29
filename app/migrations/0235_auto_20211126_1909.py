# Generated by Django 3.2.3 on 2021-11-26 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0234_monthlyexpense'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('dateStart', models.DateField(blank=True, null=True)),
                ('dateEnd', models.DateField(blank=True, null=True)),
                ('dateCreated', models.DateField(blank=True, null=True)),
                ('dateCompleted', models.DateField(blank=True, null=True)),
                ('accentColor', models.CharField(blank=True, max_length=12, null=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projectplan', to='app.projectdepartment')),
                ('projectLeader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projectplan', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('accentColor', models.CharField(blank=True, max_length=12, null=True)),
                ('projectPlan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projectstage', to='app.projectplan')),
            ],
        ),
        migrations.AddField(
            model_name='branch',
            name='monthlyExpense',
            field=models.ManyToManyField(blank=True, to='app.MonthlyExpense'),
        ),
        migrations.AlterField(
            model_name='monthlyexpense',
            name='amount',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20),
        ),
        migrations.CreateModel(
            name='ProjectTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('datetimeStart', models.DateTimeField(blank=True, null=True)),
                ('datetimeEnd', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('projectStage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projecttask', to='app.projectstage')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectAssignee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectTask', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projectassignee', to='app.projecttask')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projectassignee', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
