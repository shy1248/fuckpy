#!/usr/bin/env python
# -*- coding=UTF-8 -*-

'''
@ Author: shy
@ Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@ Version: v1.0
@ Description: -
@ Since: 2020/5/28 17:50
'''

from __future__ import print_function
from __future__ import unicode_literals

import os
import logging
import __main__
from logging import handlers

from utils import singleton


__all__ = ['SimpleLogger']

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# The background is set with 40 plus the number of the color, and the foreground with 30
# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

COLORS = {'WARNING': CYAN, 'INFO': MAGENTA, 'DEBUG': BLUE, 'CRITICAL': YELLOW, 'ERROR': RED}


class ColoredFormatter(logging.Formatter):
    origrecord = None

    def __init__(self, msg, colored=True):
        logging.Formatter.__init__(self, msg)
        self.colored = colored

    def format(self, record):
        levelname = record.levelname
        prefix_colored = COLOR_SEQ % (30 + COLORS[levelname])
        if self.colored and levelname in COLORS:
            record.msg = prefix_colored + record.msg + RESET_SEQ
        else:
            if prefix_colored in record.msg:
                record.msg = record.msg[len(prefix_colored)::].replace(RESET_SEQ, '')
            else:
                pass
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
        self.handler = handler
        self.logfile = logfile
        self.level = level

        # log format
        self.ch_format = '%(message)s'
        self.fh_format = '[%(asctime)s] - [%(levelname)s]: %(message)s'
        SimpleLogger.__logger.setLevel(logging.DEBUG)

        if self.handler != SimpleLogger.FILE:
            # add console handler
            self.ch = logging.StreamHandler()
            self.ch.setLevel(self.level)
            self.ch.setFormatter(ColoredFormatter(self.ch_format, colored=True))
            SimpleLogger.__logger.addHandler(self.ch)

        if self.handler != SimpleLogger.CONSOLE:
            if self.logfile is None:
                appname = os.path.splitext(__main__.__file__)[0]
                # log file name
                self.logfile = '%s.log' % appname

            # add file handler
            self.fh = handlers.TimedRotatingFileHandler(
                    self.logfile, when='MIDNIGHT', interval=1, backupCount=3, encoding='utf8')
            self.fh.setLevel(self.level)
            self.fh.setFormatter(ColoredFormatter(self.fh_format, colored=False))
            SimpleLogger.__logger.addHandler(self.fh)

    @classmethod
    def debug(cls, msg, *args, **kwargs):
        SimpleLogger.__logger.debug(msg, *args, **kwargs)

    @classmethod
    def info(cls, msg, *args, **kwargs):
        SimpleLogger.__logger.info(msg, *args, **kwargs)

    @classmethod
    def warn(cls, msg, *args, **kwargs):
        SimpleLogger.__logger.warn(msg, *args, **kwargs)

    @classmethod
    def error(cls, msg, *args, **kwargs):
        SimpleLogger.__logger.error(msg, *args, **kwargs)

    @classmethod
    def critical(cls, msg, *args, **kwargs):
        SimpleLogger.__logger.critical(msg, *args, **kwargs)


if __name__ == '__main__':
    logger = SimpleLogger(handler=SimpleLogger.CONSOLE, level=SimpleLogger.D)
    logger.debug('Logging DEBUG example 中文测试 ...'.encode('gbk'))
    logger.info('Logging INFO example ...')
    logger.warn('Logging WARN example ...')
    logger.error('Logging ERROR example ...')
    logger.critical('Logging CRITICAL example ...')
