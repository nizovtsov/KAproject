# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2021-01-25 12:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GuestEmails',
            new_name='GuestEmail',
        ),
    ]
