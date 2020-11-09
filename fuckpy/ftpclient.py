#!/usr/bin/env python
# -*- coding=UTF-8 -*-
'''
@ Since: 2019-07-30 16:18:29
@ Author: shy
@ Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@ Version: v1.0
@ Description: -
@ LastTime: 2019-08-12 14:48:17
'''

from __future__ import print_function
from __future__ import unicode_literals

import os
import time
import warnings
from ftplib import FTP

from simplelogger import SimpleLogger

logger = SimpleLogger(handler=SimpleLogger.BOTH, level=SimpleLogger.D)


class FtpClient(object):

    def __init__(self, ip, port, user, passwd, timeout=10):
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = passwd

    def login(self):
        self.ftp = FTP()
        try:
            self.ftp.connect(self.ip, self.port)
            self.ftp.login(self.user, self.passwd)
        except Exception:
            raise
        return True

    def set_debug(self):
        self.ftp.set_debuglevel(1)

    def set_pasv(self, pasv=False):
        self.ftp.set_pasv(pasv)

    def close(self):
        try:
            self.ftp.quit()
        except Exception:
            warnings.warn('An exception found while closing FTP[{}:{}] connection.'.format(
                self.ip, self.port))

    def cwd(self, path):
        try:
            self.ftp.cwd(path)
        except Exception:
            raise

    def get_file_size(self, filename):
        try:
            return self.ftp.size(filename)
        except Exception:
            raise

    def list_files(self, pattern):
        try:
            return self.ftp.nlst(pattern)
            # return self.ftp.retrlines('LIST {}'.format(pattern))
        except Exception:
            raise

    def retrfile(self, filename, callback):
        try:
            # tmp = '/tmp/{}'.format(filename)
            # fp = open(tmp, 'w')
            return self.ftp.retrlines('RETR {}'.format(filename), callback)
            # self.ftp.retrbinary('RETR {}'.format(tmp), fp, 1024)
        except Exception:
            raise

    def download(self, r_path, l_path):
        if (os.path.exists(l_path)):
            os.remove(l_path)
        fp = open(l_path, 'w')
        self.ftp.retrbinary('RETR {}'.format(r_path), fp.write)
        fp.close()


if __name__ == "__main__":

    def split(lines):
        print(lines.split('\n'))

    ip = '10.25.150.193'
    port = 21
    user = 'migulog'
    passwd = 'migulog@123'
    target = '20190810.tar.gz'

    client = FtpClient(ip, port, user, passwd)
    while True:
        try:
            logger.info('Try to login ftp: {}:{} with {} / {}'.format(ip, port, user, passwd))
            client.login()
            client.set_debug()
            logger.info('Ftp login success.')
            # client.list_files('*')
            client.set_pasv(True)
            logger.info('Starting download file: {} using pasv mode.'.format(target))
            client.download(target, os.path.join(os.getcwd(), target))
            logger.info('Downloading file {} success using pasv mode.'.format(target))

            client.set_pasv(False)
            logger.info('Starting download file: {} using port mode.'.format(target))
            client.download(target, os.path.join(os.getcwd(), target))
            logger.info('Downloading file {} success using port mode.'.format(target))
        except Exception, e:
            logger.error('Error occourded: {}'.format(e))
        finally:
            client.close()

        time.sleep(300)
