# Generated by Django 3.0.1 on 2020-01-25 09:06

import datetime
from django.db import migrations, models
import main.utils


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20200123_2236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Q1', models.TextField(max_length=100000, verbose_name='Question One')),
                ('Q2', models.TextField(max_length=100000, verbose_name='Question Two')),
                ('Q3', models.TextField(max_length=100000, verbose_name='Question Three')),
                ('Q4', models.TextField(max_length=100000, verbose_name='Question Four')),
                ('Q5', models.TextField(max_length=100000, verbose_name='Question Five')),
                ('Q6', models.TextField(max_length=100000, verbose_name='Question Six')),
                ('Q7', models.TextField(max_length=100000, verbose_name='Question Seven')),
                ('Q8', models.TextField(max_length=100000, verbose_name='Question Eight')),
                ('Q9', models.TextField(max_length=100000, verbose_name='Question Nine')),
                ('Q10', models.TextField(max_length=100000, verbose_name='Question Ten')),
                ('created', models.DateTimeField(default=datetime.datetime(2020, 1, 25, 10, 6, 47, 601301))),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.RemoveField(
            model_name='link_model',
            name='slug',
        ),
        migrations.AlterField(
            model_name='link_model',
            name='unique_id_link',
            field=models.CharField(default=main.utils.generate_unique_id_link, max_length=28, verbose_name='unique_link_encode'),
        ),
        migrations.AlterField(
            model_name='update_model',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 25, 10, 6, 47, 598301)),
        ),
    ]
