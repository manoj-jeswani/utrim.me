# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-10 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0008_urlss_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlss',
            name='tag',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
