from django.core.management.base import BaseCommand
import logging


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'wxmp app cmd'

    def add_arguments(self, parser):
        parser.add_argument('-r',
                            '--run',
                            dest='run',
                            choices=['add_menu', 'null'],
                            default='null',
                            help='choose a cmd to run')

    def handle(self, *args, **options):
        run_cmd = options['run']

        if run_cmd == 'null':
            logger.info('run cmd is null.')
        elif run_cmd == 'add_menu':
            logger.info('run cmd: add_menu')
        else:
            logger.warning('unhandle cmd: {}'.format(run_cmd))
            pass
