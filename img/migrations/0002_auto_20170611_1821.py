# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-11 10:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('img', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='img',
            old_name='created_at',
            new_name='CreateDate',
        ),
    ]
