#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: yushuibo
@Copyright (c) 2018 yushuibo. All rights reserved.
@Licence: GPL-2
@Email: hengchen2005@gmail.com
@Create: ping.py
@Last Modified: 2018/4/1 20:57
@Desc: --
"""

import os
import struct
import array
import time
import socket

from .utils import is_ip


class Ping(object):
    """
    python实现icmp协议的ping工具实现。

    参数：
        timeout    -- Socket超时，默认3秒
        IPv6       -- 是否是IPv6，默认为False
    """

    def __init__(self, timeout=3, ipv6=False):
        self.timeout = timeout
        self.ipv6 = ipv6

        # 用于ICMP报文的负荷字节（8bit）
        self.__data = struct.pack('d', time.time())
        # 构造ICMP报文的ID字段，无实际意义
        self.__id = os.getpid()

    # 属性装饰器
    @property
    def __socket(self):
        """创建ICMP Socket，并返回ICMP类型的Socket"""
        if not self.ipv6:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                 socket.getprotobyname("icmp"))
        else:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_RAW,
                                 socket.getprotobyname("ipv6-icmp"))
        sock.settimeout(self.timeout)
        return sock

    @property
    def __packet(self):
        """构造ICMP报文, 并返回带校验和的数据报文"""
        if not self.ipv6:
            # TYPE、CODE、CHKSUM、ID、SEQ
            header = struct.pack('bbHHh', 8, 0, 0, self.__id, 0)
        else:
            header = struct.pack('BbHHh', 128, 0, 0, self.__id, 0)

        # 不带校验和的数据包
        packet = header + self.__data
        # 生成校验和
        checksum = in_checksum(packet)

        if not self.ipv6:
            header = struct.pack('bbHHh', 8, 0, checksum, self.__id, 0)
        else:
            header = struct.pack('BbHHh', 128, 0, checksum, self.__id, 0)

        return header + self.__data

    def send(self, ip):
        """
        利用ICMP报文探测网络主机存活。

        参数:
            ip -- 要探测的主机地址
        返回：
            主机存活时返回收到的数据，否则返回None
        """

        if is_ip(ip):
            sock = self.__socket
            try:
                sock.sendto(self.__packet, (ip, 0))
                resp = sock.recvfrom(1024)
            except socket.timeout:
                resp = None
            return resp


def in_checksum(packet):
    """
    ICMP 报文效验和计算方法。

    参数：
        packet -- 原始数据包
    返回：
        带校验和的数据包
    """

    if len(packet) & 1:
        packet = packet + '\\0'
    words = array.array('h', packet)
    sum_ = 0
    for word in words:
        sum_ += (word & 0xffff)
    sum_ = (sum_ >> 16) + (sum_ & 0xffff)
    sum_ = sum_ + (sum_ >> 16)
    return (~sum_) & 0xffff


if __name__ == '__main__':
    ping = Ping(6)
    ip = socket.gethostbyname('baidu.com')
    print('ip={}'.format(ip))
    resp = ping.send(ip)
    print(resp)
