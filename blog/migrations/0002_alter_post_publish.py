# Generated by Django 4.1 on 2022-12-18 03:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 18, 3, 54, 23, 869608, tzinfo=datetime.timezone.utc)),
        ),
    ]
