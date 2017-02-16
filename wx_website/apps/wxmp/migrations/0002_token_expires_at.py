# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wxmp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='expires_at',
            field=models.IntegerField(default=0),
        ),
    ]
