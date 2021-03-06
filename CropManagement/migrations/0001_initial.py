# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-12 17:25
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0006_compensate_for_0003_bytestring_bug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CropNutrient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organic_carbon', models.FloatField(blank=True, default=0)),
                ('available_nitrogen', models.FloatField(blank=True, default=0)),
                ('available_phosphorus', models.FloatField(blank=True, default=0)),
                ('available_potassium', models.FloatField(blank=True, default=0)),
                ('available_zinc', models.FloatField(blank=True, default=0)),
                ('available_boron', models.FloatField(blank=True, default=0)),
                ('available_iron', models.FloatField(blank=True, default=0)),
                ('available_manganese', models.FloatField(blank=True, default=0)),
                ('available_copper', models.FloatField(blank=True, default=0)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CropManagement.Crop')),
            ],
        ),
        migrations.CreateModel(
            name='CropWeather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_temperature', models.FloatField(default=0)),
                ('max_temperature', models.FloatField(default=0)),
                ('min_rainfall', models.FloatField(default=0)),
                ('max_rainfall', models.FloatField(default=0)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CropManagement.Crop')),
            ],
        ),
        migrations.CreateModel(
            name='farm',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('farm_name', models.CharField(max_length=100)),
                ('farm_area', models.FloatField()),
                ('crop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CropManagement.Crop')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities_light.City')),
            ],
        ),
        migrations.CreateModel(
            name='MobileRemainder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_no', models.PositiveIntegerField()),
                ('water_remind', models.TimeField()),
                ('harvest_remind', models.DateField()),
                ('pesticide_remind', models.TimeField()),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CropManagement.farm')),
            ],
        ),
        migrations.CreateModel(
            name='SoilReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_date', models.DateField(default=datetime.datetime(2017, 11, 12, 22, 55, 13, 663107))),
                ('soil_report', models.CharField(max_length=100)),
                ('pH', models.FloatField()),
                ('EC', models.FloatField()),
                ('organic_carbon', models.FloatField(blank=True, default=0)),
                ('available_nitrogen', models.FloatField(blank=True, default=0)),
                ('available_phosphorus', models.FloatField(blank=True, default=0)),
                ('available_potassium', models.FloatField(blank=True, default=0)),
                ('available_zinc', models.FloatField(blank=True, default=0)),
                ('available_boron', models.FloatField(blank=True, default=0)),
                ('available_iron', models.FloatField(blank=True, default=0)),
                ('available_manganese', models.FloatField(blank=True, default=0)),
                ('available_copper', models.FloatField(blank=True, default=0)),
                ('farm_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='that_farm', to='CropManagement.farm')),
            ],
        ),
        migrations.CreateModel(
            name='StateWeather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avg_temperature', models.FloatField(default=0)),
                ('avg_rainfall', models.FloatField(default=0)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities_light.Region')),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(blank=True, max_length=120)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='soilreport',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mobileremainder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='farm',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='soilreport',
            unique_together=set([('soil_report', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='farm',
            unique_together=set([('farm_name', 'user')]),
        ),
    ]
