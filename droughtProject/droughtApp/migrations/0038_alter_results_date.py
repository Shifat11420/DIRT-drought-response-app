# Generated by Django 4.1.1 on 2023-05-01 15:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('droughtApp', '0037_results'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='Date',
            field=models.DateField(blank=True, default=datetime.date(1111, 11, 11), null=True),
        ),
    ]
