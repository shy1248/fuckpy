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
    A Simple Client of Mysql.
"""

import MySQLdb
from sshtunnel import SSHTunnelForwarder


class SimpleMysqlClient(object):
    """
    The class of mysql.

    args:
        host: mysql server ip address
        port: the port of mysql listen
        user: user name of mysql
        passwd: password of mysql
        db: dest database
        charset: charset of mysql connector, default is utf-8
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
        conn = MySQLdb.connect(self.host, self.port, self.user, self.passwd,
                               self.db, self.charset)
        return conn

    @property
    def cursor(self):
        corsur = self.connector.cursor()
        return corsur

    def fetchone(self, sql, *args, **kwargs):
        c = self.cursor
        c.execute(sql, *args, **kwargs)
        return c.fetchone()

    def fetchmany(self, size, sql, *args, **kwargs):
        c = self.cursor
        c.execute(sql, *args, **kwargs)
        return c.fetchmany(size=size)

    def fetchall(self, sql, *args, **kwargs):
        c = self.cursor
        c.execute(sql, *args, **kwargs)
        return c.fetchall()

    def close(self):
        self.connector.close()
