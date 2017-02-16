from django.core.management.base import BaseCommand
from apps.gohome.tools.account_importor import Importor
import logging


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'gohome app cmd'

    def add_arguments(self, parser):
        parser.add_argument('-r',
                            '--run',
                            dest='run',
                            choices=['import_12306',
                                     'import_12306_2',
                                     'clear_account',
                                     'update_wuyi_task',
                                     'null'],
                            default='null',
                            help='choose a cmd to run')

        parser.add_argument('-f',
                            '--file',
                            dest='fpath',
                            default='null',
                            help='input file path')

    def handle(self, *args, **options):
        run_cmd = options['run']
        fpath = options['fpath']

        if run_cmd == 'null':
            logger.info('run cmd is null')

        elif run_cmd == 'import_12306':
            logger.info('run cmd: import_12306')

            imptor = Importor()
            imptor.import_12306_accout(fpath)

            logger.info('run cmd succ')

        elif run_cmd == 'import_12306_2':
            logger.info('run cmd: import_12306_2')

            imptor = Importor()
            imptor.import_12306_account2(fpath)

            logger.info('run cmd succ')

        elif run_cmd == 'clear_account':
            logger.info('run cmd: clear_account')

            imptor = Importor()
            imptor.clear()

            logger.info('run cmd succ')
        elif run_cmd == 'update_wuyi_task':
            logger.info('run cmd: update_wuyi_task')

            imptor = Importor()
            if imptor.update_wuyi_task(fpath):
                logger.info('run cmd succ')
            else:
                logger.info('run cmd fail')
        else:
            logger.warning('unhandle cmd: {}'.format(run_cmd))
            pass
