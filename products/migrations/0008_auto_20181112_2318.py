# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-12 20:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20181112_2222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='slag',
            new_name='slug',
        ),
    ]
