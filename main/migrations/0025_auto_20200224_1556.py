# Generated by Django 3.0.1 on 2020-02-24 14:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20200224_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_me_model',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 24, 15, 56, 56, 499601)),
        ),
        migrations.AlterField(
            model_name='faq_model',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 24, 15, 56, 56, 493603)),
        ),
        migrations.AlterField(
            model_name='my_contact_model',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 24, 15, 56, 56, 496603)),
        ),
        migrations.AlterField(
            model_name='update_model',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 24, 15, 56, 56, 490601)),
        ),
    ]
