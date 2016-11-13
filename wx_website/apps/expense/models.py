#coding=utf-8

from __future__ import unicode_literals

from django.db import models

# Create your models here.

class expense_list(models.Model):
    money = models.FloatField()
    time = models.DateTimeField()
    remark = models.CharField(max_length=256)

