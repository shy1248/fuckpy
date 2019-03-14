#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Date    : 2018-10-27 03:03:07
# @Author  : shy (hengchen2005@gmail.com)
# @Desc    : -
# @Version : v1.0
# @Licence: GPLv3
# @Copyright (c) 2018-2022 shy. All rights reserved.


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

setup(name=_name,
      version=_version,
      author=_author,
      author_email=_email,
      url=_url,
      packages=['fuckpy'],)
