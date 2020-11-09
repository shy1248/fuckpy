#!/usr/bin/env python
# -*- coding=UTF-8 -*-
'''
@Author: shy
@Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@Version: v1.0
@Licence: GPLv3
@Description: -
@Since: 2019-01-17 15:03:29
@ LastTime: 2020-01-15 09:22:58
'''

import ConfigParser
import abc
import os
import subprocess
import sys

import cx_Oracle
import pymysql
from pyhive import hive

from extends import OrderedSet
from simplelogger import SimpleLogger
from singleton import singleton

HIVE = 0
MYSQL = 1
ORACLE = 3

logger = SimpleLogger(handler=SimpleLogger.BOTH, level=SimpleLogger.D)


def get_client_by_conf(conf, setction, ctype=HIVE):
    '''Get a instance of database from a configure file

  Arguments:
      conf {str} -- The path of the configure file
      setction {str} -- The section of destination configure

  Returns:
      [DatabaseClient] -- The instance of database client
  '''

    config = ConfigParser.ConfigParser()
    config.read(conf)
    host = config.get(setction, 'host')
    port = config.get(setction, 'port')
    user = config.get(setction, 'username')
    passwd = config.get(setction, 'password')
    db = config.get(setction, 'database')

    return get_client(host, port, user, passwd, db, ctype=ctype)


def get_client(host, port, user, passwd, db, ctype=HIVE):
    '''Get a instance of a database with the specil client type

  Arguments:
      host {str} -- The host of destination database
      port {str} -- The port of destination database
      user {str} -- The username of destination database
      passwd {str} -- The password of destination database
      db {str} -- The destination database name

  Keyword Arguments:
      ctype {int} -- The type of client (default: {HIVE})

  Returns:
      [DatabaseClient] -- The instance of database client

  Raises:
      TypeError -- When the client type is invalid
  '''

    if ctype == HIVE:
        return HiveClient(host, port, user, passwd, db)
    elif ctype == MYSQL:
        return MySQLClient(host, port, user, passwd, db)
    elif ctype == ORACLE:
        return OracleClient(host, port, user, passwd, db)
    else:
        raise TypeError("A database client type must be one of '%s'." % globals())


class DatabaseClient(object):
    '''A database client encapsulation'''
    __metaclass__ = abc.ABCMeta

    def __init__(self, host, port, username, passwd, db):
        '''Constructor function

    Keyword Arguments:
        conf {str} -- configure file (default: {'./config.conf'})
    '''

        self.host = host
        self.port = port
        self.username = username
        self.passwd = passwd
        self.db = db
        self.connection = self.get_connection()

    def fetchone(self, sql):
        '''Execetue SELECT SQL statments, return the first result.

    Arguments:
        sql {str} -- The SQL statment will be executed

    Keyword Arguments:
        conn {Connection} -- The type of database connection (default: {Hive Connection})

    Returns:
        {str} -- The first result of the resultset
    '''
        return self.fetchall([sql])[0]

    def fetchall(self, sql):
        '''Execetue SELECT SQL statments, return the all resultset by dict.

    Arguments:
        sql {str} -- the SQL statment will be executed

    Returns:
        {list} -- The list of resultset
    '''
        return self.mfetchall([sql])[sql]

    def exec_sql(self, sql):
        '''Execute SQL statment, which return none

    Arguments:
        sql {str} -- The sql statment will be executed

    Returns:
        dict -- The dict of resultset
    '''
        return self.mexec_sql([sql])

    def mfetchall(self, sql_list):
        '''Batch execetue SELECT SQL statments, return the all resultset by dict.

    Arguments:
        sql_list {list} -- The SELECT SQL statments will be executed

    Returns:
        {dict} -- The dict of resultset
    '''

        cursor = self.connection.cursor()
        results = {}
        if len(sql_list) != 0:
            for sql in sql_list:
                try:
                    # Only print select statment
                    # if sql.strip().lower().startswith('select'):
                    logger.debug('Execute SQL: %s' % sql)
                    cursor.execute(sql)
                    results[sql] = cursor.fetchall()
                except Exception, e:
                    logger.error('Execute SQL "%s" failed! The rease is:\n%s' % (sql, str(e)))
                    results[sql] = []
                finally:
                    cursor.close()
        else:
            logger.error('The SQL statment is None!')

        return results

    def mexec_sql(self, sql_list):
        '''Batch execute sql, which is none returns.

    Arguments:
        sql_list {list} -- The list of sql statments which will be executed

    '''

        cursor = self.connection.cursor()

        if len(sql_list) != 0:
            for sql in sql_list:
                try:
                    # print non select statment
                    # if not sql.strip().lower().startswith('select'):
                    logger.debug('Execute SQL: %s' % sql)
                    cursor.execute(sql)
                except Exception, e:
                    logger.error('Execute SQL "%s" failed! The rease is:\n%s' % (sql, str(e)))
                finally:
                    self.connection.commit()
                    cursor.close()
        else:
            logger.error('The SQL statments is None!')

    @abc.abstractmethod
    def get_connection(self):
        pass

    def close(self, commit=True):
        '''Close the connection of database client '''

        if self.connection:
            if commit:
                self.connection.commit()
            self.connection.close()


@singleton
class OracleClient(DatabaseClient):

    def get_connection(self):
        '''Get the connection of Oracle database

    Returns:
        The connection object of Oracle database
    '''

        try:
            # conn = cx_Oracle.connect('%s/%s@%s:%s/%s' % (self.username, self.passwd, self.host, self.port, self.db))
            # conn = cx_Oracle.connect(self.username, self.passwd, self.db)
            tns = cx_Oracle.makedsn(self.host, self.port, self.db)
            conn = cx_Oracle.connect(self.username, self.passwd, tns)
            logger.info("Connect to Oracle database successed!")
            return conn
        except Exception, e:
            logger.error('Connect to Oracle database failed. The rease is:\n%s' % str(e))
            sys.exit(0)


@singleton
class MySQLClient(DatabaseClient):

    def get_connection(self):
        '''Get the connection of MySQL database

    Returns:
        The connection object of MySQL
    '''

        try:
            conn = pymysql.connect(
                host=self.host,
                port=int(self.port),
                user=self.username,
                passwd=self.passwd,
                db=self.db,
                charset='utf8')
            logger.info('Connect to MySQL database successed!')
            return conn
        except Exception, e:
            logger.error('Connect to MySQL database failed. The rease is:\n%s' % str(e))
            sys.exit(0)


@singleton
class HiveClient(DatabaseClient):

    def get_connection(self):
        '''Get the connection of Beeline or Hive command line

    Returns:
        The connection object of Beeline or Hive command line
    '''

        try:
            conn = hive.connect(host=self.host, port=self.port, username=self.username, database=self.db)
            logger.info('Connect to Hive database successed!')
            return conn
        except Exception, e:
            logger.error('Connect to Hive databse failed. The rease is:\n%s' % str(e))
            logger.info('Try to using HiveCli...')
            if subprocess.call(
                    'which hive --skip-alias', shell=True, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE) == 1:
                logger.error(
                    'Command "hive" not found, please make sure hive has been installed and add to system path.'
                )
                sys.exit(0)
            else:
                logger.info('Using HiveCli instead HiveServer2...')

    def cli_exec(self, sql):
        sh = '$(which --skip-alias hive) -S -e "use %s;%s;"' % (self.db, sql)
        p = subprocess.Popen(sh, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        # p.wait()
        if not stdout:
            logger.error('Execute SQL %s failed.' % sql)
        else:
            logger.debug('Execute SQL %s success.' % sql)

        return [line.split() for line in stdout.split('\n') if line.strip()]

    def cli_exec_no_resp(self, sql):
        '''Execute SQL stanment with no response

    Arguments:
        sql {str} -- The SQL statment will be executed
    '''
        sh = '$(which --skip-alias hive) -S -e "use %s;%s;"' % (self.db, sql)
        p = subprocess.Popen(sh, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()

    def cli_mexec(self, sql_list):
        '''Multi execute sql using hive cammand line interface, none returned

    Arguments:
        sql_list {list} -- The list of SQL statments which will be excuted
    '''
        if len(sql_list) > 0:
            for sql in sql_list:
                self.cli_sql(sql)
        else:
            logger.warn('The list of SQL statments is empty.')

    def cli_fetchone(self, sql):
        '''Execute sql using hive cammand line interface and retun the first one of result

    Arguments:
        sql {str} -- The SQL statment which will be execute

    Returns:
        [list] -- The list for the first one of result
    '''
        return self.cli_sql(sql)[0]

    def cli_fetchall(self, sql):
        '''Execute sql using hive cammand line interface and retun the resultset

    Arguments:
        sql {str} -- The SQL statment which will be execute

    Returns:
        [list] -- The list of resultset
    '''
        return self.cli_sql(sql)

    def cli_mfetchall(self, sql_list):
        '''Multi execute sql using hive cammand line interface, has returned

    Arguments:
        sql_list {list} -- The list of SQL statments which will be excuted

    Yields:
        [tuple] -- A sql and it's resultset
    '''
        if len(sql_list) > 0:
            for sql in sql_list:
                yield sql, self.cli_sql(sql)
        else:
            logger.warn('The list of SQL statments is empty.')

    def repair_table(self, tname):
        '''Repair hive table

    Arguments:
        tname {str} -- the table name which will be repaired
    '''

        sql = 'msck repair table %s' % tname
        if self.connection:
            self.exec_sql([sql])
        else:
            self.cli_exec_no_resp(sql)

    def create_partition(self, tname, pv):
        '''Add a partition to hive table.

    Arguments:
        tname {str} -- the name of hive table
        pv {str} -- the value of partition value

    Keyword Arguments:
        pk {str} -- the partition key (default: {'deal_day'})
    '''

        sql = 'alter table %s add if not  exists partition ("%s"="%s")' % (tname, pv)
        if self.connection:
            self.exec_sql([sql])
        else:
            self.cli_exec_no_resp(sql)

    def get_partitions(self, tname):
        '''Get partitions of hive table

    Arguments:
        tname {str} -- the table name of hive

    Returns:
        list -- the list of partitions
    '''

        sql = 'show partitions %s' % tname
        partitions = []

        rs = self.fetchall(sql) if self.connection else self.cli_exec(sql)

        if not rs:
            return partitions

        for li in rs:
            partitions.append(li[0])

        return partitions

    def get_partition_keys(self, tname):
        '''Get partition keys of hive table

    Arguments:
        tname {str} -- the table name of hive

    Returns:
        OrderedSet -- the partition keys of the table
    '''

        pks = OrderedSet()
        for partition in self.get_partitions(tname):
            if os.sep not in partition:
                pks.add(partition.split('=')[0])
            else:
                for subpartition in partition.split(os.sep):
                    pks.add(subpartition.split('=')[0])

        return pks

    def get_partition_path(self, tname, partition):
        '''Get the real hdfs path of parition. if there is no partition, then return the hdfs path of the table.

    Arguments:
        tname {str} -- the name of the table
        partition {str} -- the special partition of the table

    Returns:
        str -- the hdfs path
    '''

        sql = 'desc formatted %s partition (%s)' % (tname, partition.replace(os.sep, ','))
        rs = self.fetchall(sql) if self.connection else self.cli_exec(sql)

        if not rs:
            return None

        for li in rs:
            if 'Location' in li[0]:
                return li[1]

    def get_table_path(self, tname):
        '''Get a hive table's hdfs path

    Arguments:
        tname {str} -- The table name of hive table

    Returns:
        str -- The hdfs path of the table
    '''

        sql = 'desc formatted %s' % tname
        rs = self.fetchall(sql) if self.connection else self.cli_exec(sql)

        if not rs:
            return None

        for li in rs:
            if 'Location' in li[0]:
                return li[1]
