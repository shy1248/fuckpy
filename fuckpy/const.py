#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Date    : 2018-11-03 14:51:40
# @Author  : shy (hengchen2005@gmail.com)
# @Desc    : A constant implemention
# @Version : v1.0
# @Licence: GPLv3
# @Copyright (c) 2018-2022 shy. All rights reserved.


import sys


class _Constant(object):
    '''A constant implementation'''
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError("Can't rebind constant '%s'." % name)
        self.__dict__[name] = value

    def __delattr(self, name):
        if name in self.__dict__:
            raise self.ConstError("Can't unbind constant '%s'." % name)
        raise NameError(name)


sys.modules[__name__] = _Constant()


if __name__ == '__main__':
    import const
    const.package_max_size = 10000
