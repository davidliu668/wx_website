# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('passwd', models.CharField(max_length=32)),
                ('remark', models.CharField(max_length=256)),
                ('status', models.BooleanField(default=True)),
                ('source', models.PositiveIntegerField(default=3)),
                ('num', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
