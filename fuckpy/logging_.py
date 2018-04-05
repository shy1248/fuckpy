#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: yushuibo
@Copyright (c) 2018 yushuibo. All rights reserved.
@Licence: GPL-2
@Email: hengchen2005@gmail.com
@Create: log.py
@Last Modified: 2018/4/1 22:13
@Desc: 简单的日志配置
"""

import logging
from logging import handlers

# 日志格式
_FORMAT = '%(asctime)s - [%(levelname)s] - %(name)s.%(module)s: %(message)s'


def init(filename=None):
    """
    设置日志的格式以及终端和文件的handler。

    关键字参数：
        filename --
        日志文件名。若不指定，默认为None，即只输出到终端，而不输出文件
    """

    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(_FORMAT)

    # 添加终端handler，并设置默认级别为logging.DEBUG
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # 添加文件handler，并设置默认级别为logging.INFO
    if filename is not None:
        # 设置日志文件按每天分割，并且只保留最近3天的日志文件，文件编码为utf-8
        file = handlers.TimedRotatingFileHandler(
            filename, when='D', interval=1, backupCount=3, encoding='utf8')
        file.setLevel(logging.INFO)
        file.setFormatter(formatter)
        logger.addHandler(file)

    return logger


if __name__ == '__main__':
    logger = init(filename='test.log')
    logger.info('Logging example ...')
