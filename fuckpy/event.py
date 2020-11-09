#!/usr/bin/env python
# -*- coding=UTF-8 -*-
'''
@ Since: 2019-07-12 15:00:58
@ Author: shy
@ Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@ Version: v1.0
@ Description: -
@ LastTime: 2019-07-15 15:01:59
'''


import Queue
from Queue import Empty
from threading import Thread

from simplelogger import SimpleLogger

logger = SimpleLogger(handler=SimpleLogger.BOTH)


class EventManager(object):

    def __init__(self):
        """initilize event manager"""
        self.__event_queue = Queue.Queue()
        self.__actived = False
        self.__event_loop_thread = Thread(target=self.event_loop)
        self.__handlers = {}

    def event_loop(self):
        while self.__actived:
            try:
                event = self.__event_queue.get(block=True, timeout=1)
                self.__process(event)
            except Empty:
                pass

    def __process(self, event):
        if event.__type in self.__handlers:
            for handler in self.__handlers.get(event.__type):
                handler(event)
        else:
            logger.warn("Event[{}] no handlers, skipped process!")

    def bind_listener(self, event_type, handler):
        if not isinstance(handler, callable):
            raise ValueError('Parameter "handler" except a callable, but <{}> gaven.'.format(type(handler)))

        if event_type not in self.__handlers:
            self.__handlers[event_type] = []
        if handler not in self.__handlers.get(event_type):
            self.__handlers.get(event_type).append(handler)

    def unbind_listener(self, event_type, handler):
        if event_type in self.__handlers and handler in self.__handlers.get(event_type):
            self.__handlers.get(event_type).remove(handler)

        if not self.__handlers.get(event_type):
            self.__handlers.remove(event_type)

    def emit(self, event):
        pass

    def start(self):
        pass

    def stop(self):
        pass
