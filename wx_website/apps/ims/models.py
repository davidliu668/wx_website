# coding=utf-8

from django.db import models

# Create your models here.

class MColName(models.Model):
    col_index = models.PositiveIntegerField()
    col_name = models.CharField(max_length=256)

class MInfo(models.Model):
    f01 = models.CharField(max_length=256, default='')
    f02 = models.CharField(max_length=256, default='')
    f03 = models.CharField(max_length=256, default='')
    f04 = models.CharField(max_length=256, default='')
    f05 = models.CharField(max_length=256, default='')
    f06 = models.CharField(max_length=256, default='')
    f07 = models.CharField(max_length=256, default='')
    f08 = models.CharField(max_length=256, default='')
    f09 = models.CharField(max_length=256, default='')
    f10 = models.CharField(max_length=256, default='')

    f11 = models.CharField(max_length=256, default='')
    f12 = models.CharField(max_length=256, default='')
    f13 = models.CharField(max_length=256, default='')
    f14 = models.CharField(max_length=256, default='')
    f15 = models.CharField(max_length=256, default='')
    f16 = models.CharField(max_length=256, default='')
    f17 = models.CharField(max_length=256, default='')
    f18 = models.CharField(max_length=256, default='')
    f19 = models.CharField(max_length=256, default='')
    f20 = models.CharField(max_length=256, default='')

    f21 = models.CharField(max_length=256, default='')
    f22 = models.CharField(max_length=256, default='')
    f23 = models.CharField(max_length=256, default='')
    f24 = models.CharField(max_length=256, default='')
    f25 = models.CharField(max_length=256, default='')
    f26 = models.CharField(max_length=256, default='')
    f27 = models.CharField(max_length=256, default='')
    f28 = models.CharField(max_length=256, default='')
    f29 = models.CharField(max_length=256, default='')
    f30 = models.CharField(max_length=256, default='')

    f31 = models.CharField(max_length=256, default='')
    f32 = models.CharField(max_length=256, default='')
    f33 = models.CharField(max_length=256, default='')
    f34 = models.CharField(max_length=256, default='')
    f35 = models.CharField(max_length=256, default='')
    f36 = models.CharField(max_length=256, default='')
    f37 = models.CharField(max_length=256, default='')
    f38 = models.CharField(max_length=256, default='')
    f39 = models.CharField(max_length=256, default='')
    f40 = models.CharField(max_length=256, default='')

    f41 = models.CharField(max_length=256, default='')
    f42 = models.CharField(max_length=256, default='')
    f43 = models.CharField(max_length=256, default='')
    f44 = models.CharField(max_length=256, default='')
    f45 = models.CharField(max_length=256, default='')
    f46 = models.CharField(max_length=256, default='')
    f47 = models.CharField(max_length=256, default='')
    f48 = models.CharField(max_length=256, default='')
    f49 = models.CharField(max_length=256, default='')
    f50 = models.CharField(max_length=256, default='')

    f51 = models.CharField(max_length=256, default='')
    f52 = models.CharField(max_length=256, default='')
    f53 = models.CharField(max_length=256, default='')
    f54 = models.CharField(max_length=256, default='')
    f55 = models.CharField(max_length=256, default='')
    f56 = models.CharField(max_length=256, default='')
    f57 = models.CharField(max_length=256, default='')
    f58 = models.CharField(max_length=256, default='')
    f59 = models.CharField(max_length=256, default='')
    f60 = models.CharField(max_length=256, default='')

    f61 = models.CharField(max_length=256, default='')
    f62 = models.CharField(max_length=256, default='')
    f63 = models.CharField(max_length=256, default='')
    f64 = models.CharField(max_length=256, default='')
    f65 = models.CharField(max_length=256, default='')
    f66 = models.CharField(max_length=256, default='')
    f67 = models.CharField(max_length=256, default='')
    f68 = models.CharField(max_length=256, default='')
    f69 = models.CharField(max_length=256, default='')
    f70 = models.CharField(max_length=256, default='')


class MUser(models.Model):
    name = models.CharField(max_length=32)
    passwd = models.CharField(max_length=32)
