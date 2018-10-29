# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_openid', models.CharField(max_length=128)),
                ('user_id', models.PositiveIntegerField()),
                ('nickname', models.CharField(max_length=128)),
                ('bind_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'happytea_wxapp_user_list',
            },
        ),
    ]
