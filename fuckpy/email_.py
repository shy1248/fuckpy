#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: yushuibo
@Copyright (c) 2018 yushuibo. All rights reserved.
@Licence: GPL-2
@Email: hengchen2005@gmail.com
@Create: email.py
@Last Modified: 2018/4/1 20:57
@Desc:  一个简单的Email客户端，暂不支持附件发送
"""

import smtplib
import email.mime.multipart
import email.mime.text


class Email(object):
    """
    简单Eamil类封装

    参数：
        server -- smtp服务器地址
        port -- smtp服务器端口
        username -- smtp服务器的用户名，即邮箱账号
        passwd -- smtp服务器的密码，即邮箱密码
        mailto -- 收件人列表
    """

    server = None
    port = None
    username = None
    passwd = None
    mailto = None

    def __init__(self, subject, content):
        """
        Email类的构造函数。

        参数：
            subject -- 邮件主题
            content -- 邮件正文
        """

        self.subject = subject
        self.content = content

    # 邮箱服务器设置
    @classmethod
    def setup(cls, server, port, username, passwd, mailto):
        """
        邮箱服务器设置，设置好了才能通过发送邮件。

        参数：
            server -- smtp服务器地址
            port -- smtp服务器端口
            username -- smtp服务器用户名，即邮箱账号
            passwd -- smtp服务器密码，即邮箱密码
            mailto -- 收件人列表
        """

        cls.server = server
        cls.port = port
        cls.username = username
        cls.passwd = passwd
        cls.mailto = mailto

    # 发送邮件
    def send(self):
        """通过设置好的邮件服务器发送邮件"""
        msg = email.mime.multipart.MIMEMultipart()
        msg['from'] = Email.username
        msg['to'] = ','.join(Email.mailto)
        msg['subject'] = self.subject
        content = self.content
        txt = email.mime.text.MIMEText(content)
        msg.attach(txt)
        smtp = smtplib.SMTP_SSL(Email.server, Email.port)
        smtp.ehlo()
        smtp.login(Email.username, Email.passwd)
        smtp.sendmail(Email.username, self.mailto, str(msg))
        smtp.close()


if __name__ == '__main__':
    server = 'smtp.163.com'
    port = 465
    username = 'yushuibo@163.com'
    passwd = 'xxxxxxxx'
    mailto = ['a@163.com', 'b@163.com', 'c@163.com']

    Email.setup(server, port, username, passwd, mailto)
    email_ = Email('Email test!', 'This is a test message!')
    email_.send()
