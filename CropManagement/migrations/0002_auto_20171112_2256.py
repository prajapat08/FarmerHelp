# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-12 17:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CropManagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soilreport',
            name='uploaded_date',
            field=models.DateField(default=datetime.datetime(2017, 11, 12, 22, 56, 55, 607638)),
        ),
    ]
