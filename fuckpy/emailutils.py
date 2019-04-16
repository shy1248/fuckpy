#!/usr/bin/env python
# -*- coding=UTF-8 -*-
'''
@Author: shy
@Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@Version: v1.0
@Licence: GPLv3
@Description: -
@Since: 2019-02-02 16:43:24
@LastTime: 2019-04-16 15:36:43
'''

import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from simplelogger import SimpleLogger

logger = SimpleLogger(handler=SimpleLogger.BOTH, level=SimpleLogger.D)


class Account(object):
    '''A account of email'''

    def __init__(self, server, port, username, password, name='Robat',
                 ssl=True):
        self.server = server
        self.port = port
        self.username = username
        self.passwd = password
        self.name = name
        self.ssl = ssl

    def login(self):
        '''Login to email server

        Returns:
            [stmp] -- A smtp protocol object
        '''
        try:
            if self.ssl:
                smtp = smtplib.SMTP_SSL(self.server, self.port)
            else:
                smtp = smtplib.SMTP(self.server, self.port)
            smtp.ehlo()
            smtp.login(self.username, self.passwd)
        except Exception, e:
            logger.error(
                'Email client connect to server or login faild. The rease is:\n%s'
                % e)

        return smtp


class Email(object):
    '''An email object'''

    def __init__(self,
                 account,
                 tolist,
                 content,
                 cclist=None,
                 subject=None,
                 attaches=None):
        self.account = account
        self.tolist = tolist
        self.content = content
        self.cclist = cclist
        self.subject = subject
        self.attaches = attaches

    def send(self):
        '''The function of senf email'''

        if isinstance(self.content, unicode):
            content = self.content.encode('utf8')
        else:
            content = self.content

        me = "%s<%s>" % (self.account.name, self.account.username)
        msg = MIMEMultipart()
        puretext = MIMEText(content, 'plain', 'utf-8')

        if self.subject and not isinstance(self.subject, unicode):
            subject = unicode(self.subject, 'utf8')
            msg['Subject'] = subject
        else:
            msg['Subject'] = ''

        msg['From'] = me
        msg['To'] = ";".join(self.tolist)
        msg['Cc'] = '' if not self.cclist else ';'.join(self.cclist)
        msg["Accept-Language"] = "zh-CN"
        msg["Accept-Charset"] = "ISO-8859-1,utf-8"
        msg.attach(puretext)
        recivers = self.tolist.extend(
            self.cclist) if self.cclist else self.tolist

        if self.attaches:
            for attache in self.attaches:
                if not os.path.isfile(attache):
                    logger.warn('Email attachement "%s" dose exist.' % attache)

                filepart = MIMEApplication(open(attache, 'rb').read())
                filepart.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(attache))
                msg.attach(filepart)

        try:
            smtp = self.account.login()
            smtp.sendmail(me, recivers, msg.as_string())
            smtp.close()
        except Exception, e:
            logger.error('Send email failed. The rease is:\n%s' % str(e))


if __name__ == '__main__':
    server = 'smtp.163.com'
    port = 465
    username = 'yyyyy@163.com'
    password = 'xxxxx'
    tolist = ['zzzzz@ebupt.com']

    account = Account(server, port, username, password)
    email_ = Email(
        account,
        tolist,
        'This is a test message!',
        subject='Email test!',
        attaches=['resty.py'])
    email_.send()
