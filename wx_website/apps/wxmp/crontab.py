# coding=utf-8

import datetime
import json
from lib.httpclient import HttpClient
from models import appinfo
from models import token


# 微信公众号id
wxid = 1
wx_host = 'api.weixin.qq.com'


def get_app_token():
    app = appinfo.objects.filter(wxid=wxid)[0]
    appid = app.appid
    secret = app.secret

    query_url = "/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(appid, secret)

    hc = HttpClient(wx_host, url=query_url, https=True)
    (ret, retinfo) = hc.send_and_recv()

    if ret != 0:
        print 'get app token fail, info:' + retinfo
        return

    json_obj = json.loads(retinfo)
    if 'access_token' not in json_obj:
        print 'get app token fail, wx rsp:' + retinfo
        return

    new_token = json_obj['access_token']
    cur_time = datetime.datetime.now()

    last_token = token.objects.filter(wxid=wxid)[0]
    last_token.token = new_token
    last_token.time = cur_time
    last_token.save()

    print 'update app token succ, wxid: {}, time: {}'.format(wxid, str(cur_time)[0:-7])


if __name__ == "__main__":
    pass
