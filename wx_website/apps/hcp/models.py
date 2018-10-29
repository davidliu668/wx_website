# coding=utf-8
from django.db import models

# Create your models here.


# 订单信息
class Order(models.Model):
    # 下订单的用户名(手机号)
    user = models.CharField(max_length=64)

    # 起点站和终点站
    from_station = models.CharField(default='', max_length=256)
    to_station = models.CharField(default='', max_length=256)

    # 订票时间
    time = models.DateField()
    create_time = models.DateTimeField(auto_now_add=True)

    # 身份信息
    name = models.CharField(max_length=64)
    sfz_id = models.CharField(max_length=64)
    is_student = models.PositiveIntegerField(default=0)

    # 备注
    remark = models.CharField(default='', max_length=256)
    remark2 = models.CharField(default='', max_length=256)


class User(models.Model):
    name = models.CharField(max_length=64)
    wx_name = models.CharField(default='', max_length=64)
    passwd = models.CharField(default='', max_length=32)
    create_time = models.DateTimeField(auto_now_add=True)


class Rpt(models.Model):
    # 手机号
    name = models.CharField(max_length=64)
    rpt_txt = models.CharField(default='', max_length=2048)
