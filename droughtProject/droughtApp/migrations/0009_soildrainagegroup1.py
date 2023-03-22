# Generated by Django 4.1.1 on 2023-03-22 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('droughtApp', '0008_hydrologicgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='soilDrainageGroup1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptionForCN', models.CharField(max_length=30)),
                ('indicator', models.IntegerField()),
                ('A', models.IntegerField()),
                ('B', models.IntegerField()),
                ('C', models.IntegerField()),
                ('D', models.IntegerField()),
            ],
        ),
    ]
