# coding=utf-8
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.cache import cache
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import *
from qcloud_cos import CosClient
from qcloud_cos import UploadFileRequest
from ..wxmp.models import token
from ..wxmp.models import appinfo
from ..happytea_wxapp.models import AppUser
from .models import *
import logging
import datetime
import re
import csv
import codecs
import os


logger = logging.getLogger(__name__)

# 请求存放memcache的过期时间（单位：秒）
memcached_timeout = 180

# 反馈邮件接收列表
maillist_fankui = ['zhuofuliu@tencent.com']

# 注册请求接收列表
maillist_user_reg = ['zhuofuliu@tencent.com']

# 微信公众号在db中的id
wx_id = 3
(appid, appsecret, apptoken, appaeskey) = appinfo.get_appinfo_by_wxid(wx_id)


def set_wx_token_func(newtoken, expires_at):
    '''
    定义设置token和expires_at的函数
    '''
    cur_time = datetime.datetime.now()
    token.set_token_by_wxid(wx_id, newtoken, cur_time, expires_at)


def get_wx_token_func():
    '''
    定义获取token和expires_at的函数
    '''
    last_token = token.get_token_by_wxid(wx_id)
    return (str(last_token.token), last_token.expires_at)


conf = WechatConf(token=apptoken, appid=appid, appsecret=appsecret,
                  encrypt_mode='normal', encoding_aes_key=appaeskey,
                  access_token_getfunc=get_wx_token_func,
                  access_token_setfunc=set_wx_token_func,
                  access_token_refreshfunc=None)
wechat = WechatBasic(conf=conf)


def index(request):
    return HttpResponseRedirect('/static/index.html')


def wxmp(request):
    '''
    get：处理微信平台发来的鉴权请求
    post：处理微信平台发送来的消息
    '''
    # 1，解析3个请求鉴权参数
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')

    # 2、调用鉴权接口
    if not wechat.check_signature(signature, timestamp, nonce):
        logger.info('check_signature fail')
        return HttpResponseForbidden()

    # 3、如果是get鉴权，返回echostr；如果是post，则进行消息处理
    if request.method == 'GET':
        echostr = request.GET.get('echostr')
        logger.info('wx reg succ')
        return HttpResponse(echostr)
    elif request.method == 'POST':
        return handler_wxmp_req(request.body)
    else:
        logger.error('get unhandler method:' + request.method)
        return HttpResponseBadRequest()


def handler_wxmp_req(body):
    '''
    处理微信公众号推送过来的消息
    '''
    # 1、解析消息
    try:
        wechat.parse_data(body)
    except ParseError:
        logger.error('parse wx_msg fail, msg: ' + body)
        return HttpResponseBadRequest()

    # 2、根据openid查询用户信息
    userid = wechat.message.source
    user = User.get_user_by_openid(userid)
    username = userid
    if user is not None:
        username = user.rtx

    # 3、分类型处理
    msg = wechat.message

    if isinstance(msg, EventMessage):
        # 如果是关注事件
        if msg.type == 'subscribe' and msg.key is None:
            # 无论新老用户，都给出流程指引
            content = gen_user_help(user)

            # 如果是老用户，欢迎再关注
            if user is not None:
                welcome = '欢迎回来，{rtx} ^_^\r\n'.format(rtx=user.rtx)
                content = welcome + content
                logger.info(username + ' back to subscribe')
            else:
                logger.info(username + ' subscribe')
        # 如果是其他事件，直接返回流程指引
        else:
            content = gen_user_help(user)
            logger.info('get event: ' + msg.type +
                        ', send user_help to ' + username)

        rsp = wechat.response_text(content=content)
    # 文本消息单独处理
    elif isinstance(msg, TextMessage):
        rsp = hanlder_txt_msg()
    # 如果是其他类型消息，直接返回流程指引
    else:
        content = gen_user_help(user)
        rsp = wechat.response_text(content=content)
        logger.info('get msg: ' + msg.type + ', send user_help to ' + username)

    # 返回最终的响应
    return HttpResponse(rsp)


def hanlder_txt_msg():
    # 得到用户发送的文本
    txt = wechat.message.content.strip()

    # 获取用户并得到检查结果
    user = User.get_user_by_openid(wechat.message.source)
    (user_check_ret, user_check_info) = check_user(user)

    # 导出组织结构信息
    # add 20220427 zhuofu
    if txt == '0427':
        content = gen_org_help()
        return wechat.response_text(content=content)
    # 如何注册
    if txt == '1':
        content = gen_reg_help()
        return wechat.response_text(content=content)
    # 查看注册信息
    if txt == '2':
        content = gen_user_info()
        return wechat.response_text(content=content)
    # 如何提交报销
    if txt == '3':
        content = gen_add_help()
        return wechat.response_text(content=content)
    # 查看未报销记录
    if txt == '4':
        # 用户未注册 or 未审核
        if not user_check_ret:
            return wechat.response_text(content=user_check_info)
        else:
            logger.info('{} view expense_list(expense=False)'.format(user.rtx))
            content = gen_expense_info(user, False)
            return wechat.response_text(content=content)
    # 查看已报销记录
    if txt == '5':
        # 用户未注册 or 未审核
        if not user_check_ret:
            return wechat.response_text(content=user_check_info)
        else:
            logger.info('{} view expense_list(expense=True)'.format(user.rtx))
            content = gen_expense_info(user, True)
            return wechat.response_text(content=content)
    # 如何反馈
    if txt == '6':
        content = gen_fankui_help()
        return wechat.response_text(content=content)
    # 绑定wxapp
    if txt.startswith(u'绑定 '):
        # 用户未注册 or 未审核
        if not user_check_ret:
            return wechat.response_text(content=user_check_info)
        else:
            # 如果用户已经绑定，直接返回
            qs = AppUser.objects.filter(user_id=user.id)
            if qs.exists():
                nickname = qs[0].nickname.encode('utf8', 'ignore')
                bindtime = qs[0].bind_time.strftime('%Y-%m-%d %H:%M:%S')
                content = '您已绑定过小程序\n绑定用户: {}\n绑定时间: {}'.format(nickname, bindtime)
                return wechat.response_text(content=content)

            # 先检查输入的合法性
            (ret, active_code) = parse_active_req(txt)
            if not ret:
                content = '您输入的格式有误\n\n'
                content += '请输入‘绑定 xxxx’\n(xxxx为小程序的4位绑定码)'
                return wechat.response_text(content=content)

            # 获取memcache中的active_info
            (ret, openid, nickname) = get_actvie_info_from_memcache(active_code)
            if not ret:
                content = '绑定码错误或过期，请重新获取'
                return wechat.response_text(content=content)

            # 绑定用户
            try:
                appUser = AppUser(pk=openid, user_id=user.id,
                                  nickname=nickname)
                appUser.save()
            except Exception as e:
                logger.error('add AppUser fail, rtx: {}, wxappopenid: {}, nickname: {}, code: {}, exception: {}'.format(
                    user.rtx, openid, nickname, active_code, str(e)))
                content = '绑定失败，请联系管理员zhuofu'
                return wechat.response_text(content=content)

            # 运行到这里，说明绑定成功了
            logger.info('{} bind wxapp succ, wx openid: {}, nickname: {}'.format(
                user.rtx, openid, nickname))

            # 返回确认信息
            content = '绑定成功\n小程序用户：{}'.format(nickname)
            return wechat.response_text(content=content)
    # 提交报销
    if txt.startswith(u'添加'):
        # 用户未注册 or 未审核
        if not user_check_ret:
            return wechat.response_text(content=user_check_info)
        else:
            # 先检查输入的合法性
            (ret, expinfo) = parse_add_expense(txt)
            if not ret:
                content = '您输入的格式有误\n\n'
                content += gen_add_help()
                return wechat.response_text(content=content)

            # 添加报销请求到缓存
            add_expense_req_to_memcached(user, expinfo)
            logger.info('{} add expense_req to memcache, money:{}'.format(
                user.rtx, expinfo[0]))

            # 返回确认信息
            content = gen_exp_add_req_info(expinfo)
            return wechat.response_text(content=content)
    # 确认报销
    if txt == '0':
        # 用户未注册 or 未审核
        if not user_check_ret:
            return wechat.response_text(content=user_check_info)
        else:
            exp_req = pop_expense_req(user)

            # req为None说明未请求 or 请求已过期
            if exp_req is None:
                content = '未提交报销 或 请求已过期\n\n'
                content += gen_add_help()
                return wechat.response_text(content=content)

            # 添加报销到db
            new_teacharge = TeaCharge(team_id=exp_req[0], user_id=exp_req[1], charge_time=exp_req[2],
                                      money=exp_req[3], remark=exp_req[4])
            new_teacharge.save()
            logger.warn('{} add expense to db, TeaCharge:{}'.format(
                user.rtx, new_teacharge))

            content = gen_exp_add_ret_info(new_teacharge)
            return wechat.response_text(content=content)
    # 取消报销
    if txt == '999':
        # 用户未注册 or 未审核
        if not user_check_ret:
            return wechat.response_text(content=user_check_info)
        else:
            exp_req = pop_expense_req(user)

            # req为None说明未请求 or 请求已过期
            if exp_req is None:
                content = '未提交报销 或 请求已过期\n\n'
                content += gen_add_help()
                return wechat.response_text(content=content)

            logger.info('{} del expense from memcache'.format(user.rtx))

            # pop_expense_req操作后，缓存中的请求已删除，发送取消成功消息
            content = '报销请求已取消！'
            return wechat.response_text(content=content)
    # 处理反馈
    if txt.startswith(u'反馈'):
        # 用户未注册 or 未审核
        if not user_check_ret:
            return wechat.response_text(content=user_check_info)
        else:
            # 将反馈内容发送邮件
            send_fankui_mail(user, txt)
            logger.info('{} send a fankui msg'.format(user.rtx))

            return wechat.response_text(content='已收到，谢谢您的反馈')
    # 处理注册
    if txt.startswith(u'注册'):
        # 已注册并审核通过
        if user_check_ret:
            team_name = Team.get_name_by_id(user.team_id).encode('utf8')
            content = '您已注册\n企业微信：{}小组：{}\n\n修改信息请联系管理员(zhuofu)'.format(
                user.rtx, team_name)
            return wechat.response_text(content=content)
        # 未注册 or 未审核
        else:
            # 先检查输入的合法性
            (ret, reg_req) = parse_register_req(txt)
            if not ret:
                content = '您输入的格式有误\n\n'
                content += gen_reg_help()
                return wechat.response_text(content=content)

            reg_info = gen_reg_info(reg_req)

            # 未注册，则在db中添加注册信息
            if user is None:
                content = '新用户注册：\n'

                user = User(rtx=reg_req[0], openid=wechat.message.source,
                            team_id=reg_req[1], status=0, is_admin=False)
                user.save()

                logger.warn(
                    '{} add register info, User:{}'.format(user.rtx, user))
            # 未审核，则更新db中的注册信息
            else:
                content = '注册信息更新为：\n'

                user.rtx = reg_req[0]
                user.team_id = reg_req[1]
                user.save()

                logger.warn(
                    '{} update register info, User:{}'.format(user.rtx, user))

            content += reg_info

            # 发送注册提醒邮件
            send_reg_mail(user, content)

            # 返回注册确认信息
            content += '\n\n待管理员(zhuofu)审核\n可发送‘2’查看注册进度'
            return wechat.response_text(content=content)
    # 查看未报销统计信息(管理员)
    if user is not None and user.is_admin and txt == '7':
        unexp_info = get_unexp_teacharge_info(user)

        # 如果没有，直接返回
        if unexp_info['tc_num'] == 0:
            return wechat.response_text(content='没有未报销记录')

        summery = gen_summery(unexp_info)

        logger.info('{} view the summery'.format(user.rtx))
        return wechat.response_text(content=summery)
    # 导出未报销统计信息(管理员)
    if user is not None and user.is_admin and txt == '8':
        unexp_info = get_unexp_teacharge_info(user)

        # 如果没有，直接返回
        if unexp_info['tc_num'] == 0:
            return wechat.response_text(content='没有未报销记录')

        summery = gen_summery(unexp_info)

        filepath = export_to_csv(unexp_info)

        send_summery_mail(user, summery, filepath)

        logger.info('{} export the summery'.format(user.rtx))
        return wechat.response_text(content='信息已发送公司邮箱，请查收')
    # 请求报销所有未报销记录(管理员)
    if user is not None and user.is_admin and txt == '9':
        unexp_info = get_unexp_teacharge_info(user)
        confirm_info = gen_charge_confirm_info(unexp_info)

        # 如果没有，直接返回
        if unexp_info['tc_num'] == 0:
            return wechat.response_text(content='没有未报销记录')

        # 将报销请求写入memcache
        add_charge_req_to_memcache(user, unexp_info)

        logger.warn('{} add charge_req to memcache, num:{}, moeny:{}'.format(
            user.rtx, unexp_info['tc_num'], unexp_info['tc_total']))
        return wechat.response_text(content=confirm_info)
    # 确认报销所有未报销记录(管理员)
    if user is not None and user.is_admin and txt == '571':
        # 提取请求
        charge_req = pop_charge_req(user)

        # req为None说明未请求 or 请求已过期
        if charge_req is None:
            content = '未提交请求 或 请求已过期'
            return wechat.response_text(content=content)

        # 将请求中的teacharge都设置为已报销
        (num, money) = do_charge_req(charge_req)

        logger.warn('{} confirm charge_req, ids:{}'.format(
            user.rtx, repr(charge_req)))

        content = '报销成功！\n\n修改报销记录 {} 条，金额 {} 元'.format(num, money)
        return wechat.response_text(content=content)
    # 手动出发备份(管理员)
    if user is not None and user.is_admin and txt == u'备份':
        (ret, info) = backup_to_cos()
        if ret:
            content = '备份成功，请查收邮件'
        else:
            content = '备份失败，错误:' + info
        return wechat.response_text(content=content)
    # 运行到这里，说明没有匹配上任何命令，返回帮助
    content = gen_user_help(user)
    return wechat.response_text(content=content)


def parse_active_req(txt):
    if not txt.startswith(u'绑定 '):
        return (False, None)

    index = len(u'绑定 ')
    active_code = txt[index:]
    if len(active_code) != 4:
        return (False, None)

    if active_code.isdigit():
        return (True, active_code)
    else:
        return (False, None)


def get_actvie_info_from_memcache(active_code):
    key = 'wxapp_actvie_code_' + active_code
    active_info = cache.get(key)

    # 提取后，需要删除
    cache.delete(key)

    if active_info is None:
        return (False, None, None)
    else:
        return (True, active_info['openid'], active_info['nickname'])


def do_charge_req(charge_req):
    total = 0
    for tcid in charge_req:
        tc = TeaCharge.objects.get(pk=tcid)
        tc.expense = True
        total += tc.money
        tc.save()

    return (len(charge_req), total)


def gen_charge_confirm_info(unexp_info):
    summery = '''未报销记录：
总数量：{} 笔
总金额：{} 元

确认要将这{}笔记录修改为‘已报销’吗？
确认请发送'571'

3分钟内未确认将自动取消
'''.format(unexp_info['tc_num'], unexp_info['tc_total'], unexp_info['tc_num'])
    return summery


def export_to_csv(unexp_info):
    filename = '/tmp/apd_happytea_detail_list.csv'

    csvfile = file(filename, 'wb')
    csvfile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvfile)

    writer.writerow(['企业微信', '小组', '金额', '时间', '备注'])
    csv_data = []
    for tc in unexp_info['tc_list']:
        csv_data.append((tc['user_name'].encode('utf8'), tc['team_name'], str(tc['money']),
                         tc['time'], tc['remark'].encode('utf8')))
    writer.writerows(csv_data)
    csvfile.close()

    return filename


def gen_summery(unexp_info):
    summery = '''未报销统计：
总数量：{} 笔
总金额：{} 元

'''.format(unexp_info['tc_num'], unexp_info['tc_total'])

    for team_info in unexp_info['team_list']:
        if team_info['tc_num'] == 0:
            team_str = '{}：无\n'.format(team_info['name'])
        else:
            team_str = '''{}：
数量：{} 笔
金额：{} 元
'''.format(team_info['name'], team_info['tc_num'], team_info['tc_total'])
            for userid in team_info['user_dict']:
                user_info = team_info['user_dict'][userid]
                user_str = '{}：{} 元 ({}笔)\n'.format(user_info['name'], user_info[
                    'tc_total'], user_info['tc_num'])

                team_str += user_str

            team_str += '\n'

        summery += team_str

    return summery


def gen_reg_info(reg_req):
    reg_info = '企业微信：{}\n小组：{}'.format(reg_req[0], reg_req[2])
    return reg_info


def parse_register_req(txt):
    try:
        items = txt.split(u' ')
        item_num = len(items)
        if item_num != 3:
            return (False, None)

        # rtx名必须全部是字母
        rtx = items[1].encode('utf8').lower()
        if not re.match('^[a-z]+$', rtx):
            return (False, None)

        # team_name 必须在范围内
        team_name = items[2].encode('utf8')
        tms = Team.objects.filter(name=team_name)
        if len(tms) != 1:
            return (False, None)

        reg_req = (rtx, tms[0].id, team_name)
        return (True, reg_req)
    except Exception:
        return (False, None)


def send_summery_mail(user, content, filepath):
    mail_title = '【架平下午茶】下午茶消费信息统计'.format(user.rtx)
    mail_txt = content
    sender = settings.EMAIL_HOST_USER
    receiver = ['{}@tencent.com'.format(user.rtx)]
    email = EmailMultiAlternatives(mail_title, mail_txt, sender, receiver)
    email.attach_alternative(mail_txt, 'text/plain')
    email.attach_file(filepath)
    email.send()


def send_reg_mail(user, content):
    mail_title = '【架平下午茶】收到来自 {} 的注册请求'.format(user.rtx)
    mail_txt = content
    sender = settings.EMAIL_HOST_USER
    receiver = maillist_user_reg
    email = EmailMultiAlternatives(mail_title, mail_txt, sender, receiver)
    email.attach_alternative(mail_txt, 'text/plain')
    email.send()


def send_fankui_mail(user, txt):
    mail_title = '【架平下午茶】收到来自 {} 的反馈'.format(user.rtx)
    mail_txt = txt.encode('utf8')
    sender = settings.EMAIL_HOST_USER
    receiver = maillist_fankui
    email = EmailMultiAlternatives(mail_title, mail_txt, sender, receiver)
    email.attach_alternative(mail_txt, 'text/plain')
    email.send()


def pop_expense_req(user):
    add_key = user.rtx + '_add_exp'
    exp_req = cache.get(add_key)

    # 提取后，需要删除
    cache.delete(add_key)

    return exp_req


def pop_charge_req(user):
    add_key = user.rtx + '_add_charge'
    charge_req = cache.get(add_key)

    # 提取后，需要删除
    cache.delete(add_key)

    return charge_req


def add_charge_req_to_memcache(user, unexp_info):
    add_key = user.rtx + '_add_charge'
    add_value = []
    for tc in unexp_info['tc_list']:
        add_value.append(tc['id'])
    cache.set(add_key, add_value, memcached_timeout)


def add_expense_req_to_memcached(user, expinfo):
    add_key = user.rtx + '_add_exp'
    add_value = (user.team_id, user.id, expinfo[1], expinfo[0], expinfo[2])
    cache.set(add_key, add_value, memcached_timeout)


def gen_exp_add_ret_info(teacharge):
    time_str = teacharge.charge_time.strftime('%Y-%m-%d')
    ret_info = '''添加成功！

金额：{}
时间：{}
备注：{}
'''.format(teacharge.money, time_str, teacharge.remark.encode('utf8'))
    return ret_info


def gen_exp_add_req_info(expinfo):
    time_str = expinfo[1].strftime('%Y-%m-%d')
    req_info = '''报销信息：
金额：{}
时间：{}
备注：{}

确认提交，请发送‘0’
取消，请发送‘999’

3分钟内未确认将自动取消
    '''.format(expinfo[0], time_str, expinfo[2].encode('utf8'))

    return req_info


def check_user(user):
    # 如果未注册，则返回注册说明
    if user is None:
        content = gen_user_info()
        return (False, content)

    # 如果未审核，则提醒要审核
    if user.status == 0:
        content = gen_check_info()
        return (False, content)

    return (True, None)


def parse_add_expense(txt):
    try:
        items = txt.split(u' ')
        item_num = len(items)
        # 参数的个数应该大于 2 个：添加 金额 [时间] [备注]
        if item_num >= 2:
            # 1 解析 金额，并判断是否大于0
            money = float(items[1])
            if money <= 0:
                return (False, None)

            # 2 解析 时间，如没有，则使用当天
            if item_num >= 3:
                try:
                    charge_time = datetime.datetime.strptime(
                        items[2], '%Y%m%d')
                except Exception:
                    return (False, None)
            else:
                charge_time = datetime.datetime.now()

            # 解析 备注，如没有，则设置‘’
            if item_num >= 4:
                remarks = items[3:]
                remark = ' '.join(remarks)
            else:
                remark = ''

            return (True, (money, charge_time, remark))
        else:
            return (False, None)
    except Exception:
        return (False, None)


def gen_expense_info(user, expense=False):
    team_id = user.team_id
    team_name = Team.get_name_by_id(team_id).encode('utf8')
    teacharge_list = TeaCharge.objects.filter(
        team_id=team_id, expense=expense).order_by('-charge_time')
    num = len(teacharge_list)
    str_expense = '已报销' if expense else '未报销'

    # 最大展示记录条数
    max_num = 20
    if num == 0:
        expense_info = '{} 目前没有{}记录'.format(team_name, str_expense)
    else:
        total = 0
        index = 1
        detail_list = ''
        for teacharge in teacharge_list:
            total += teacharge.money
            time_str = teacharge.charge_time.strftime('%Y-%m-%d')
            t_user = User.get_user_by_id(teacharge.user_id)
            rtx = '该用户已注销' if t_user is None else t_user.rtx

            # 超过限制的条数不展示
            if index > max_num:
                index += 1
                continue
            detail_list += '''
第 {} 笔
金额：{}
时间：{}
报销人：{}
备注：{}\n'''.format(index, teacharge.money, time_str, rtx, teacharge.remark.encode('utf8'))
            index += 1

        max_tips = '' if index <= max_num else '（最多展示 {} 条记录）'.format(max_num)
        expense_info = '{} 有 {} 笔{}费用，总计 {} 元\n\n详细列表{}:\n{}'.format(
            team_name, num, str_expense, total, max_tips, detail_list)

    return expense_info


def gen_user_info():
    userid = wechat.message.source
    user = User.get_user_by_openid(userid)

    if user is None:
        # 如果未注册，则提醒用户注册
        userinfo = '您还未注册，请先注册，谢谢！\n\n'
        userinfo += gen_reg_help()
    else:
        # 如果已注册 or 注册中，给出注册信息
        team_id = user.team_id
        status = user.status
        team_name = Team.get_name_by_id(team_id).encode('utf8')
        status_str = '已注册' if status == 1 else '待审核'

        userinfo = '''企业微信: {}
小组: {}
状态: {}'''.format(user.rtx, team_name, status_str)

        # 判断是否绑定小程序
        qs = AppUser.objects.filter(user_id=user.id)
        userinfo += '\n小程序: '
        userinfo += '已绑定' if qs.exists() else '未绑定'

        # 如果是管理员，给出提示
        if user.is_admin:
            userinfo += '\n管理员：已授权'

        # 如果是未审核，则给出提醒
        if status == 0:
            userinfo += '\n\n' + gen_check_info()
        elif status == 1:
            userinfo += '\n\n修改信息请联系管理员(zhuofu)'

    return userinfo


def gen_check_info():
    check_info = '''审核通过才能进行其他操作\n可提醒管理员(zhuofu)尽快审核'''
    return check_info


def gen_org_help():
    org_info = ''
    centers = Center.objects.all()
    for center in centers:
        org_info += '{}\n'.format(center.name.encode('utf8'))
        teams = Team.objects.filter(center_id=center.id)
        for team in teams:
            org_info += '\t\t{}({})\n'.format(team.name.encode('utf8'), team.id)
            users = User.objects.filter(team_id=team.id)
            for user in users:
                if user.status == 1:
                    org_info += '\t\t\t\t{}\n'.format(user.rtx)
    return org_info


def get_unexp_teacharge_info(user=None):
    '''
    得到未报销的记录信息
    user：动作发起人，默认为None。如果为None，则获取所有小组的；否则，获取user所在中心的小组
    '''

    # 得到需要导出的team_id列表，如果user为None，则导出所有的
    teamid_list = get_rel_teams(user)

    # 进行统计
    all_team_list = []
    all_tc_list = []
    all_tc_num = 0
    all_tc_total = 0

    # 逐个组统计
    for teamid in teamid_list:
        teamname = Team.get_name_by_id(teamid).encode('utf8')
        tcs = TeaCharge.objects.filter(team_id=teamid, expense=False)

        team_tc_total = 0
        team_tc_num = len(tcs)
        team_tc_list = []
        team_user_dict = {}

        for tc in tcs:
            user_id = tc.user_id
            username = User.get_user_by_id(user_id).rtx
            if user_id not in team_user_dict:
                team_user_dict[user_id] = {'tc_num': 0, 'tc_total': 0,
                                           'tc_list': [], 'name': username}

            tc_info = {'team_name': teamname, 'user_name': username,
                       'team_id': tc.team_id, 'user_id': tc.user_id,
                       'time': tc.charge_time.strftime('%Y-%m-%d'),
                       'money': tc.money, 'remark': tc.remark,
                       'id': tc.id}

            # 统计个人的
            team_user_dict[user_id]['tc_num'] += 1
            team_user_dict[user_id]['tc_total'] += tc.money
            team_user_dict[user_id]['tc_list'].append(tc_info)

            # 统计小组的
            team_tc_total += tc.money
            team_tc_list.append(tc_info)

            all_tc_list.append(tc_info)

        all_tc_num += team_tc_num
        all_tc_total += team_tc_total
        all_team_list.append({'name': teamname, 'team_tc_list': team_tc_list,
                              'tc_total': team_tc_total, 'tc_num': team_tc_num,
                              'team_id': teamid, 'user_dict': team_user_dict})

    unexp_info = {'tc_num': all_tc_num, 'tc_list': all_tc_list,
                  'tc_total': all_tc_total, 'team_list': all_team_list}

    return unexp_info


def get_rel_teams(user=None):
    # 返回所有team的id列表
    team_id_list = []
    qs = Team.objects.all()
    for team in qs:
        team_id_list.append(team.id)

    return team_id_list


def gen_user_help(user):
    user_help = '''通过本公众号，您可以进行’提交报销‘、’查看报销记录‘等操作

注册成功才能进行其他操作

发送‘1’查看如何注册
发送‘2’查看注册信息
发送‘3’查看如何提交报销
发送‘4’查看本组未报销记录
发送‘5’查看本组已报销记录
发送’6‘查看如何反馈
'''

    # 如果是管理员，加上管理员命令菜单
    if user is not None and user.is_admin:
        user_help += '''发送‘7’查看未报销统计
发送‘8’导出未报销记录
发送‘9’报销全部未报销记录
'''

    return user_help


def gen_add_help():
    add_hlep = '''提交报销说明：
1、发送提交请求
发送：'添加'+空格+金额+空格+[时间]+空格+[备注]
例如：添加 98.2
或者：添加 98.2 20170219
或者：添加 98.2 20170219 参加人数较多，加量 卤味+水果

’时间‘为可选，格式必须为’YYYYMMDD‘；不填，则自动设置为当天
’备注‘为可选，如果填写’备注‘，必须填写’时间‘

2、接收确认信息
系统验证提交信息合法后，返回待提交信息
用户检查信息是否正确

3、确认/取消提交
发送’0‘确认并提交
发送’999‘取消提交
'''
    return add_hlep


def gen_reg_help():
    reg_hlep = '''注册说明：
1、发送注册请求
发送：'注册'+空格+企业微信+空格+小组名
例如：注册 zhuofuliu 接入测试组
小组名：'接入运维组'，'接入测试组'，'加速运维组'...
若注册失败请联系管理员（zhuofu）

2、等待管理员(zhuofu)审核
申请注册后，系统会通知管理员
审核通过后，系统会有邮件提醒
可以发送’2‘随时查看
'''
    return reg_hlep


def gen_fankui_help():
    fankui_help = '''反馈说明：
发送：'反馈'+空格+反馈内容
例如：反馈 请问可以支持语音输入吗？
'''
    return fankui_help


def backup_to_cos():
    logger.info('begin backup_to_cos')
    try:
        time_str = datetime.datetime.now().strftime('%Y%m%d')
        filename = 'happytea_{}.sql'.format(time_str)
        backup_path = '/data/mysql/backup/happytea/'
        file_path = backup_path + filename

        # 如果文件不在，抛异常
        if not os.path.isfile(file_path):
            raise Exception(
                'sql export file not exist, path:{}'.format(file_path))

        cos_client = CosClient(settings.COS_APPID, settings.COS_SECRET_ID,
                               settings.COS_SECRET_KEY, settings.COS_REGION)
        cos_upload_req = UploadFileRequest(
            u'happytea', u'/' + filename.decode('utf8'), file_path.decode('utf8'))
        # 允许覆盖
        cos_upload_req.set_insert_only(0)
        cos_upload_rsp = cos_client.upload_file(cos_upload_req)

        if cos_upload_rsp['code'] != 0:
            raise Exception('cos upload fail, info:{}'.format(
                cos_upload_rsp['message']))

        # 如果运行到这里，说明成功了
        if datetime.datetime.now().weekday() == 0:
            mail_title = '【架平下午茶】数据备份'
            mail_txt = '见附件'
            sender = settings.EMAIL_HOST_USER
            receiver = maillist_fankui
            email = EmailMultiAlternatives(
                mail_title, mail_txt, sender, receiver)
            email.attach_alternative(mail_txt, 'text/plain')
            email.attach_file(file_path)
            email.send()

        logger.info('backup_to_cos succ.')
        return (True, None)
    except Exception as e:
        logger.error('backup_to_cos fail, err:' + str(e))
        mail_title = '【架平下午茶】备份sql失败！！！'
        mail_txt = '失败原因：' + str(e)
        sender = settings.EMAIL_HOST_USER
        receiver = maillist_fankui
        email = EmailMultiAlternatives(mail_title, mail_txt, sender, receiver)
        email.attach_alternative(mail_txt, 'text/plain')
        email.send()
        return (False, str(e))
