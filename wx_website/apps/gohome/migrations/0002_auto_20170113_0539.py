# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gohome', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='end_station',
            field=models.CharField(default=b'', max_length=256),
        ),
        migrations.AddField(
            model_name='account',
            name='from_station',
            field=models.CharField(default=b'', max_length=256),
        ),
        migrations.AddField(
            model_name='account',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
