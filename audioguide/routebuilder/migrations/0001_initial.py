# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=40, verbose_name=b'title')),
                ('description', models.CharField(max_length=500, verbose_name=b'description')),
                ('color', models.CharField(max_length=7, verbose_name=b'color')),
                ('cover_image', models.CharField(max_length=40, verbose_name=b'cover image')),
                ('timestamp', models.DateTimeField(verbose_name=b'last updated')),
            ],
        ),
        migrations.CreateModel(
            name='Waypoint',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('seq', models.IntegerField(verbose_name=b'sequence')),
                ('title', models.CharField(max_length=40, verbose_name=b'title')),
                ('description', models.CharField(max_length=500, verbose_name=b'description')),
                ('lat', models.FloatField(verbose_name=b'latitude')),
                ('lng', models.FloatField(verbose_name=b'longitude')),
                ('image', models.CharField(max_length=120, verbose_name=b'image')),
                ('audio_file', models.CharField(max_length=120, verbose_name=b'audio file')),
                ('route_id', models.ForeignKey(to='routebuilder.Route')),
            ],
        ),
    ]
