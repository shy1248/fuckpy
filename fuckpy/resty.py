#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: yushuibo
@Copyright (c) 2018 yushuibo. All rights reserved.
@Licence: GPL-2
@Email: hengchen2005@gmail.com
@File: resty.py
@Create: 2018-04-01 16:45:48
@Last Modified: 2018-04-01 16:45:48
@Desc: 一个简单的rest服务实现
"""

import cgi
import weakref
from functools import wraps
from wsgiref.simple_server import make_server

# 定义404返回的html
_notfound_resp = """\
<html>
<title>Page Not Found!</title>
<body>
<p>404, Page Not Found!</p>
</body>
</html>
"""


def notfound_404(environ, start_response):
    """
    默认的404请求的处理函数。

    参数：
        environ --
        封装请求的参数。例如：可以使用environ['params']来获取请求参数的字典
        start_response -- 定义rest服务响应的头部信息

    """

    start_response('404 Not Found', [('content-type', 'text/html')])
    yield _notfound_resp.encode('utf-8')


# Resty的缓存工具类
class CachedRestyManager(object):
    """
    Resty的缓存管理工具类。当使用相同的Dispatcher生成Resty时，都会返回相同的Resty实例。
    """

    def __init__(self):
        self._cache = weakref.WeakKeyDictionary()

    def getinstance(self, name):
        """通过Dispatcher返回一个Resty的实例并将其缓存，当缓存实例已经存在时，直接返回该缓存实例"""
        if dispatcher not in self._cache:
            instance = Resty(name)
            self._cache[name] = instance
        else:
            instance = self._cache[name]
        return instance

    def clear(self):
        """清除Resty的实例缓存"""
        self._cache.clear()


# Resty服务类
class Resty(object):
    """Resty服务类"""
    manager = CachedRestyManager()

    def __init__(self, name):
        self.name = name

    def getinstance(self, name):
        """返回Resty的实例，参考CachedRestyManager.getinstance方法"""
        return Resty.manager.getinstance(name)

    # Resty的http服务
    def listen(self, port):
        """
        启动Resty的http服务。

        参数：
            port -- resty服务监听的端口
        """

        httpd = make_server('', port, PathDispatcher)
        httpd.serve_forever()


# Resty服务的路由分发类
class PathDispatcher(object):
    """请求路径的路由分发类"""

    _pathmap = {}

    def __new__(cls, environ, start_response, *args, **kwargs):
        path = environ['PATH_INFO']
        params = cgi.FieldStorage(environ['wsgi.input'], environ=environ)
        method = environ['REQUEST_METHOD'].lower()
        environ['params'] = {key: params.getvalue(key) for key in params}
        handler = cls._pathmap.get((method, path), notfound_404)
        return handler(environ, start_response)

    @classmethod
    def regist(cls, method, path, func):
        """
        给PathDispatcher绑定响应的处理函数。

        参数：
            method -- 请求方法。如GET，POST等
            path -- 请求的URL路径
            func -- 请求路径对应的处理函数
        """

        cls._pathmap[method.lower(), path] = func
        return func

    @classmethod
    def get(cls, path):
        """
        Resty服务GET请求装饰器。使用方法：
            @PathDispatcher.get('/hello')
            def hello_handler(envrion, start_response):
                pass

        参数：
            path -- GET请求路径
        """

        def decorate(func):
            method = 'GET'
            cls._pathmap[method.lower(), path] = func

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorate

    @classmethod
    def post(cls, path):
        """
        Resty服务POST请求装饰器。使用方法：
            @PathDispatcher.post('/hello')
            def hello_handler(envrion, start_response):
                pass

        参数：
            path -- POST请求路径
        """

        def decorate(func):
            method = 'POST'
            cls._pathmap[method.lower(), path] = func

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorate


if __name__ == '__main__':
    # demo
    @PathDispatcher.get('/hello')
    def default(environ, start_response):
        start_response('200 OK', [('content-type', 'text/html')])
        yield b'Hello, RESTY!'

    #  Dispatcher.regist('GET', '/hello', default)
    resty = Resty('test')
    resty.listen(8080)
