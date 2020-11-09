#!/usr/bin/env python
# -*- coding=UTF-8 -*-
'''
@ Since: 2019-08-03 22:58:05
@ Author: shy
@ Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@ Version: v1.0
@ Description: A email send util
@ LastTime: 2019-08-15 16:06:20
'''

import os
import smtplib
import warnings
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class Account(object):
    '''A account of email'''

    def __init__(self, server, port, username, password, name='Robat', ssl=True):
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
        except Exception:
            raise

        return smtp


class Email(object):
    '''An email object'''

    def __init__(self, account, tolist, content, cclist=None, subject=None, attaches=None):
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
        recivers = self.tolist + self.cclist

        if self.attaches:
            for attache in self.attaches:
                if not os.path.isfile(attache):
                    warnings.warn('Email attachement "%s" dose exist.' % attache)
                    continue

                filepart = MIMEApplication(open(attache, 'rb').read())
                filepart.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attache))
                msg.attach(filepart)

        try:
            smtp = self.account.login()
            smtp.sendmail(me, recivers, msg.as_string())
            smtp.close()
        except Exception:
            raise


if __name__ == '__main__':
    server = 'smtp.163.com'
    port = 465
    username = 'yyyyy@163.com'
    password = 'xxxxx'
    tolist = ['zzzzz@ebupt.com']

    account = Account(server, port, username, password)
    mail = Email(account, tolist, 'This is a test message!', subject='Email test!', attaches=['resty.py'])
    mail.send()
