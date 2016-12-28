# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0002_auto_20161204_1105'),
    ]

    operations = [
        migrations.CreateModel(
            name='exp_pic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cos_uri', models.CharField(max_length=128)),
                ('access_url', models.CharField(max_length=128)),
                ('md5', models.CharField(max_length=32)),
            ],
        ),
    ]
