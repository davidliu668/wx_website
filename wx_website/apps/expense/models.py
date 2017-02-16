# coding=utf-8
from django.db import models

# Create your models here.


# 记录每笔报销信息
class expense_list(models.Model):
    money = models.FloatField()
    time = models.DateTimeField()
    remark = models.CharField(max_length=256, default='')
    is_expense = models.BooleanField(default=False)
    openid = models.CharField(max_length=128, default='nullid')
    fileid = models.PositiveIntegerField(default=0)

    @classmethod
    def add_expense(cls, money, time, remark, is_expense, openid, fileid):
        expense = expense_list(money=money, time=time, remark=remark,
                               is_expense=is_expense, openid=openid, fileid=fileid)
        expense.save()

    @classmethod
    def ch_expense(cls, id, is_expense=True):
        expense_list.objects.filter(pk=id).update(is_expense=is_expense)

# 记录报销凭证
class exp_pic(models.Model):
    cos_uri = models.CharField(max_length=128)
    access_url = models.CharField(max_length=128)
    md5 = models.CharField(max_length=32)

    @classmethod
    def add(cls, cos_uri, access_url, md5):
        pic = exp_pic(cos_uri=cos_uri, access_url=access_url, md5=md5)
        pic.save()
        return pic.pk


# 记录用户信息，openid和实际姓名的对应关系
class users(models.Model):
    openid = models.CharField(
        max_length=128, primary_key=True, default='nullid')
    name = models.CharField(max_length=128)

    @classmethod
    def has_user(cls, openid):
        if users.objects.filter(pk=openid):
            return True
        else:
            return False

    @classmethod
    def reg_user(cls, openid, name):
        u = users(openid=openid, name=name)
        u.save()

    @classmethod
    def update_user(cls, openid, name):
        users.objects.filter(pk=openid).update(name=name)
