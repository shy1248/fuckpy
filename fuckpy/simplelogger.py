#!/usr/bin/env python
# -*- coding=UTF-8 -*-
'''
@Author: shy
@Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@Version: v1.0
@Licence: GPLv3
@Description: -
@Since: 2019-01-06 18:16:13
@LastTime: 2019-03-30 14:27:46
'''

import os
import __main__
import logging
from logging import handlers

from sysinfo import SYS_TYPE

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


# log format
ch_format = '%(message)s'
fh_format = '[%(asctime)s] - [%(levelname)s]: %(message)s'
appname = os.path.basename(os.path.splitext(__main__.__file__)[0])
# log file name
logfile = '%s.log' % appname

logger = logging.getLogger(os.path.split(__file__)[1])
logger.setLevel(logging.DEBUG)

# add console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(ColoredFormatter(ch_format, colored=True))
logger.addHandler(ch)
# add file handler
fh = handlers.TimedRotatingFileHandler(
    logfile, when='D', interval=1, backupCount=3, encoding='utf8')
fh.setLevel(logging.INFO)
fh.setFormatter(ColoredFormatter(fh_format, colored=False))
logger.addHandler(fh)

if __name__ == '__main__':
    logger.debug('Logging DEBUG example中文 ...')
    logger.info('Logging INFO example ...')
    logger.warn('Logging WARN example ...')
    logger.error('Logging ERROR example ...')
    logger.critical('Logging CRITICAL example ...')
