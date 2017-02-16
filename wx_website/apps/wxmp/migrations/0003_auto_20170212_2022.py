# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wxmp', '0002_token_expires_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='appinfo',
            name='aes_key',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='appinfo',
            name='token',
            field=models.CharField(default='', max_length=128),
        ),
    ]
