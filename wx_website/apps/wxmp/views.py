from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.mail import mail_admins
from django.core.mail import get_connection
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

    str_list = [token, timestamp, nonce]
    str_list.sort()
    list_str = ''.join(str_list)
    exp_sig = hashlib.sha1(list_str).hexdigest()

    if exp_sig == signature:
        return HttpResponse(echostr)
    else:
        return HttpResponse("check wx_reg fail.")


def wx_debug(request):
    from django.conf import settings
    rst = 'ok' + str(type(settings))

    try:
        cc = get_connection(fail_silently=False, username='wx_website@163.com', password='wx123456')
        mail_admins('ss', 'cc', connection=cc)
        #send_mail('title33', 'text333', 'wx_website@163.com',
        #          ['liuzhuofu1984@163.com'])
    except Exception, e:
        rst = 'exception:', str(e)
    return HttpResponse(rst)
