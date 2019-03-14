#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Date    : 2018-10-26 17:43:43
# @Author  : shy (hengchen2005@gmail.com)
# @Desc    : -
# @Version : v1.0
# @Licence: GPLv3
# @Copyright (c) 2018-2022 shy. All rights reserved.

import itchat
from itchat.content import *


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])


@itchat.msg_register(TEXT, isGroupChat=True)
def groupchat_reply(msg):
    if msg['isAt']:
        itchat.send(u'@%s\u2005I received: %s' %
                    (msg['ActualNickName'], msg['Content']), msg['FromUserName'])


itchat.auto_login(True)
itchat.run()
