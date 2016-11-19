from django.shortcuts import render

from django.http import HttpResponse
import hashlib

# Create your views here.

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




