#!/usr/bin/env python
# -*- coding=UTF-8 -*-

'''
@ Author: shy
@ Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@ Version: v1.0
@ Description: -
@ Since: 2020/5/28 17:57
'''

from __future__ import print_function
from __future__ import unicode_literals

import os
import glob
import time

import paramiko

from utils import is_contain_chinese
from simplelogger import SimpleLogger
logger = SimpleLogger()

class SftpClient(object):

    def __init__(self, ip, port, user, passwd, timeout=60):
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = passwd
        self.timeout = timeout

    def login(self):
        self.client = paramiko.Transport((self.ip, self.port))
        self.client.banner_timeout = self.timeout
        try:
            self.client.connect(username=self.user, password=self.passwd)
            self.ftp = paramiko.SFTPClient.from_transport(self.client)
        except Exception:
            raise
        return True

    def close(self):
        try:
            self.client.close()
            logger.info("Quit to ftp server with ip: {}".format(self.ip))
        except Exception as e:
            logger.error('An exception found while closing FTP[{}:{}] connection. Reason:\n{}'.format(
                    self.ip, self.port, e))
            # warnings.warn('An exception found while closing FTP[{}:{}] connection.'.format(
            #    self.ip, self.port))

    def cwd(self, path):
        if isinstance(path, unicode):
            if is_contain_chinese(path):
                path = path.encode('gbk')
            else:
                path = path.encode('utf-8')

        try:
            self.ftp.chdir(path)
        except Exception:
            raise

    def get_file_size(self, filename):
        if isinstance(filename, unicode):
            if is_contain_chinese(filename):
                filename = filename.encode('gbk')
            else:
                filename = filename.encode('utf-8')

        try:
            return self.ftp.stat(filename).st_size
        except Exception:
            raise

    def list_files(self, pattern):
        if isinstance(pattern, unicode):
            if is_contain_chinese(pattern):
                pattern = pattern.encode('gbk')
            else:
                pattern = pattern.encode('utf-8')

        if '/' in pattern:
            d, f = os.path.split(pattern)
        else:
            d, f = ('.', pattern)

        try:
            all_files = self.ftp.listdir(path=d)
            if f:
                return glob.fnmatch.filter(all_files, f)
            else:
                return all_files
        except Exception:
            raise

    def retrfile(self, filename, callback=None):
        if isinstance(filename, unicode):
            if is_contain_chinese(filename):
                filename = filename.encode('gbk')
            else:
                filename = filename.encode('utf-8')

        try:
            fc = ''.join(self.ftp.file(filename, mode='r', bufsize=1024).readlines())
            if callback:
                callback(fc)
            else:
                print(fc)
        except Exception:
            raise

    def waitting_file_completed(self, filename):
        '''if the file size is no changed at one second, we consider the file is not writting now'''
        if isinstance(filename, unicode):
            if is_contain_chinese(filename):
                filename = filename.encode('gbk')
            else:
                filename = filename.encode('utf-8')

        last_size = 0
        while True:
            time.sleep(2)
            current_size = self.get_file_size(filename)

            if current_size == last_size:
                break
            else:
                last_size = current_size


if __name__ == "__main__":

    def split(lines):
        print(lines.split('\n'))

    # ip = '192.168.100.8'
    # port = 21
    # user = 'shy'
    # passwd = '123456'
    ip = 'demos01'
    port = 22
    user = 'shy'
    passwd = '123456'

    client = SftpClient(ip, port, user, passwd)
    client.login()
    client.cwd('tmp/hadoop')
    files = client.list_files('dev-support/bin/')
    print(files)
    #   print(client.get_file_size('pom.xml'))
    # print(client.get_file_size(files[0]))
    #   client.retrfile('pom.xml', split)
    # client.waitting_file_completed('test.dat')
    # print('File write completed.')
    client.close()

