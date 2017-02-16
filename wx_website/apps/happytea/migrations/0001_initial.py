# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TeaCharge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('team_id', models.PositiveIntegerField()),
                ('user_id', models.PositiveIntegerField()),
                ('charge_time', models.DateTimeField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('remark', models.CharField(default=b'', max_length=256)),
                ('money', models.FloatField()),
                ('expense', models.BooleanField(default=False)),
                ('fileid', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'happytea_teacharge_list',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rtx', models.CharField(max_length=32)),
                ('openid', models.CharField(max_length=128)),
                ('team_id', models.PositiveIntegerField()),
                ('status', models.PositiveIntegerField()),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
    ]
