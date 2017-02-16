# coding=utf-8

from __future__ import unicode_literals

import logging
import json
import os
from django.conf import settings
from wxmp_client import WxmpClient
from models import token


logger = logging.getLogger(__name__)


class WxmpOp:
    '''
    提供微信公众号接口操作
    '''

    # 微信公众号id
    wxid = settings.G_WX_ID
    msg_folder = 'wxmp_msg'

    def __init__(self):
        self.wc = WxmpClient()
        self.msg_folder = os.path.dirname(__file__) + os.sep + 'wxmp_msg'

    def load_msg(self, msgname):
        filepath = self.msg_folder + os.sep + msgname + '.msg'
        msg = None
        fp = None

        try:
            fp = file(filepath)
            msg = fp.read()
            msg = msg.decode('utf-8', 'ignore')
        except Exception as e:
            logger.error(
                'load msg exception, msg: {}, errinfo:{}'.format(msgname, str(e)))
            logger.exception(e)
        finally:
            if fp is not None:
                fp.close()

        return msg

    def create_menu(self):
        msg = self.load_msg('create_menu')
        if msg is None:
            logger.error('create_menu fail(load msg)')
            return False

        last_token = token.get_token_by_wxid(self.wxid).token
        query_url = '/cgi-bin/menu/create?access_token={}'.format(last_token)

        (ret, rsp, rspmsg) = self.wc.request(url=query_url, body=msg)

        if ret != 0:
            logger.error('create_menu fail(wxmp request)')
            return False

        if 'errcode' in rsp and rsp['errcode'] == 0:
            logger.info('create menu succ')
            return True
        else:
            logger.error(
                'create_menu fail(rsp check), rspmsg:{}'.format(rspmsg))
            return False
