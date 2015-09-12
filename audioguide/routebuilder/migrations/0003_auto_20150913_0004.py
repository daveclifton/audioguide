# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routebuilder', '0002_auto_20150908_1159'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='route',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='waypoint',
            options={'ordering': ['route_id', 'seq']},
        ),
        migrations.AlterField(
            model_name='route',
            name='cover_image',
            field=models.CharField(max_length=160, verbose_name=b'cover image'),
        ),
        migrations.AlterField(
            model_name='route',
            name='description',
            field=models.CharField(max_length=2000, verbose_name=b'description'),
        ),
        migrations.AlterField(
            model_name='waypoint',
            name='description',
            field=models.CharField(max_length=2000, verbose_name=b'description'),
        ),
        migrations.AlterField(
            model_name='waypoint',
            name='image',
            field=models.CharField(max_length=160, verbose_name=b'image'),
        ),
    ]
