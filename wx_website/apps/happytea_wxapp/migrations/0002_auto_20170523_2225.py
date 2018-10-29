# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('happytea_wxapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='id',
        ),
        migrations.AlterField(
            model_name='appuser',
            name='app_openid',
            field=models.CharField(max_length=128, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='user_id',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
