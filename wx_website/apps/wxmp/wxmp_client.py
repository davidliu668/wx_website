# coding=utf-8
from __future__ import unicode_literals
import logging
import json
from lib.httpclient import HttpClient


logger = logging.getLogger(__name__)


class WxmpClient:
    '''
    do https request with wxmp platform
    '''
    wx_host = 'api.weixin.qq.com'
    timeout = 15

    def __init__(self):
        self.hc = HttpClient(self.wx_host, https=True)

    def request(self, url='', body='', headers={}):
        logger.info('do request, url: {}, body: {}'.format(url, body))

        # 设置url等信息
        self.hc.set_url(url)
        self.hc.set_body(body)
        self.hc.set_headers(headers)

        # 如果body不为空，修改方法为post，并检查body格式
        if body != '':
            self.hc.set_method('POST')

        # 发送请求并接收响应
        (ret, retinfo) = self.hc.send_and_recv(timeout=self.timeout)
        if ret != 0:
            logger.error(
                'do request fail(http send_and_recv), errinfo: {}'.format(retinfo))

            if not (self.hc.get_exception() is None):
                logger.exception(self.hc.get_exception())

            return (1, None)

        # 解析body，判断是否有错误码
        try:
            rsp = json.loads(retinfo)

            # 如果有‘errcode’且不为0，则说明请求失败
            if 'errcode' in rsp and rsp['errcode'] != 0:
                errmsg = ''
                if 'errmsg' in rsp:
                    errmsg = rsp['errmsg']

                logger.error('do request fail(wx rsp fail), errcode: {}, errmsg: {}'.format(
                    rsp['errcode'], errmsg))
                return (3, errmsg)

            # 如果运行到这里，说明请求成功，返回响应的json对象
            logger.info('do request succ')

            rsp_txt = json.dumps(rsp, indent=2)
            logger.debug('wxmp rsp: \n{}'.format(rsp_txt))
            return (0, rsp)

        except Exception as e:
            logger.error('do request fail(parse rsp)')
            logger.exception(e)
            return (2, None)
