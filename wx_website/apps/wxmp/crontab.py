# coding=utf-8

import datetime
import logging
from wxmp_client import WxmpClient
from models import appinfo
from models import token


# 微信公众号id
wxid = 1
logger = logging.getLogger(__name__)


def get_app_token():
    app = appinfo.objects.filter(wxid=wxid)[0]
    appid = app.appid
    secret = app.secret

    query_url = "/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(appid, secret)

    wc = WxmpClient()
    (ret, rsp, rsp_txt) = wc.request(url=query_url)

    if ret != 0:
        logger.error('get wxmp app token fail')
        return

    if 'access_token' not in rsp:
        logger.error('get token from rsp fail, rsp:\n{}'.format(rsp_txt))
        return

    new_token = rsp['access_token']
    cur_time = datetime.datetime.now()

    last_token = token.objects.filter(wxid=wxid)[0]
    last_token.token = new_token
    last_token.time = cur_time
    last_token.save()

    logger.info('update app token succ, wxid: {}, time: {}'.format(wxid, str(cur_time)[0:-7]))


if __name__ == "__main__":
    pass
