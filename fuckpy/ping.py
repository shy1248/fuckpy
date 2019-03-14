#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Date    : 2018-10-26 17:43:43
# @Author  : shy (hengchen2005@gmail.com)
# @Desc    : -
# @Version : v1.0
# @Licence: GPLv3
# @Copyright (c) 2018-2022 shy. All rights reserved.

import os
import struct
import array
import time
import socket

from .utils import isip


class Ping(object):
    '''A icmp protocol implemention'''

    def __init__(self, timeout=3, ipv6=False):
        self.timeout = timeout
        self.ipv6 = ipv6

        # The icmp package length（8bit）
        self.__data = struct.pack('d', time.time())
        # The id of the icmp package
        self.__id = os.getpid()

    @property
    def __socket(self):
        '''Get icmp socket

        Returns:
            [socket] -- The icmp socket
        '''
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
        '''Construct icmp package

        Returns:
            [pack] -- The package which will be send
        '''
        if not self.ipv6:
            # TYPE、CODE、CHKSUM、ID、SEQ
            header = struct.pack('bbHHh', 8, 0, 0, self.__id, 0)
        else:
            header = struct.pack('BbHHh', 128, 0, 0, self.__id, 0)

        # The package without checksum
        packet = header + self.__data
        # The package with checksum
        checksum = in_checksum(packet)

        if not self.ipv6:
            header = struct.pack('bbHHh', 8, 0, checksum, self.__id, 0)
        else:
            header = struct.pack('BbHHh', 128, 0, checksum, self.__id, 0)

        return header + self.__data

    def ping(self, ip):
        '''Send package to remote host for a ping test

        Arguments:
            ip {str} -- The IP address of remote host

        Returns:
            {bytes or None} -- The remote host respose
        '''

        if isip(ip):
            sock = self.__socket
            try:
                sock.sendto(self.__packet, (ip, 0))
                resp = sock.recvfrom(1024)
            except socket.timeout:
                resp = None
            return resp
        else:
            raise Exception('Invalid ip address: "%s"' % ip)


def in_checksum(packet):
    '''ICMP package's checksum

    Arguments:
        packet {byte} -- The package without checksum
    '''

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
    resp = ping.ping(ip)
    print(resp)
