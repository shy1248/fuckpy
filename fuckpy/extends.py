#!/usr/bin/env python
# -*- coding=UTF-8 -*-

'''
@Author: shy
@Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@Version: v1.0
@Licence: GPLv3
@Description: -
@Since: 2018-11-03 23:49:07
@LastTime: 2019-03-30 13:20:22
'''


import re
import time
import collections

from datetime import date
from datetime import timedelta


def strtodatetime(strtime):
    fmt = '%Y%m%d%H%M%S'
    strtime = re.sub(r'[^\d]', '', strtime)
    return date.fromtimestamp(
        time.mktime(time.strptime(strtime, fmt[:(len(strtime) - 2 if len(strtime) % 2 == 0 else len(strtime) - 1)])))


class OrderedSet(collections.OrderedDict, collections.MutableSet):
    '''An ordered set implementation'''

    def update(self, *args, **kwargs):
        if kwargs:
            raise TypeError("update() takes no keyword arguments")

        for s in args:
            for e in s:
                self.add(e)

    def add(self, elem):
        self[elem] = None

    def discard(self, elem):
        self.pop(elem, None)

    def __le__(self, other):
        return all(e in other for e in self)

    def __lt__(self, other):
        return self <= other and self != other

    def __ge__(self, other):
        return all(e in self for e in other)

    def __gt__(self, other):
        return self >= other and self != other

    def __repr__(self):
        return 'OrderedSet([%s])' % (', '.join(map(repr, self.keys())))

    def __str__(self):
        return '{%s}' % (', '.join(map(repr, self.keys())))

    difference = property(lambda self: self.__sub__)
    difference_update = property(lambda self: self.__isub__)
    intersection = property(lambda self: self.__and__)
    intersection_update = property(lambda self: self.__iand__)
    issubset = property(lambda self: self.__le__)
    issuperset = property(lambda self: self.__ge__)
    symmetric_difference = property(lambda self: self.__xor__)
    symmetric_difference_update = property(lambda self: self.__ixor__)
    union = property(lambda self: self.__or__)


class DateRange(object):
    '''An iterator for day, which can be itrete for year, month, week and day'''

    def __init__(self, start=None, stop=None, step=1):
        current = date.fromtimestamp(time.time())
        self.start = current if not start else strtodatetime(start)
        self.stop = current if not stop else strtodatetime(stop)
        self.step = step

        if not isinstance(step, int) or step <= 0:
            raise StopIteration("Iteration[step] must be a non zero positive interger.")

        if self.start >= self.stop:
            raise StopIteration('Iteration[start] >= Interation[stop].')

    def years(self, outfmt='%Y'):
        t = self.start
        while t <= self.stop:
            yield t.strftime(outfmt)
            next_ = date(t.year + self.step, t.month, t.day)
            t = next_

    def months(self, outfmt='%Y%m'):
        t = self.start
        while t <= self.stop:
            yield t.strftime(outfmt)
            if t.month + self.step > 12:
                next_ = date(t.year + 1, (t.month + self.step) % 12, 1)
            else:
                next_ = date(t.year, t.month + self.step, 1)
            t = next_

    def weeks(self, outfmt='%Y%W'):
        t = self.start
        while t <= self.stop:
            yield t.strftime(outfmt)
            next_ = t + timedelta(days=7)
            t = next_

    def days(self, outfmt='%Y%m%d'):
        t = self.start
        while t <= self.stop:
            yield t.strftime(outfmt)
            next_ = t + timedelta(days=self.step)
            t = next_
