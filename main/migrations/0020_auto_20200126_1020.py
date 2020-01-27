# Generated by Django 3.0.1 on 2020-01-26 09:20

import datetime
from django.db import migrations, models
import main.utils


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20200125_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_Me_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100000, null=True, verbose_name='Name')),
                ('email', models.EmailField(blank=True, max_length=100000, null=True, verbose_name='Email')),
                ('whatsapp_contact', models.CharField(blank=True, max_length=100000, null=True, verbose_name='Whatsapp')),
                ('query', models.TextField(blank=True, max_length=100000, null=True, verbose_name='QUery')),
                ('seven_digit_auth_code', models.CharField(default=main.utils.auth_code, max_length=30, verbose_name='auth_code')),
                ('seven_digit_auth_code_enter', models.CharField(max_length=30, verbose_name='auth_code_enter')),
                ('updated', models.DateTimeField(default=datetime.datetime(2020, 1, 26, 10, 20, 2, 523144))),
            ],
            options={
                'ordering': ['-updated'],
            },
        ),
        migrations.CreateModel(
            name='My_Contact_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100000, null=True, verbose_name='Name')),
                ('email', models.EmailField(blank=True, max_length=100000, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=100000, null=True, verbose_name='Phone')),
                ('address', models.TextField(blank=True, max_length=100000, null=True, verbose_name='Address')),
                ('additional', models.TextField(blank=True, max_length=100000, null=True, verbose_name='Extra')),
                ('updated', models.DateTimeField(default=datetime.datetime(2020, 1, 26, 10, 20, 2, 523144))),
            ],
            options={
                'ordering': ['-updated'],
            },
        ),
        migrations.CreateModel(
            name='Resubmit_Ticket_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_id', models.CharField(blank=True, max_length=100000, null=True, verbose_name='Name')),
                ('seven_digit_auth_code', models.CharField(default=main.utils.auth_code, max_length=30, verbose_name='auth_code')),
                ('seven_digit_auth_code_enter', models.CharField(max_length=30, verbose_name='auth_code_enter')),
                ('created', models.DateTimeField(default=datetime.datetime(2020, 1, 26, 10, 20, 2, 523144))),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.DeleteModel(
            name='Contact_Model',
        ),
        migrations.AlterField(
            model_name='faq_model',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 26, 10, 20, 2, 523144)),
        ),
        migrations.AlterField(
            model_name='update_model',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 26, 10, 20, 2, 523144)),
        ),
    ]
