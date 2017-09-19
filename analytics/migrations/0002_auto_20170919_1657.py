# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-19 16:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='iplocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cip', models.CharField(max_length=50, unique=True)),
                ('ccity', models.CharField(blank=True, max_length=250)),
                ('ccountry', models.CharField(max_length=250)),
                ('clat', models.DecimalField(decimal_places=20, max_digits=40)),
                ('clon', models.DecimalField(decimal_places=20, max_digits=40)),
                ('cstate', models.CharField(max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='clickevent',
            name='req_ips',
            field=models.ManyToManyField(to='analytics.iplocation'),
        ),
    ]
