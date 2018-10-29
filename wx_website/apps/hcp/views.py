# coding=utf-8
import logging
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from .models import *
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


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
            return HttpResponseRedirect('/hcp/ims_login/login/')
    return wrapper


def do_login(request):
    if 'user' not in request.POST or 'wx_name' not in request.POST:
        return HttpResponseRedirect('/hcp/ims_login/fail/')
    # ip = request.META['HTTP_X_FORWARDED_FOR'] \
    # if 'HTTP_X_FORWARDED_FOR' in request.META else
    # request.META['REMOTE_ADDR']
    user = request.POST['user'].encode('utf8', 'ignore')
    wx_name = request.POST['wx_name'].encode('utf8', 'ignore')

    qs = User.objects.filter(name=user)
    if qs.count() == 0:
        userObj = User(name=user, wx_name=wx_name)
        userObj.save()
        logger.debug('reg new user: {}, wx_name: {}'.format(user, wx_name))
        return HttpResponseRedirect('/hcp/ims_list/{}/'.format(userObj.id))
    else:
        userObj = qs[0]
        request.session['login_ims'] = 'succ'
        request.session['name'] = user
        request.session['wx_name'] = wx_name
        request.session.set_expiry(15 * 60)
        logger.debug('{}[{}] login succ'.format(user, wx_name))
        return HttpResponseRedirect('/hcp/ims_list/{}/'.format(userObj.id))


@check_login
def ims_logout(request):
    if 'login_ims' in request.session:
        del request.session['login_ims']
    if 'name' in request.session:
        del request.session['name']
    if 'wx_name' in request.session:
        del request.session['wx_name']

    return HttpResponseRedirect('/hcp/ims_login/login/')


def ajax_get_list(request, name):
    logger.debug('enter ajax_get_hcp_list')

    name = name.encode('utf8', 'ignore')
    qs = Order.objects.filter(user=name)

    ims_list = []
    for order in qs:
        minfo_data = {}
        minfo_data['id'] = order.id
        minfo_data['from'] = order.from_station.encode('utf8', 'ignore')
        minfo_data['to'] = order.to_station.encode('utf8', 'ignore')
        minfo_data['time'] = order.time.strftime('%m-%d')
        minfo_data['name'] = order.name.encode('utf8', 'ignore')
        minfo_data['sfz_id'] = order.sfz_id.encode('utf8', 'ignore')
        minfo_data['is_student'] = order.is_student
        minfo_data['remark'] = order.remark.encode('utf8', 'ignore')
        minfo_data['remark2'] = order.remark2.encode('utf8', 'ignore')

        ims_list.append(minfo_data)

    tbl_data = dict()
    tbl_data['data'] = ims_list

    return JsonResponse(tbl_data, safe=False)


@check_login
def ims_about(request):
    name = request.session['name'].encode('utf8', 'ignore')
    context = {}
    # 左导航的选中项-li_project
    context['active_li_id'] = 'li_list'
    # 上导航的路径
    uid = User.objects.get(name=name).id
    context['bread_nav_list'] = [{'url': '/hcp/ims_list/{}/'.format(uid), 'tag': '订单信息'},
                                 {'url': '#', 'tag': '联系方式'}]
    return render(request, 'hcp/ims_about.html', context)


@check_login
def ims_rpt(request, user_id):
    logger.debug('enter ims_list')
    name = request.session['name'].encode('utf8', 'ignore')

    context = {}
    # 左导航的选中项-li_project
    context['active_li_id'] = 'li_list'
    # 上导航的路径
    uid = User.objects.get(name=name).id
    wx_name = User.objects.get(name=name).wx_name.encode('utf8', 'ignore')
    context['bread_nav_list'] = [{'url': '/hcp/ims_list/{}/'.format(uid), 'tag': '订单信息'},
                                 {'url': '#', 'tag': '订单确认'}]

    qs = Order.objects.filter(user=name)

    rpt_txt = ''
    rpt_txt += '联系电话: {}\n\n'.format(name)

    if qs.count() == 0:
        rpt_txt += '请先添加订单，谢谢！'
    else:
        idx = 1
        for order in qs:
            rpt_txt += '订单-{}\n'.format(idx)
            idx += 1

            rpt_txt += "出行人: {}\n".format(order.name.encode('utf8', 'ignore'))
            rpt_txt += "身份证: {}\n".format(
                order.sfz_id.encode('utf8', 'ignore'))
            rpt_txt += "出行时间: {}\n".format(order.time.strftime('%Y-%m-%d'))
            rpt_txt += "出发地: {}\n".format(
                order.from_station.encode('utf8', 'ignore'))
            rpt_txt += "目的地: {}\n".format(
                order.to_station.encode('utf8', 'ignore'))
            rpt_txt += "备注: {}\n".format(order.remark.encode('utf8', 'ignore'))
            rpt_txt += "\n"

        sender = settings.EMAIL_HOST_USER
        sendto = ["hejunyi-1@163.com", "liuzhuofu1984@163.com"]
        title = '[订单信息汇总]手机: {}, wx: {}, 订单数: {}'.format(
            name, wx_name, qs.count())
        email = EmailMultiAlternatives(title, rpt_txt, sender, sendto)
        email.attach_alternative(rpt_txt, 'text/plain')

        qs_rpt = Rpt.objects.filter(name=name)
        if qs_rpt.count() == 1:
            rpt = qs_rpt[0]
            if rpt.rpt_txt.encode('utf8', 'ignore') != rpt_txt:
                rpt.rpt_txt = rpt_txt
                rpt.save()
                email.send()
        else:
            rpt = Rpt(name=name, rpt_txt=rpt_txt)
            rpt.save()
            email.send()

    context['rpt_txt'] = rpt_txt

    return render(request, 'hcp/ims_rpt.html', context)


@check_login
def ims_list(request, user_id):
    logger.debug('enter ims_list')
    user_id = int(user_id)
    name = request.session['name'].encode('utf8', 'ignore')
    # browse_ip = request.META['HTTP_X_FORWARDED_FOR'] \
    # if 'HTTP_X_FORWARDED_FOR' in request.META else
    # request.META['REMOTE_ADDR']

    context = {}
    # 左导航的选中项-li_project
    context['active_li_id'] = 'li_list'
    # 上导航的路径
    context['bread_nav_list'] = [
        {'url': '#', 'tag': '订单信息'}]

    if user_id != 0:
        userObj = User.objects.get(pk=user_id)
        if name != userObj.name:
            return HttpResponseRedirect('/hcp/ims_login/fail/')
    else:
        userObj = User.objects.get(name=name)
        user_id = userObj.id

    wx_name = userObj.wx_name.encode('utf8', 'ignore')
    context['name'] = name
    context['name_display'] = name if wx_name == "" else wx_name
    context['id'] = user_id

    qs = Order.objects.filter(user=name)
    context['num'] = qs.count()

    logger.debug('{}[{}] view ims_list'.format(name, wx_name))

    return render(request, 'hcp/ims_list.html', context)


@check_login
def ims_detail(request, o_id):
    logger.debug('enter ims_detail')
    name = request.session['name'].encode('utf8', 'ignore')
    uid = User.objects.get(name=name).id
    o_id = int(o_id)

    context = {}
    # 左导航的选中项-li_project
    context['active_li_id'] = 'li_list'
    # 上导航的路径
    context['bread_nav_list'] = [{'url': '/hcp/ims_list/{}/'.format(uid), 'tag': '订单信息'},
                                 {'url': '#', 'tag': '详情'}]

    logger.debug('{} view ims_detail'.format(name))

    context['id'] = o_id
    if o_id == 0:
        qs = Order.objects.filter(user=name).order_by('-create_time')
        if qs.count() > 0:
            order = qs[0]
            context['time'] = order.time.strftime('%Y-%m-%d')
            context['from'] = order.from_station.encode('utf8', 'ignore')
            context['to'] = order.to_station.encode('utf8', 'ignore')
        return render(request, 'hcp/ims_detail.html', context)
    else:
        order = Order.objects.get(pk=o_id)
        context['name'] = order.name.encode('utf8', 'ignore')
        context['sfz_id'] = order.sfz_id.encode('utf8', 'ignore')
        context['time'] = order.time.strftime('%Y-%m-%d')
        context['from'] = order.from_station.encode('utf8', 'ignore')
        context['to'] = order.to_station.encode('utf8', 'ignore')
        context['remark'] = order.remark.encode('utf8', 'ignore')

    return render(request, 'hcp/ims_detail.html', context)


@check_login
def ims_new(request):
    logger.debug('enter ims_new')
    user = request.session['name'].encode('utf8', 'ignore')
    uid = User.objects.get(name=user).id

    oid = int(request.POST['id'])
    name = request.POST['name'].encode('utf8', 'ignore')
    sfz_id = request.POST['sfz_id'].encode('utf8', 'ignore')
    time = request.POST['time'].encode('utf8', 'ignore')
    if time.find('-') != -1:
        time = datetime.datetime.strptime(time, '%Y-%m-%d')
    else:
        time = datetime.datetime.strptime(time, '%Y年%m月%d日')
    from_station = request.POST['from'].encode('utf8', 'ignore')
    to_station = request.POST['to'].encode('utf8', 'ignore')
    remark = request.POST['remark'].encode('utf8', 'ignore')

    if oid == 0:
        order = Order(user=user, from_station=from_station, to_station=to_station,
                      time=time, name=name, sfz_id=sfz_id, remark=remark)
        order.save()
        logger.info('{} add, name: {}, sfz_id: {}, time: {},\
            from: {}, to: {}, remark: {}'.format(user, name, sfz_id, time,
                                                 from_station, to_station, remark))
    else:
        order = Order.objects.get(id=oid)
        order.name = name
        order.sfz_id = sfz_id
        order.time = time
        order.from_station = from_station
        order.to_station = to_station
        order.remark = remark
        order.save()
        logger.info('{} edit, name: {}, sfz_id: {}, time: {},\
            from: {}, to: {}, remark: {}'.format(user, name, sfz_id, time,
                                                 from_station, to_station, remark))

    return HttpResponseRedirect('/hcp/ims_list/{}/'.format(uid))


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
        {'url': '#', 'tag': '登录'}]

    if 'name' in request.session:
        context['name'] = request.session['name'].encode('utf8', 'ignore')
    if 'wx_name' in request.session:
        context['wx_name'] = request.session[
            'wx_name'].encode('utf8', 'ignore')

    is_fail = 0 if flag != 'fail' else 1
    context['is_fail'] = is_fail

    logger.debug('{}[{}] view ims_login[{}]'.format('...', browse_ip, flag))

    return render(request, 'hcp/ims_login.html', context)
