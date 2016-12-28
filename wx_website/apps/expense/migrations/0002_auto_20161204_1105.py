# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('openid', models.CharField(default=b'nullid', max_length=128, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='expense_list',
            name='fileid',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='expense_list',
            name='is_expense',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='expense_list',
            name='openid',
            field=models.CharField(default=b'nullid', max_length=128),
        ),
    ]
