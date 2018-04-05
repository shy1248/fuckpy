#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: yushuibo
@Copyright (c) 2018 yushuibo. All rights reserved.
@Licence: GPL-2
@Email: hengchen2005@gmail.com
@File: mysql.py
@Create: 2018-03-27 23:31:42
@Last Modified: 2018-03-27 23:31:42
@Desc:
    一个简单的mysql客户端封装
"""

import MySQLdb

#  from sshtunnel import SSHTunnelForwarder


class SimpleMysqlClient(object):
    """
    MySql客户端的简单封装。

    参数：
        host -- MySql服务器的IP地址
        port -- MySql服务监听的端口
        user -- MySql的用户名
        passwd -- MySql的密码
        db -- 目标数据库
        charset -- MySql连接字符集，默认为utf-8
    """

    def __init__(self, host, port, user, passwd, db, charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.connector()
        self.cursor()

    @property
    def connector(self):
        """返回mysql的连接对象"""
        conn = MySQLdb.connect(self.host, self.port, self.user, self.passwd,
                               self.db, self.charset)
        return conn

    @property
    def cursor(self):
        """返回mysql的游标对象"""
        corsur = self.connector.cursor()
        return corsur

    def fetchone(self, sql, *args, **kwargs):
        """返回SQL Select语句结果集的第一条记录"""
        c = self.cursor
        c.execute(sql, *args, **kwargs)
        return c.fetchone()

    def fetchmany(self, size, sql, *args, **kwargs):
        """返回SQL Select语句结果的多条记录"""
        c = self.cursor
        c.execute(sql, *args, **kwargs)
        return c.fetchmany(size=size)

    def fetchall(self, sql, *args, **kwargs):
        """返回SQL Select语句结果集的所有记录"""
        c = self.cursor
        c.execute(sql, *args, **kwargs)
        return c.fetchall()

    def close(self):
        """关闭mysql的连接"""
        self.connector.close()
