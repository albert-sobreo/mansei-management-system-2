# Generated by Django 3.2.3 on 2021-10-04 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0166_holiday_leaverequest_otrequest_timesheet_timesheetdaycategory_utrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='holiday',
            field=models.ManyToManyField(blank=True, to='app.Holiday'),
        ),
        migrations.AddField(
            model_name='branch',
            name='leaveRequest',
            field=models.ManyToManyField(blank=True, to='app.LeaveRequest'),
        ),
        migrations.AddField(
            model_name='branch',
            name='otRequest',
            field=models.ManyToManyField(blank=True, to='app.OTRequest'),
        ),
        migrations.AddField(
            model_name='branch',
            name='timesheet',
            field=models.ManyToManyField(blank=True, to='app.Timesheet'),
        ),
        migrations.AddField(
            model_name='branch',
            name='timesheetDayCategory',
            field=models.ManyToManyField(blank=True, to='app.TimesheetDayCategory'),
        ),
        migrations.AddField(
            model_name='branch',
            name='utRequest',
            field=models.ManyToManyField(blank=True, to='app.UTRequest'),
        ),
    ]
