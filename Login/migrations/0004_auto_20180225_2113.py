# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-25 15:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0003_auto_20180225_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song_album',
            name='album_logo',
            field=models.ImageField(upload_to='..\\Login\\Static\\lbum_logo'),
        ),
    ]
