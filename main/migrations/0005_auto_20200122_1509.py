# Generated by Django 3.0.1 on 2020-01-22 23:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200122_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update_model',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 22, 15, 9, 28, 417042)),
        ),
    ]
