# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_user_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
