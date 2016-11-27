# coding=utf-8

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class token(models.Model):
    wxid = models.PositiveIntegerField()
    token = models.CharField(max_length=1024)
    time = models.DateTimeField()

    @classmethod
    def get_token_by_wxid(cls, wxid):
        last_token = token.objects.filter(wxid=wxid)[0]
        return last_token.token


class appinfo(models.Model):
    wxid = models.PositiveIntegerField()
    appid = models.CharField(max_length=128)
    secret = models.CharField(max_length=128)

    @classmethod
    def get_appinfo_by_wxid(cls, wxid):
        app = appinfo.objects.filter(wxid=wxid)[0]
        appid = app.appid
        secret = app.secret
        return (appid, secret)
