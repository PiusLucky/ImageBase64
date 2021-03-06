# Generated by Django 3.0.1 on 2020-01-25 21:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20200125_2215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=100000, null=True, verbose_name='Email')),
                ('additional', models.TextField(blank=True, max_length=100000, null=True, verbose_name='Extra')),
                ('updated', models.DateTimeField(default=datetime.datetime(2020, 1, 25, 22, 23, 45, 700803))),
            ],
            options={
                'ordering': ['-updated'],
            },
        ),
        migrations.DeleteModel(
            name='CNT_Model',
        ),
        migrations.AlterField(
            model_name='faq_model',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 25, 22, 23, 45, 700803)),
        ),
        migrations.AlterField(
            model_name='update_model',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 25, 22, 23, 45, 700803)),
        ),
    ]
