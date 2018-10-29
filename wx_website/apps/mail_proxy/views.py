# coding=utf-8
import logging
import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives


# Create your views here.
logger = logging.getLogger(__name__)


def send_mail(request):
    logger.debug('enter send_mail...')
    body = request.body

    ret_json = {'ret_code': 0, 'errinfo': ''}

    try:
        obj = json.loads(body)

        title = obj['title'].encode('utf8', 'ignore')
        content = obj['content'].encode('utf8', 'ignore')
        sendto = obj['sendto'].encode('utf8', 'ignore')

        sendtolist = []
        sendto = sendto.split(',')
        for onesendto in sendto:
            onesendto = onesendto.strip()
            if onesendto != '':
                sendtolist.append(onesendto)

        if 'hejunyi-1@163.com' in sendtolist:
            sendtolist.append('17747406@qq.com')

        sender = settings.EMAIL_HOST_USER
        email = EmailMultiAlternatives(title, content, sender, sendtolist)
        email.attach_alternative(content, 'text/plain')
        email.send()

        logstr = 'send mail, title: {}, sendto: {}, content: {}'.format(
            title, sendto, content)
        logger.debug(logstr)

    except Exception as e:
        # 请求body不是json对象
        ret_json['ret_code'] = 1
        ret_json['errinfo'] = str(e)
        logger.error('send_mail fail, errinfo: {}'.format(str(e)))
    return JsonResponse(ret_json, safe=False)


if __name__ == '__main__':
    body = {'title': '测试qq邮箱规则（请忽略）',
            'content': '测试邮件，请忽略',
            'sendto': 'liuzhuofu1984@163.com,hejunyi-1@163.com'}
    r = requests.post('http://www.gohome123.cn/mail_proxy/send_mail/',
                      data=json.dumps(body, indent=2),
                      timeout=30)
    r.raise_for_status()
    print r.json()
