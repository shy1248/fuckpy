#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: yushuibo
@Copyright (c) 2018 yushuibo. All rights reserved.
@Licence: GPL-2
@Email: hengchen2005@gmail.com
@File: singleton.py
@Create: 2018-04-04 22:16:02
@Last Modified: 2018-04-04 22:16:02
@Desc: 单例模式2中常见实现方式
"""

from functools import wraps


# 单例模式类继承实现
class Singleton(object):
    """
    单例模式父类。使用方法：
        class testSingleton(Singleton):
            pass
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


# 单例模式装饰器实现
def singleton(cls):
    """
    单例模式装饰器。使用方法：
        @singleton
        class testSingleton(object):
            pass
    """

    instances = {}

    @wraps(cls)
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance
