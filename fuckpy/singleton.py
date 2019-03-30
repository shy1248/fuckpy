#!/usr/bin/env python
# -*- coding=UTF-8 -*-
'''
@Author: shy
@Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@Version: v1.0
@Licence: GPLv3
@Description: -
@Since: 2018-11-06 10:44:49
@LastTime: 2019-03-30 14:27:57
'''

from functools import wraps


class Singleton(object):
    '''A singleton implementation using class extend

    usage：
        class MySingletonCalss(Singleton):
            pass

    Variables:
        _instance {dict} -- The dict of instances
    '''

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


def singleton(cls):
    '''A singleton implementation using decorator

    usage:
        @singleton
        class testSingleton(object):
            pass

    Decorators:
        wraps

    Returns:
        [cls] -- A instance of class which be decorated
    '''

    instances = {}

    @wraps(cls)
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance
