# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 08:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0006_user_posts_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture_link', models.CharField(max_length=10000)),
                ('user_reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facebook.User')),
            ],
        ),
    ]
