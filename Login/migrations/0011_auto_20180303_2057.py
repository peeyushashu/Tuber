# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-03 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0010_song_is_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song_album',
            name='album_logo',
            field=models.FileField(upload_to=''),
        ),
    ]
