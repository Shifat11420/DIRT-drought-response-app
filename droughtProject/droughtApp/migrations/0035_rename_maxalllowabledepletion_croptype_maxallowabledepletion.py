# Generated by Django 4.1.7 on 2023-04-10 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("droughtApp", "0034_field_elevation"),
    ]

    operations = [
        migrations.RenameField(
            model_name="croptype",
            old_name="MaxAlllowableDepletion",
            new_name="MaxAllowableDepletion",
        ),
    ]
