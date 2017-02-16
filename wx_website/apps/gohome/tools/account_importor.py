# coding=utf-8
import json
import re
from apps.gohome.models import *
import logging
import os


logger = logging.getLogger(__name__)


class Importor(object):

    def import_12306_accout(self, fpath):
        # 直接用wuyi的任务文件导入
        logger.debug('import file path: ' + fpath)

        fp = open(fpath)
        lines = fp.readlines()
        fp.close()
        logger.debug('load {} lines.'.format(len(lines)))

        account_num = 0
        for line in lines:
            line = line.strip()
            if line == '':
                continue

            jo = json.loads(line)
            user = jo['Username'].encode('utf8', 'ignore')
            passwd = jo['Passwd'].encode('utf8', 'ignore')

            datestr = jo['Date'].encode('utf8', 'ignore')
            datelist = re.split('[\[\]]', datestr)
            datestrlist = []
            for one in datelist:
                if one == '':
                    continue
                datestrlist.append(one)

            start_date = datestrlist[0]
            end_date = datestrlist[-1]

            from_station = jo['From'].encode('utf8', 'ignore')
            end_station = jo['To'].encode('utf8', 'ignore')

            from_station_list = re.split('[\[\]]', from_station)
            from_station_strlist = []
            for one in from_station_list:
                if one == '':
                    continue
                from_station_strlist.append(one)
            from_station = from_station_strlist[0]

            end_station_list = re.split('[\[\]]', end_station)
            end_station_strlist = []
            for one in end_station_list:
                if one == '':
                    continue
                end_station_strlist.append(one)
            end_station = end_station_strlist[0]

            Account.add(name=user, passwd=passwd,
                        from_station=from_station, end_station=end_station,
                        start_date=start_date, end_date=end_date)
            logger.info('import account [{}] - [{}] succ'.format(user, passwd))
            account_num += 1

        logger.info('import {} 12306 account'.format(account_num))

    def import_12306_account2(self, fpath):
        # 从文件中导入空账号，如果新增则添加为空置账号，如果存在则跳过

        # 1 先拉取当前所有账号
        ex_acts_list = Account.objects.all()
        logger.debug('load {} 12306 account in db'.format(len(ex_acts_list)))
        ex_acts_user_list = []
        for ex_act in ex_acts_list:
            ex_acts_user_list.append(ex_act.name)

        # 从文件加载新的账号列表
        fp = open(fpath)
        lines = fp.readlines()
        fp.close()

        new_acts_list = []
        for line in lines:
            line = line.strip()
            if line == '':
                continue
            user_passwd = line.split(',')
            user = user_passwd[0]
            passwd = user_passwd[1]

            new_acts_list.append((user, passwd))

        # 如果账号不在db中，则作为未使用账号导入
        new_act_num = 0
        for new_act in new_acts_list:
            (user, passwd) = new_act
            if user not in ex_acts_user_list:
                Account.add(name=user, passwd=passwd, status=False,
                            start_date=None, end_date=None)
                print user, ' add succ.'
                new_act_num += 1

        logger.info('add {} new 12306 accounts'.format(new_act_num))

    def clear(self):
        logger.info('clear all accounts in db begin')
        Account.objects.all().delete()
        logger.info('clear succ')

    def update_wuyi_task(self, fpath):
        logger.info('begin update_wuyi_task, fpath:{}'.format(fpath))

        if not os.path.isfile(fpath):
            logger.error(
                'file not exist, update_wuyi_task fail, path:{}'.format(fpath))
            return False

        # 读取文件内容
        fp = open(fpath)
        lines = fp.readlines()
        fp.close()

        # 拉取目前已有账号
        ex_acts_list = Account.objects.all()
        logger.info('load {} account in db'.format(len(ex_acts_list)))
        ex_acts_user_list = []
        for ex_act in ex_acts_list:
            ex_acts_user_list.append(ex_act.name)

        insert_num = 0
        update_num = 0
        for line in lines:
            line = line.strip()
            if line == '':
                continue

            jo = json.loads(line)
            user = jo['Username'].encode('utf8', 'ignore')
            passwd = jo['Passwd'].encode('utf8', 'ignore')

            datestr = jo['Date'].encode('utf8', 'ignore')
            datelist = re.split('[\[\]]', datestr)
            datestrlist = []
            for one in datelist:
                if one == '':
                    continue
                datestrlist.append(one)

            start_date = datestrlist[0]
            end_date = datestrlist[-1]

            from_station = jo['From'].encode('utf8', 'ignore')
            end_station = jo['To'].encode('utf8', 'ignore')

            from_station_list = re.split('[\[\]]', from_station)
            from_station_strlist = []
            for one in from_station_list:
                if one == '':
                    continue
                from_station_strlist.append(one)
            from_station = from_station_strlist[0]

            end_station_list = re.split('[\[\]]', end_station)
            end_station_strlist = []
            for one in end_station_list:
                if one == '':
                    continue
                end_station_strlist.append(one)
            end_station = end_station_strlist[0]

            # 如果username已经存在，则update，否则insert
            if user in ex_acts_user_list:
                Account.update_by_name(name=user, passwd=passwd,
                                       from_station=from_station, end_station=end_station,
                                       start_date=start_date, end_date=end_date)
                update_num += 1
            else:
                Account.add(name=user, passwd=passwd,
                            from_station=from_station, end_station=end_station,
                            start_date=start_date, end_date=end_date)
                insert_num += 1

        logger.info('update_wuyi_task succ, insert {} account, update {} account.'.format(insert_num, update_num))
        return True


if __name__ == '__main__':
    pass
