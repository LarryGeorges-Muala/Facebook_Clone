# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0008_user_msg'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_msg',
            name='respond_to',
            field=models.IntegerField(default=0),
        ),
    ]
