# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-25 19:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0006_auto_20180226_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song_album',
            name='album_logo',
            field=models.ImageField(upload_to='../MyPro/Login/song_album_id/album_logo'),
        ),
    ]
