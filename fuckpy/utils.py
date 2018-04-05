#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: yushuibo
@Copyright (c) 2018 yushuibo. All rights reserved.
@Licence: GPL-2
@Email: hengchen2005@gmail.com
@File: utils.py
@Create: 2018-04-04 21:33:10
@Last Modified: 2018-04-04 21:33:10
@Desc: 包含一些常用的函数
"""


def attach_file(file_, size):
    """
    创建一个文件并将其内容扩充至固定大小。

    参数：
        file_ -- 要创建的文件，例如/tmp/test.tmp
        size -- 文件的大小，单位为字节
    """

    with open(file_, 'wb') as f:
        f.seek(size - 1)
        f.write(b'\x00')


def is_ip(ip):
    """
    判断IP是否是一个合法的单播地址。

    参数：
        ip -- 要检测的ip地址
    返回：
        当ip地址为有效的单播地址时返回True，否则返回False
    """

    ip = [int(x) for x in ip.split('.') if x.isdigit()]
    if len(ip) == 4:
        if (0 < ip[0] < 223 and ip[0] != 127 and ip[1] < 256 and ip[2] < 256
                and 0 < ip[3] < 255):
            return True
    return False


def make_ip_pool(start, end, ipv6=False):
    """
    生产IP地址池。

    参数：
        start -- 开始的ip地址
        end -- 结束的ip地址
        ipv6 -- 是否为ipv6，默认为False
    返回：
    ip地址的集合
    """

    import IPy
    ip_ver = 6 if ipv6 else 4

    def int_ip(ip):
        return IPy.IP(ip).int()

    ip_pool = {
        IPy.intToIp(ip, ip_ver)
        for ip in range(int_ip(start),
                        int_ip(end) + 1)
    }
    return {ip for ip in ip_pool if is_ip(ip)}
