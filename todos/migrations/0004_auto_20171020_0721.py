# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-20 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0003_list_item_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list_item',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
