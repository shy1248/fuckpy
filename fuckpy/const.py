#!/usr/bin/env python
# -*- coding=UTF-8 -*-

'''
@Author: shy
@Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@Version: v1.0
@Licence: GPLv3
@Description: -
@Since: 2019-01-06 11:26:40
@LastTime: 2019-03-26 23:51:56
'''


import sys


class _Constant(object):
    '''A constant implementation'''
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
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
