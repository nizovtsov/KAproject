# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2021-02-02 13:46
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_auto_20210125_0855'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='billingprofile',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]