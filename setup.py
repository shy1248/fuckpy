#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: yushuibo
@Copyright (c) 2018 yushuibo. All rights reserved.
@Licence: GPL-2
@Email: hengchen2005@gmail.com
@File: setup.py
@Create: 2018-04-03 23:49:42
@Last Modified: 2018-04-03 23:49:42
@Desc: --
"""


import os
import sys
from distutils.core import setup


_name = 'fuckpy'
_version = '1.1'
_author = 'yushuibo'
_email = 'hengchen2005@gmail.com'
_url = 'https://github.com/yushuibo/fuckpy'

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a {} -m 'veriosn {}'".format(_version, _version))
    os.system("git push --tags")
    sys.exit()

setup(name=_name,
      version=_version,
      author=_author,
      author_email=_email,
      url=_url,
      packages=['fuckpy'],
)
