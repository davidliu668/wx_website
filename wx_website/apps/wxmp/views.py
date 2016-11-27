from django.shortcuts import render
from django.http import HttpResponse
import hashlib
import logging


# Create your views here.
logger = logging.getLogger(__name__)


def wx_reg(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    echostr = request.GET.get('echostr')
    token = 'zykfxzs'

    if signature is None or timestamp is None or nonce is None or echostr is None:
        logger.warning('wx_reg url format error.')
        return HttpResponse("url format error")

    str_list = [token, timestamp, nonce]
    str_list.sort()
    list_str = ''.join(str_list)
    exp_sig = hashlib.sha1(list_str).hexdigest()

    if exp_sig == signature:
        return HttpResponse(echostr)
    else:
        logger.error('check wx_reg signature fail.')
        return HttpResponse("check wx_reg fail.")


def wx_debug(request):
    logger.debug('### in wx_debug view ###')
    rst = 'ok'

    try:
        pass
    except Exception, e:
        rst = 'exception:', str(e)
    return HttpResponse(rst)
