#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Date    : 2018-10-28 01:05:15
# @Author  : shy (hengchen2005@gmail.com)
# @Desc    : -
# @Version : $Id$
# @Licence: GPLv3
# @Copyright (c) 2018-2022 shy. All rights reserved.


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
            record.levelname = COLOR_SEQ % (
                30 + COLORS[levelname]) + levelname + RESET_SEQ
        else:
            record.levelname = levelname[len(
                COLOR_SEQ)::].replace(RESET_SEQ, '')
        return logging.Formatter.format(self, record)


# log format
# logformat = '[%(asctime)s] - [%(levelname)s]: %(message)s (%(filename)s:%(lineno)d)'
logformat = '[%(asctime)s] - [%(levelname)s]: %(message)s'
appname = os.path.basename(os.path.splitext(__main__.__file__)[0])
# log file name
logfile = '%s.log' % appname

logger = logging.getLogger(os.path.split(__file__)[1])
logger.setLevel(logging.DEBUG)

# add console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(ColoredFormatter(logformat, colored=True))
logger.addHandler(ch)
# add file handler
fh = handlers.TimedRotatingFileHandler(
    logfile, when='D', interval=1, backupCount=3, encoding='utf8')
fh.setLevel(logging.INFO)
fh.setFormatter(ColoredFormatter(logformat, colored=True))
logger.addHandler(fh)


if __name__ == '__main__':
    logger.debug('Logging DEBUG example中文 ...')
    logger.info('Logging INFO example ...')
    logger.warn('Logging WARN example ...')
    logger.error('Logging ERROR example ...')
    logger.critical('Logging CRITICAL example ...')
