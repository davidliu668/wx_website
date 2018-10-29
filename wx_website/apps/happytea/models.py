# coding=utf-8
from django.db import models


# 每笔下午费用
class TeaCharge(models.Model):
    team_id = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField()
    charge_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=256, default='')
    money = models.FloatField()
    add_type = models.PositiveIntegerField(default=1)
    expense = models.BooleanField(default=False)
    fileid = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u'id:{}, team_id:{}, user_id:{}, time:{}, money:{}, remark:{}'.format(
            self.id, self.team_id, self.user_id, self.charge_time, self.money, self.remark)

    class Meta:
        db_table = 'happytea_teacharge_list'


class User(models.Model):
    rtx = models.CharField(max_length=32)
    openid = models.CharField(max_length=128)
    team_id = models.PositiveIntegerField()
    status = models.PositiveIntegerField()
    is_admin = models.BooleanField(default=False)

    def __unicode__(self):
        return u'id:{}, rtx:{}, team_id:{}, openid:{}'.format(
            self.id, self.rtx, self.team_id, self.openid)

    @classmethod
    def get_user_by_openid(cls, openid):
        ret = User.objects.filter(openid=openid)
        if len(ret) == 0:
            return None
        else:
            return ret[0]

    @classmethod
    def get_user_by_id(cls, id):
        ret = User.objects.filter(pk=id)
        if len(ret) == 0:
            return None
        else:
            return ret[0]


class Team(models.Model):
    name = models.CharField(max_length=32)

    @classmethod
    def get_name_by_id(cls, team_id):
        return Team.objects.filter(pk=team_id)[0].name
