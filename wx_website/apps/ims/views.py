# coding=utf-8
import logging
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.http import HttpResponse
from .models import *


# Create your views here.
logger = logging.getLogger(__name__)


def is_login_ims(request):
    if 'login_ims' in request.session:
        return True
    else:
        return False


def check_login(func):
    """
    检查是否登录
    """
    def wrapper(request, *args, **kwargs):
        if is_login_ims(request):
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/ims/ims_login/login/')
    return wrapper


def do_login(request):
    if 'name' not in request.POST or 'passwd' not in request.POST:
        return HttpResponseRedirect('/ims/ims_login/fail/')
    ip = request.META['HTTP_X_FORWARDED_FOR'] \
        if 'HTTP_X_FORWARDED_FOR' in request.META else request.META['REMOTE_ADDR']
    name = request.POST['name'].encode('utf8', 'ignore')
    passwd = request.POST['passwd'].encode('utf8', 'ignore')

    qs = MUser.objects.filter(name=name, passwd=passwd)
    if qs.count() == 0:
        return HttpResponseRedirect('/ims/ims_login/fail/')
    else:
        request.session['login_ims'] = 'succ'
        request.session['user'] = name
        request.session.set_expiry(30 * 60)
        logger.info('{}[{}] login succ'.format(name, ip))
        return HttpResponseRedirect('/ims/ims_list/')


def ajax_get_list(request):
    logger.debug('enter ajax_get_list')

    qs = MInfo.objects.all()

    ims_list = []
    for minfo in qs:
        minfo_data = {}
        minfo_data['id'] = minfo.id
        minfo_data['val1'] = minfo.f01.encode('utf8', 'ignore')
        minfo_data['val2'] = minfo.f04.encode('utf8', 'ignore')
        minfo_data['val3'] = minfo.f02.encode('utf8', 'ignore')
        minfo_data['val4'] = minfo.f03.encode('utf8', 'ignore')
        minfo_data['val5'] = minfo.f07.encode('utf8', 'ignore')
        minfo_data['all'] = ''

        ims_list.append(minfo_data)

    tbl_data = dict()
    tbl_data['data'] = ims_list

    return JsonResponse(tbl_data, safe=False)


@check_login
def view_log(request):
    user = request.session['user'].encode('utf8', 'ignore')
    if user != 'zhuofu':
        return HttpResponseRedirect('/ims/ims_list/')

    logs_str = ''

    with open('/data/website/logs/ims.log', 'r') as fp:
        lines = fp.readlines()
        lines.reverse()
        for line in lines:
            line = line.replace('apps.ims.views: ', '')
            line = line.replace('(20) ', '')
            logs_str += line + '<br>'

    return HttpResponse(logs_str)


@check_login
def ims_list(request):
    logger.debug('enter ims_list')
    user = request.session['user'].encode('utf8', 'ignore')
    browse_ip = request.META['HTTP_X_FORWARDED_FOR'] \
        if 'HTTP_X_FORWARDED_FOR' in request.META else request.META['REMOTE_ADDR']

    context = {}
    # 左导航的选中项-li_project
    context['active_li_id'] = 'li_list'
    # 上导航的路径
    context['bread_nav_list'] = [
        {'url': '#', 'tag': 'IMS系统'}, {'url': '#', 'tag': '发动机配置表'}]

    logger.info('{}[{}] view ims_list'.format(user, browse_ip))

    return render(request, 'ims/ims_list.html', context)


@check_login
def ims_detail(request, m_id):
    logger.debug('enter ims_detail')
    user = request.session['user'].encode('utf8', 'ignore')
    m_id = int(m_id)
    browse_ip = request.META['HTTP_X_FORWARDED_FOR'] \
        if 'HTTP_X_FORWARDED_FOR' in request.META else request.META['REMOTE_ADDR']

    context = {}
    # 左导航的选中项-li_project
    context['active_li_id'] = 'li_list'
    # 上导航的路径
    context['bread_nav_list'] = [{'url': '#', 'tag': 'IMS系统'},
                                 {'url': '/ims/ims_list/', 'tag': '发动机配置表'},
                                 {'url': '#', 'tag': '配置详情'}]

    logger.info('{}[{}] view ims_detail'.format(user, browse_ip))

    qs_col = MColName.objects.all()
    col_dict = {}
    for mColName in qs_col:
        col_dict[mColName.col_index] = mColName.col_name.encode(
            'utf8', 'ignore')

    minfo = MInfo.objects.get(pk=m_id)

    item_list = []
    index = 1
    for col_index in sorted(col_dict.keys()):
        # col_list.append(col_dict[col_index])
        fname = 'f{:0>2}'.format(index)
        val = getattr(minfo, fname).encode('utf8', 'ignore')
        # val_list.append(val)
        item_list.append((col_dict[col_index], val))
        index += 1

    context['item_list'] = item_list

    return render(request, 'ims/ims_detail.html', context)


def ims_login(request, flag):
    logger.debug('enter ims_login')
    flag = str(flag)
    browse_ip = request.META['HTTP_X_FORWARDED_FOR'] \
        if 'HTTP_X_FORWARDED_FOR' in request.META else request.META['REMOTE_ADDR']

    context = {}
    # 左导航的选中项-li_project
    context['active_li_id'] = 'li_list'
    # 上导航的路径
    context['bread_nav_list'] = [
        {'url': '#', 'tag': 'IMS系统'}, {'url': '#', 'tag': '登录'}]

    is_fail = 0 if flag != 'fail' else 1
    context['is_fail'] = is_fail

    logger.debug('{}[{}] view ims_login[{}]'.format('...', browse_ip, flag))

    return render(request, 'ims/ims_login.html', context)
