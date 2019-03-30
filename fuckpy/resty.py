#!/usr/bin/env python
# -*- coding=UTF-8 -*-
'''
@Author: shy
@Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@Version: v1.0
@Licence: GPLv3
@Description: -
@Since: 2018-11-16 11:01:28
@LastTime: 2019-03-30 14:27:32
'''

import cgi
import weakref
from functools import wraps
from wsgiref.simple_server import make_server

# Define 404 page
_notfound_resp = """\
<html>
<title>Page Not Found!</title>
<body>
<p>404, Page Not Found!</p>
</body>
</html>
"""


def notfound_404(environ, start_response):
    '''The 404 page handler

    Arguments:
        environ {dict} -- The dict contains request parameters
        start_response -- The response of header

    Yields:
        [str] -- The response body
    '''

    start_response('404 Not Found', [('content-type', 'text/html')])
    yield _notfound_resp.encode('utf-8')


class CachedRestyManager(object):
    '''A cache for instance of Resty'''

    def __init__(self):
        self._cache = weakref.WeakKeyDictionary()

    def getinstance(self, name):
        '''Return the instance of Resty

         Arguments:
            name {str} -- The key of the Resty's instance

        Returns:
            [Resty] -- The instance of Resty
        '''

        if name not in self._cache.keys():
            instance = Resty(name)
            self._cache[name] = instance
        else:
            instance = self._cache[name]
        return instance

    def clear(self):
        '''Clean the cache of instance'''

        self._cache.clear()


class Resty(object):
    manager = CachedRestyManager()

    def __init__(self, name):
        self.name = name

    def getinstance(self, name):
        '''Return a instance of Resty with the specil name'''

        return Resty.manager.getinstance(name)

    def listen(self, host, port):
        '''The HTTP server

        Arguments:
            port {int} -- The HTTP server listen port
        '''

        httpd = make_server(host, port, PathDispatcher)
        httpd.serve_forever()


class PathDispatcher(object):
    '''The route dispatcher of request'''

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
        '''Bind a handler for a request path with specil request method

        Arguments:
            method {str} -- The method of request. Such as 'GET', 'POST' and so on
            path {str} -- The path of request
            func {str} -- The name of handler function

        Returns:
            [func] -- The function of hanfler
        '''

        cls._pathmap[method.lower(), path] = func
        return func

    @classmethod
    def get(cls, path):
        '''The decorator of GET method

        usage:
            @PathDispatcher.get('/hello')
            def hello_handler(envrion, start_response):
                pass

        Decorators:
            wraps

        Arguments:
            path {str} -- The path of request

        Returns:
            [func] -- The function of handler
        '''

        def decorate(func):
            method = 'GET'
            cls._pathmap[method.lower(), path] = func

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func

            return wrapper

        return decorate

    @classmethod
    def post(cls, path):
        '''The decorator of POST method

        usage:
            @PathDispatcher.post('/hello')
            def hello_handler(envrion, start_response):
                pass

        Decorators:
            wraps

        Arguments:
            path {str} -- The path of request

        Returns:
            [func] -- The function of handler
        '''

        def decorate(func):
            method = 'POST'
            cls._pathmap[method.lower(), path] = func

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func

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
    resty.listen('localhost', 8080)
