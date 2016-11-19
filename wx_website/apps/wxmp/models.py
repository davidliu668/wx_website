# coding=utf-8

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class token(models.Model):
    wxid = models.PositiveIntegerField()
    token = models.CharField(max_length=1024)
    time = models.DateTimeField()


class appinfo(models.Model):
    wxid = models.PositiveIntegerField()
    appid = models.CharField(max_length=128)
    secret = models.CharField(max_length=128)
