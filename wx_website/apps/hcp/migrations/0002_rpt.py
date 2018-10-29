# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hcp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rpt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('rpt_txt', models.CharField(default=b'', max_length=2048)),
            ],
        ),
    ]
