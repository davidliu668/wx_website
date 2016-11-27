import logging


class CmdFilter(logging.Filter):

    def __init__(self):
        pass

    def filter(self, record):
        if record.name.find('management') != -1:
            return True
        return False


class CrontabFilter(logging.Filter):

    def __init__(self):
        pass

    def filter(self, record):
        if record.name.find('crontab') != -1:
            return True
        return False
