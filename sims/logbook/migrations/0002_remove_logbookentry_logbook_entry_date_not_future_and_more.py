# Generated by Django 4.2.23 on 2025-06-24 19:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logbook", "0001_initial"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="logbookentry",
            name="logbook_entry_date_not_future",
        ),
        migrations.AddConstraint(
            model_name="logbookentry",
            constraint=models.CheckConstraint(
                check=models.Q(("date__lte", datetime.date(2025, 6, 24))),
                name="logbook_entry_date_not_future",
            ),
        ),
    ]
