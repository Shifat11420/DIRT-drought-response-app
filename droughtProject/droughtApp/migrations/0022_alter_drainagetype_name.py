# Generated by Django 4.1.1 on 2023-04-03 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('droughtApp', '0021_rename_id_soilmoisture_indicator_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drainagetype',
            name='Name',
            field=models.CharField(max_length=50),
        ),
    ]
