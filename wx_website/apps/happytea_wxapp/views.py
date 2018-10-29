# coding=utf-8
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from .models import AppUser
from ..happytea.models import TeaCharge, User
import logging
import string
import datetime
import random
import requests

logger = logging.getLogger(__name__)

# 绑定码在memcached的过期时间（单位：秒）
memcached_timeout = 180

appid = 'wxeefa7e90ad6d43e6'
appsecret = 'a213884ef0388ba9c3a167290efccdfa'


def index(request):
    return HttpResponse('开发中...')


def la(request):
    logger.info('recv http msg: \n{}'.format(fmt_request(request)))
    return HttpResponse('la 开发中...')


def add_one_teacharge(request):
    openid = request.GET.get('openid').encode('utf8', 'ignore')
    appUser = AppUser.objects.get(pk=openid)
    user = User.objects.get(pk=appUser.user_id)

    ret_json = {}
    # 检查用户的状态，如果未审核，则不能提交
    if user.status == 0:
        ret_json['retcode'] = 1
        logger.info('{} status is 0, reject add teacharge'.format(user.rtx))
    # 审核通过，不经过缓存，直接提交
    else:
        time = request.GET.get('time')
        money = float(request.GET.get('money'))
        remark = request.GET.get('remark')

        charge_time = datetime.datetime.strptime(time, '%Y-%m-%d')

        teaCharge = TeaCharge(team_id=user.team_id, user_id=user.id,
                              charge_time=charge_time, remark=remark,
                              money=money, add_type=2)
        teaCharge.save()

        logger.warn(u'{}({}) add expense to db, TeaCharge:{}'.format(
            appUser.nickname, user.rtx, teaCharge))
        ret_json['retcode'] = 0

    return JsonResponse(ret_json, safe=False)


def get_teachage_info(request):
    openid = request.GET.get('openid').encode('utf8', 'ignore')
    appUser = AppUser.objects.get(pk=openid)

    last_time = '无'
    last_money = 0
    total_unexp_money = 0
    qs = TeaCharge.objects.filter(
        user_id=appUser.user_id).order_by('-create_time')
    if qs.exists():
        last = qs[0]
        last_money = last.money
        last_time = last.charge_time.strftime('%m月%d日')
        for teacharge in qs:
            if not teacharge.expense:
                total_unexp_money += teacharge.money

    ret_json = {}
    ret_json['last_time'] = last_time
    ret_json['last_money'] = last_money
    ret_json['total_unexp_money'] = total_unexp_money
    ret_json['retcode'] = 0

    logger.info('{} get_teachage_info succ'.format(
        appUser.nickname.encode('utf8', 'ignore')))

    return JsonResponse(ret_json, safe=False)


def get_openid(request):
    code = request.GET.get('code').encode('utf8', 'ignore')

    url = 'https://api.weixin.qq.com/sns/jscode2session' \
        + '?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(
            appid, appsecret, code)

    rsp = requests.get(url)
    rsp = rsp.json()
    open_id = rsp['openid'].encode('utf8', 'ignore')
    # session_key = rsp['session_key']

    ret = {}
    ret['ret'] = 0
    ret['open_id'] = open_id
    logger.info('get_openid succ: ' + open_id)

    return JsonResponse(ret, safe=False)


def get_activeinfo(request):
    openid = request.GET.get('openid').encode('utf8', 'ignore')
    nickname = request.GET.get('nickname').encode('utf8', 'ignore')

    # 先检查用户是否已经激活，如果已经激活，直接返回 active_status = 0
    qs = AppUser.objects.filter(pk=openid)
    if qs.exists():
        return JsonResponse({'active_status': 0}, safe=False)

    # 获取激活码
    activeinfo = cache.get('wxapp_active_openid_' + openid)

    # 如果为None，说明已经过期，或者还未分配
    if activeinfo is None:
        # 分配一个新的激活码
        code = gen_activecode()

        if code is None:
            return JsonResponse({'activecode': '获取失败', 'activetime': '-:-:-'}, safe=False)

        # 保存 openid: codeinfo
        expire_time = datetime.datetime.now() + datetime.timedelta(seconds=memcached_timeout)
        expire_time = expire_time.strftime('%H:%M:%S')
        activeinfo = {'activecode': code, 'activetime': expire_time}
        cache.set('wxapp_active_openid_' + openid,
                  activeinfo, memcached_timeout)

        # 保存 code：openid，nickname
        bindinfo = {'openid': openid, 'nickname': nickname}
        cache.set('wxapp_actvie_code_' + code, bindinfo, memcached_timeout)
        if nickname != 'oltest':
            logger.info('gen activeinfo succ: {}, {}'.format(
                activeinfo['activecode'], activeinfo['activetime']))
    else:
        if nickname != 'oltest':
            logger.info('get activeinfo succ: {}, {}'.format(
                activeinfo['activecode'], activeinfo['activetime']))

    return JsonResponse(activeinfo, safe=False)


def gen_activecode():
    # 从cache中拉取正在使用的code列表，没有则初始化
    exist_code_list = cache.get('wxapp_exist_code_list')
    if exist_code_list is None:
        exist_code_list = []

    # 分配四位随机数字，确保没有在正在使用的列表中
    code = ''.join([random.choice(string.digits) for i in range(4)])
    index = 0
    while code in exist_code_list and index < 1000:
        code = ''.join([random.choice(string.digits) for i in range(4)])
        index += 1

    # 如果index超过1000，说明出问题了
    if index >= 1000:
        logger.error('gen activecode fail, try over 1000 times')
        return None

    # 将新分配的code保存到正在使用列表中
    exist_code_list.append(code)
    cache.set('wxapp_exist_code_list', exist_code_list, memcached_timeout)
    return code


def fmt_request(request):
    fmt_str = ''
    method = request.method
    url = request.get_full_path()
    scheme = request.META['SERVER_PROTOCOL']
    fmt_str += '{} {} {}\n\n'.format(method, url, scheme)

    for key in request.META:
        if not key[0].isupper():
            continue
        fmt_str += '{}: {}\n'.format(key, request.META[key])

    fmt_str += '\n'

    fmt_str += '{}\n'.format(request.body)

    return fmt_str
