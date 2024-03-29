# Generated by Django 4.1.7 on 2023-05-01 17:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('droughtApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='FieldCapacity',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='GrowingPeriodDays',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='PermanentWiltingPoint',
            field=models.FloatField(null=True),
        ),
        migrations.CreateModel(
            name='results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(blank=True, default=datetime.date(1111, 11, 11), null=True)),
                ('WaterLevelStart', models.FloatField(null=True)),
                ('WaterLevelEnd', models.FloatField(null=True)),
                ('DeepPercolation', models.FloatField(null=True)),
                ('SurfaceRunoff', models.FloatField(null=True)),
                ('VolumetricWaterContent', models.FloatField(null=True)),
                ('EffectiveIrrigation', models.FloatField(null=True)),
                ('IrrigationEfficiency', models.FloatField(null=True)),
                ('MaximumAvailableDepletion', models.FloatField(null=True)),
                ('FieldCapacity', models.FloatField(null=True)),
                ('PermanentWiltingPoint', models.FloatField(null=True)),
                ('WaterDeficit', models.FloatField(null=True)),
                ('IrrigationActivityAmount', models.FloatField(null=True)),
                ('RainObservedAmount', models.FloatField(null=True)),
                ('FieldId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='droughtApp.field')),
            ],
        ),
    ]
