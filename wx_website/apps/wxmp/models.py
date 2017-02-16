# coding=utf-8

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class token(models.Model):
    wxid = models.PositiveIntegerField()
    token = models.CharField(max_length=1024)
    time = models.DateTimeField()
    expires_at = models.IntegerField(default=0)

    @classmethod
    def get_token_by_wxid(cls, wxid):
        last_token = token.objects.filter(wxid=wxid)[0]
        return last_token

    @classmethod
    def set_token_by_wxid(cls, wxid, new_token, time, expires_at):
        last_token = token.objects.filter(wxid=wxid)[0]
        last_token.token = new_token
        last_token.time = time
        last_token.expires_at = expires_at
        last_token.save()


class appinfo(models.Model):
    wxid = models.PositiveIntegerField()
    appid = models.CharField(max_length=128)
    secret = models.CharField(max_length=128)
    token = models.CharField(max_length=128, default='')
    aes_key = models.CharField(max_length=128, default='')

    @classmethod
    def get_appinfo_by_wxid(cls, wxid):
        app = appinfo.objects.filter(wxid=wxid)[0]
        return (app.appid, app.secret, app.token, app.aes_key)
