# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-09-27 03:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170927_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar/default.png', max_length=200, upload_to='uploads/avatar/%Y/%m', verbose_name='\u5934\u50cf'),
        ),
    ]
