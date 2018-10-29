# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('happytea', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacharge',
            name='add_type',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
