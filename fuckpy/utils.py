#!/usr/bin/env python
# -*- coding=UTF-8 -*-
'''
@Author: shy
@Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@Version: v1.0
@Licence: GPLv3
@Description: -
@Since: 2018-12-21 18:06:56
@ LastTime: 2020-07-29 14:57:39
'''

import re
import os
import json
import tarfile
from functools import wraps

SUFFIXES = {
    1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
    1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
}


def creattmpfile(file_, size):
    '''Create a temprary file for a specil size

    Arguments:
        file_ {str} -- The path of the temprary file. eg: '/tmp/test.tmp'
        size {int} -- The size of the temprary file, the unit is 'byte'
    '''

    with open(file_, 'wb') as f:
        f.seek(size - 1)
        f.write(b'\x00')


def isip(ip):
    '''Decide the specil IP is valid or not

    Arguments:
        ip {str} -- The specil IP address

    Returns:
        bool -- Return 'True' if the specil IP is valid. Otherwise, return 'False'
    '''

    ip = [int(x) for x in ip.split('.') if x.isdigit()]
    if len(ip) == 4:
        if (0 < ip[0] < 223 and ip[0] != 127 and ip[1] < 256 and ip[2] < 256 and 0 < ip[3] < 255):
            return True
    return False


def mkips(start, end, ipv6=False):
    '''Make a pool for IP addresses

    Arguments:
        start {str} -- The start IP address of the pool
        end {str} -- The stop IP address of the pool

    Keyword Arguments:
        ipv6 {bool} -- IPv6 is support or not (default: {False})

    Returns:
        [set] -- The set of the IP pool
    '''

    import IPy
    ip_ver = 6 if ipv6 else 4

    def int_ip(ip):
        return IPy.IP(ip).int()

    ip_pool = {IPy.intToIp(ip, ip_ver) for ip in range(int_ip(start), int_ip(end) + 1)}
    return {ip for ip in ip_pool if isip(ip)}


def intar(tarname, spath, mode='w:gz'):
    '''Create an achive file using tar

    Arguments:
        tarname {str} -- The achive's name
        spath {str} -- The path which will be add to achive

    Keyword Arguments:
        mode {str} -- compress format，gzip(w:gz) or bzip(w:bz2) (default: {'w：gz'})
    '''

    tar = tarfile.open(tarname, mode)
    tar.add(spath, arcname=os.path.basename(spath))
    tar.close


def untar(tarname, dpath, mode='r:gz'):
    '''Extract an achive using tar

    Arguments:
        tarname {str} -- The achive which will be extract
        dpath {str} -- The output path

    Keyword Arguments:
        mode {str} -- compress format，gzip(w:gz) or bzip(w:bz2) (default: {'r:gz'})
    '''

    tar = tarfile.open(tarname, mode)
    tar.extractall(dpath)
    tar.close


def jsondumps(d, file, indent=0):
    '''Dump the specil dict to a json file

    Arguments:
        d {dict} -- The dict which will be dump
        file {str} -- The path of the json file

    Keyword Arguments:
        indent {int} -- indent width (default: {0})
    '''

    json_str = json.dumps(d, indent=indent)
    with open(file, 'wb') as f:
        f.write(json_str)


def jsonloads(file):
    '''Load the specil josn file to a dict

    Arguments:
        file {str} -- The json file path will be load

    Returns:
        [dict] -- The dict object for the json file
    '''

    with open(file, 'rb') as f:
        json_str = f.read()

    return json.loads(json_str)


def approximate_size(size, a_kilobyte_is_1024_bytes=True):
    '''Convert a file size to human-readable form.

    Keyword arguments:
        size {int} -- file size in bytes
        a_kilobyte_is_1024_bytes -- if True (default), use multiples of 1024; if False, use multiples of 1000
    Returns:
        string
    '''
    if size < 0:
        raise ValueError('Number must be non-negative.')

    multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
    for suffix in SUFFIXES[multiple]:
        size /= multiple
        if size < multiple:
            return '{0:.1f} {1}'.format(size, suffix)

    raise ValueError('Number is too large.')


def is_contain_chinese(dest):
    '''check a string contains a chinese or not

    Arguments:
        dest {str} -- the destination string will be check
    '''
    for ch in dest:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def is_all_chinese(dest, whitespace=True):
    '''check a string is all chinese or not

    Arguments:
        dest {str} -- the destination string will be check

    Keyword Arguments:
        whitespace {bool} -- if take with whitespace charators or not (default: {True})
    '''

    if not whitespace:
        dest = re.sub(r'\s*', '', dest)
    for ch in dest:
        if ch < u'\u4e00' or ch > u'\u9fff':
            return False

    return True


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


def is_contain_chinese(dest):
    '''check a string contains a chinese or not

    Arguments:
        dest {str} -- the destination string will be check
    '''
    for ch in dest:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def chinese_counter(dest):
    '''the counter of chinese char in dest

    Arguments:
        dest {str} -- the destination string will be check
    '''
    counter = 0
    for ch in dest:
        if '\u4e00' <= ch <= '\u9fff':
            counter += 1
    return counter


def is_all_chinese(dest, whitespace=True):
    '''check a string is all chinese or not

    Arguments:
        dest {str} -- the destination string will be check

    Keyword Arguments:
        whitespace {bool} -- if take with whitespace charators or not (default: {True})
    '''

    if not whitespace:
        dest = re.sub(r'\s*', '', dest)
    for ch in dest:
        if ch < '\u4e00' or ch > '\u9fff':
            return False

    return True


def get_mom_day(date, fmt='%Y%m%d'):
    if isinstance(date, str):
        try:
            date = datetime.datetime.strptime(date, fmt)
        except Exception as e:
            raise e

    year = date.year
    month = date.month
    day = date.day

    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    if day == 31 and month in (4, 6, 9, 11):
        day = 30
    if day > 28 and month == 2:
        day = 29 if year % 4 == 0 else 28

    dest_day = datetime.datetime.strftime(date.replace(year=year, month=month, day=day), fmt)

    return dest_day


if __name__ == "__main__":
    # s1 = '??'
    # s2 = 'hello'
    # s3 = 'hello, ??'
    # print(is_contain_chinese(s1))
    # print(is_contain_chinese(s2))
    # print(is_contain_chinese(s3))
    day1 = '20200108'
    day2 = '20200329'
    day3 = '20191130'
    day4 = '20191025'
    print(get_mom_day(day1, fmt='%Y%m%d'))
    print(get_mom_day(day2, fmt='%Y%m%d'))
    print(get_mom_day(day3, fmt='%Y%m%d'))
    print(get_mom_day(day4, fmt='%Y%m%d'))
