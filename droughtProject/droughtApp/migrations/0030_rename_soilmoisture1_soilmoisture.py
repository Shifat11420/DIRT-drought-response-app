# Generated by Django 4.1.7 on 2023-04-10 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("droughtApp", "0029_rename_cropperiod1_cropperiod"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="soilMoisture1",
            new_name="soilMoisture",
        ),
    ]
