# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=64)),
                ('from_station', models.CharField(default=b'', max_length=256)),
                ('to_station', models.CharField(default=b'', max_length=256)),
                ('time', models.DateField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=64)),
                ('sfz_id', models.CharField(max_length=64)),
                ('is_student', models.PositiveIntegerField(default=0)),
                ('remark', models.CharField(default=b'', max_length=256)),
                ('remark2', models.CharField(default=b'', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('wx_name', models.CharField(default=b'', max_length=64)),
                ('passwd', models.CharField(default=b'', max_length=32)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
