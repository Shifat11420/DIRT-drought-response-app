# Generated by Django 4.1.7 on 2023-07-12 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('droughtApp', '0005_results_effectiverainamount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irrigation',
            name='FieldId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='droughtApp.field'),
        ),
        migrations.AlterField(
            model_name='results',
            name='FieldId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='droughtApp.field'),
        ),
    ]
