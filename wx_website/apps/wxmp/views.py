# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.conf import settings
import xml.etree.ElementTree as ET
import hashlib
import logging


# Create your views here.
logger = logging.getLogger(__name__)
token = 'zykfxzs'


def wx_msg_dispatch(request):
    '''
    post：处理微信平台推送过来的消息
    get：处理微信平台的鉴权请求
    '''
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')

    if signature is None or timestamp is None or nonce is None:
        logger.warning('timestamp, signature, nonce is None')
        return HttpResponseBadRequest()

    if not wx_auth(timestamp, signature, nonce):
        logger.warning('wx_auth fail')
        return HttpResponseBadRequest()

    if request.method == 'POST':
        return handle_wx_msg(request)
    elif request.method == 'GET':
        return handle_wx_reg(request)
    else:
        logger.warning('get unknown http request')
        return HttpResponse("unkown http request.")


def handle_wx_msg(request):
    openid = request.GET.get('openid')
    msgbody = request.body
    root = ET.fromstring(msgbody)
    line = '\nopenid:{}\n'.format(openid)
    for ch in root:
        line += '{}:{}<{}>\n'.format(ch.tag, ch.text.encode('utf8'), str(type(ch.text)))
    logger.debug(line)
    return HttpResponse('')


def handle_wx_reg(request):
    '''
    微信认证服务器的接口
    '''
    echostr = request.GET.get('echostr')
    if echostr is None:
        logger.warning('echostr is None')
        return HttpResponseBadRequest()

    logger.info('handle_wx_reg succ.')
    return HttpResponse(echostr)


def wx_auth(timestamp, signature, nonce):
    str_list = [token, timestamp, nonce]
    str_list.sort()
    list_str = ''.join(str_list)
    exp_sig = hashlib.sha1(list_str).hexdigest()

    if exp_sig == signature:
        return True
    else:
        return False


def wx_debug(request):
    logger.debug('### in wx_debug view ###')
    rst = 'ok {}, {}'.format(str(type(settings.G_WX_ID)), settings.G_WX_ID)
    wxid = settings.G_WX_ID
    logstr = "wxid type:{}".format(type(wxid))
    logger.debug(logstr)

    try:
        pass
    except Exception, e:
        rst = 'exception:', str(e)
    return HttpResponse(rst)
