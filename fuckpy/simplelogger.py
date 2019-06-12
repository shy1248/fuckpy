#!/usr/bin/env python
# -*- coding=UTF-8 -*-
'''
@Author: shy
@Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@Version: v1.0
@Description: -
@Since: 2019-01-06 18:16:13
@ LastTime: 2019-07-10 09:56:00
'''

__all__ = ['SimpleLogger']

import os
import sys
import __main__
import logging
from logging import handlers

from singleton import singleton
from sysinfo import SYS_TYPE

reload(sys)
sys.setdefaultencoding('utf-8')

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# The background is set with 40 plus the number of the color, and the foreground with 30

# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

COLORS = {
    'WARNING': CYAN,
    'INFO': MAGENTA,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}


class ColoredFormatter(logging.Formatter):
    origrecord = None

    def __init__(self, msg, colored=True):
        logging.Formatter.__init__(self, msg)
        self.colored = colored

    def format(self, record):
        # TODO: waitting for implemention on windows platform
        if SYS_TYPE == 'Windows':
            return logging.Formatter.format(self, record)

        levelname = record.levelname
        if self.colored and levelname in COLORS:
            record.msg = COLOR_SEQ % (
                30 + COLORS[levelname]) + record.msg + RESET_SEQ
        else:
            record.msg = record.msg[len(COLOR_SEQ)::].replace(RESET_SEQ, '')
        return logging.Formatter.format(self, record)

@singleton
class SimpleLogger(object):
    CONSOLE = 1
    FILE = 2
    BOTH = 3
    # all levels
    D = logging.DEBUG
    I = logging.INFO
    W = logging.WARN
    E = logging.ERROR
    C = logging.CRITICAL

    __logger = logging.getLogger(os.path.split(__file__)[1])

    def __init__(self, handler=CONSOLE, logfile=None, level=I):
        # log format
        ch_format = '%(message)s'
        fh_format = '[%(asctime)s] - [%(levelname)s]: %(message)s'
        SimpleLogger.__logger.setLevel(logging.DEBUG)

        if handler != SimpleLogger.FILE:
            # add console handler
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(ColoredFormatter(ch_format, colored=True))
            SimpleLogger.__logger.addHandler(ch)

        if handler != SimpleLogger.CONSOLE:
            if logfile is None:
                appname = os.path.splitext(__main__.__file__)[0]
                # log file name
                logfile = '%s.log' % appname

            # add file handler
            fh = handlers.TimedRotatingFileHandler(
                logfile, when='D', interval=1, backupCount=3, encoding='utf8')
            fh.setLevel(level)
            fh.setFormatter(ColoredFormatter(fh_format, colored=False))
            SimpleLogger.__logger.addHandler(fh)

    @staticmethod
    def debug(msg, *args, **kwargs):
        SimpleLogger.__logger.debug(msg, *args, **kwargs)

    @staticmethod
    def info(msg, *args, **kwargs):
        SimpleLogger.__logger.info(msg, *args, **kwargs)

    @staticmethod
    def warn(msg, *args, **kwargs):
        SimpleLogger.__logger.warn(msg, *args, **kwargs)

    @staticmethod
    def error(msg, *args, **kwargs):
        SimpleLogger.__logger.error(msg, *args, **kwargs)

    @staticmethod
    def critical(msg, *args, **kwargs):
        SimpleLogger.__logger.critical(msg, *args, **kwargs)


if __name__ == '__main__':

    logger = SimpleLogger(handler=SimpleLogger.CONSOLE, level=SimpleLogger.D)
    logger.debug(u'Logging DEBUG example中文 ...'.encode('gbk'))
    logger.info('Logging INFO example ...')
    logger.warn('Logging WARN example ...')
    logger.error('Logging ERROR example ...')
    logger.critical('Logging CRITICAL example ...')
