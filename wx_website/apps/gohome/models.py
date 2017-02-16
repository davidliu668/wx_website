# coding=utf-8
from django.db import models

# Create your models here.


# 12306账号
class Account(models.Model):
    name = models.CharField(max_length=32)
    passwd = models.CharField(max_length=32)
    remark = models.CharField(max_length=256)
    status = models.BooleanField(default=True)
    source = models.PositiveIntegerField(default=3)
    num = models.PositiveIntegerField(default=0)
    from_station = models.CharField(default='', max_length=256)
    end_station = models.CharField(default='', max_length=256)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    @classmethod
    def add(cls, name, passwd, remark='', status=True, source=3, num=0,
            from_station='', end_station='', start_date='', end_date=''):
        account = Account(name=name, passwd=passwd, remark=remark,
                          status=status, source=source, num=num,
                          from_station=from_station, end_station=end_station,
                          start_date=start_date, end_date=end_date)
        account.save()

    @classmethod
    def update_by_name(cls, name, passwd, status=True,
                       from_station='', end_station='', start_date='', end_date=''):
        account = Account.objects.get(name=name)
        account.passwd = passwd
        account.status = status
        account.from_station = from_station
        account.end_station = end_station
        account.start_date = start_date
        account.end_date = end_date
        account.save()
