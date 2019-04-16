#!/usr/bin/env python
# -*- coding=UTF-8 -*-
'''
@Author: shy
@Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@Version: v1.0
@Licence: GPLv3
@Description: -
@Since: 2019-04-07 04:48:56
@LastTime: 2019-04-15 13:49:00
'''

import os
import sys
import time
import Queue
import threading
import tkinter as tk
from abc import ABCMeta
from abc import abstractmethod

import win32api
import win32con
import win32gui_struct
import win32gui

__all__ = ['BaseWinTrayApp', 'TrayMessage']


class TrayMessage(object):

    def __init__(self, app, title, msg):
        self.app = app
        self.title = title
        self.msg = msg

    def __repr__(self):
        return "[App={}, Title={}, Message={}]".format(self.app, self.title,
                                                       self.msg)

    def __str__(self):
        return self.__repr__()


class SystemTray(object):

    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]
    FIRST_ID = 1314

    def __init__(
            self,
            icon,
            hover_text,
            menu_options,
            on_quit=None,
            default_menu_index=None,
            window_class_name=None,
    ):
        self.icon = icon
        self.hover_text = hover_text
        self.on_quit = on_quit

        menu_options = menu_options + (('Exit', None, self.QUIT),)
        self._next_action_id = self.FIRST_ID
        self.menu_actions_by_id = set()
        self.menu_options = self._add_ids_to_menu_options(list(menu_options))
        self.menu_actions_by_id = dict(self.menu_actions_by_id)
        del self._next_action_id

        self.default_menu_index = (default_menu_index or 0)
        self.window_class_name = window_class_name if window_class_name else "SysTrayIconPy"
        message_map = {
            win32gui.RegisterWindowMessage("TaskbarCreated"): self.refresh_icon,
            win32con.WM_DESTROY: self.destroy,
            win32con.WM_COMMAND: self.command,
            win32con.WM_USER + 20: self.notify,
        }

        # registry windown class
        window_class = win32gui.WNDCLASS()
        window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        # bind wndproc
        window_class.lpfnWndProc = message_map
        self.classAtom = win32gui.RegisterClass(window_class)

    def show_icon(self):
        # initlize icon
        hinst = win32gui.GetModuleHandle(None)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(
            self.classAtom, self.window_class_name, style, 0, 0,
            win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        self.notify_id = None
        self.refresh_icon(is_init=True)

        win32gui.PumpMessages()

    def show_menu(self):
        menu = win32gui.CreatePopupMenu()
        self.create_menu(menu, self.menu_options)
        # win32gui.SetMenuDefaultItem(menu, 1000, 0)
        pos = win32gui.GetCursorPos()
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0,
                                self.hwnd, None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

    def destroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)
        if self.on_quit:
            self.on_quit(self)
        os._exit(0)
        sys.exit(0)

    def notify(self, hwnd, msg, wparam, lparam):
        # left button double click event
        if lparam == win32con.WM_LBUTTONDBLCLK:
            # self.execute_menu_option(self.default_menu_index + self.FIRST_ID)
            pass
        # right buttuon click event
        elif lparam == win32con.WM_RBUTTONUP:
            self.show_menu()
        # left button click event
        elif lparam == win32con.WM_LBUTTONUP:
            pass
        return True

    def _add_ids_to_menu_options(self, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in self.SPECIAL_ACTIONS:
                self.menu_actions_by_id.add((self._next_action_id,
                                             option_action))
                result.append(menu_option + (self._next_action_id,))
            else:
                result.append((option_text, option_icon,
                               self._add_ids_to_menu_options(option_action),
                               self._next_action_id))
            self._next_action_id += 1
        return result

    def refresh_icon(self, is_init=True, trayMsg=None):
        hinst = win32gui.GetModuleHandle(None)
        # try to find custom icon file
        if os.path.isfile(self.icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst, self.icon, win32con.IMAGE_ICON, 0,
                                       0, icon_flags)
        # if the custom icon not found, using default
        else:
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD
        self.notify_id = (self.hwnd, 0, win32gui.NIF_ICON | win32gui.NIF_MESSAGE
                          | win32gui.NIF_TIP, win32con.WM_USER + 20, hicon,
                          self.hover_text)
        win32gui.Shell_NotifyIcon(message, self.notify_id)
        if not is_init:
            if not (trayMsg and isinstance(trayMsg, TrayMessage)):
                raise ValueError(
                    '"{}" except a "winsystray.TrayMessage" object, but gaven "{}".'
                    .format(trayMsg,
                            type(trayMsg).__name__))
            win32gui.Shell_NotifyIcon(
                win32gui.NIM_MODIFY,
                (self.hwnd, 0, win32gui.NIF_INFO, win32con.WM_USER + 20, hicon,
                 trayMsg.app, trayMsg.msg, 200, trayMsg.title))

    def create_menu(self, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::
                                                                               -1]:
            if option_icon:
                option_icon = self.prep_menu_icon(option_icon)

            if option_id in self.menu_actions_by_id:
                item, extras = win32gui_struct.PackMENUITEMINFO(
                    text=option_text, hbmpItem=option_icon, wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                self.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(
                    text=option_text, hbmpItem=option_icon, hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(self, icon):
        # preload icon
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y,
                                   win32con.LR_LOADFROMFILE)
        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        # fill background
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        # draw icon
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0,
                            win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)
        return hbm

    def command(self, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        self.execute_menu_option(id)

    def execute_menu_option(self, id):
        menu_action = self.menu_actions_by_id[id]
        if menu_action == self.QUIT:
            win32gui.DestroyWindow(self.hwnd)
        else:
            menu_action(self)


class BaseWinTrayApp():
    __metaclass__ = ABCMeta

    def __init__(self, name, icon, interval, logger):
        self.name = name
        self.icon = icon
        self.interval = interval
        self.logger = logger
        self.is_exit = False

    def start(self):
        self.message_queue = Queue.Queue()
        self._producer = threading.Thread(target=self.produce, args=())
        self._producer.setName('MessageQueueProducer')
        self._comsumer = threading.Thread(target=self.__comsume, args=())
        self._comsumer.setName('MessageQueueComsumer')
        self._producer.start()
        self._comsumer.start()

        self.root = tk.Tk()
        menu_options = ()
        self.tray = SystemTray(
            self.icon,
            self.name,
            menu_options,
            on_quit=self.__exit,
            default_menu_index=1)
        self.__minimize()
        self.root.mainloop()

    @abstractmethod
    def produce(self):
        pass

    def __minimize(self):
        self.root.withdraw()
        self.tray.show_icon()

    def __comsume(self):
        while not self.is_exit:
            if not self.message_queue.empty():
                trayMsg = self.message_queue.get()
                self.logger.info("{} get a TrayMessage：{}.".format(
                    threading.current_thread().getName(), trayMsg))
                self.tray.refresh_icon(is_init=False, trayMsg=trayMsg)
            time.sleep(self.interval)
            self.logger.info("{}: Message queue size is {}.".format(
                threading.current_thread().getName(),
                self.message_queue.qsize()))
            if not self._producer.is_alive:
                self.logger.info("{}: The produce thread dead, restart it.".format(threading.current_thread().getName()))
                self._producer.start()

    def __exit(self, _sysTrayIcon=None):
        self.is_exit = True
        self._producer.join()
        self._comsumer.join()
        self.root.destroy()
        self.logger.info('{} has exited.'.format(self.name))
