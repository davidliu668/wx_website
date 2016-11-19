# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='appinfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wxid', models.PositiveIntegerField()),
                ('appid', models.CharField(max_length=128)),
                ('secret', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wxid', models.PositiveIntegerField()),
                ('token', models.CharField(max_length=1024)),
                ('time', models.DateTimeField()),
            ],
        ),
    ]
