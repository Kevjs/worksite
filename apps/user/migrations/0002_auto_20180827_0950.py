# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-08-27 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='latest_message',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
