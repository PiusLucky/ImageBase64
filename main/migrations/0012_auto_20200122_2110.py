# Generated by Django 3.0.1 on 2020-01-23 05:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20200122_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update_model',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 22, 21, 10, 33, 958013)),
        ),
    ]
