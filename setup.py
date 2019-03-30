#!/usr/bin/env python
# -*- coding=UTF-8 -*-
'''
@Author: shy
@Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@Version: v1.0
@Licence: GPLv3
@Description: -
@Since: 2018-11-03 22:50:33
@LastTime: 2019-03-30 14:29:18
'''

import os
import sys
from distutils.core import setup

_name = 'fuckpy'
_version = '1.4'
_author = 'shy'
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

setup(
    name=_name,
    version=_version,
    author=_author,
    author_email=_email,
    url=_url,
    packages=['fuckpy'],
)
