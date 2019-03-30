#!/usr/bin/env python
# -*- coding=UTF-8 -*-
'''
@Author: shy
@Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@Version: v1.0
@Licence: GPLv3
@Description: -
@Since: 2018-11-16 10:53:26
@LastTime: 2019-03-30 14:21:13
'''

import os
import sys
import time
import atexit
from abc import ABCMeta
from abc import abstractmethod
from signal import SIGTERM


def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    '''Damonize current progress

    Keyword Arguments:
        stdin {str} -- Redirect for standard input (default: {'/dev/null'})
        stdout {str} -- Redirect for standard output (default: {'/dev/null'})
        stderr {str} -- Redirect for standard error (default: {'/dev/null'})
    '''

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        raise OSError(
            "Fork #1 failed: (ERROR CODE: %d), %s\n" % (e.errno, e.strerror))

    # os.chdir("/")
    os.umask(0)
    os.setsid()

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # second parent progress exit
            sys.exit(0)
    except OSError, e:
        raise OSError(
            "Fork #2 failed: (ERROR CODE: %d), %s\n" % (e.errno, e.strerror))

    # progress is daemonized, redirect the fi ledescraptor
    for f in sys.stdout, sys.stderr:
        f.flush()
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+', 0)
    # dup2 for dumplicate and close filedecraptor
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


class Daemon():
    """
    A generic daemon class.
    Usage: subclass the Daemon class and override the run() method
    """
    __metaclass__ = ABCMeta

    def __init__(self,
                 pidfile,
                 stdin='/dev/null',
                 stdout='/dev/null',
                 stderr='/dev/null',
                 args=None):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.args = args

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            raise OSError("Fork #1 failed: (ERROR CODE: %d), %s\n" %
                          (e.errno, e.strerror))

        # decouple from parent environment
        # os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            raise OSError("Fork #2 failed: (ERROR CODE: %d), %s\n" %
                          (e.errno, e.strerror))

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        if type(sys.stderr) is file:
            os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "Pidfile %s already exist. Daemon already running?\n"
            raise OSError(message % self.pidfile)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "Pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                raise OSError(err)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    @abstractmethod
    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """


def main():
    '''Example function, print a number and timestamp for every second'''
    import time
    sys.stdout.write('Daemon started with pid %d\n' % os.getpid())
    sys.stdout.write('Daemon stdout output\n')
    sys.stderr.write('Daemon stderr output\n')
    c = 0
    while True:
        sys.stdout.write('%d: %s\n' % (c, time.ctime()))
        sys.stdout.flush()
        c = c + 1
        time.sleep(1)


if __name__ == "__main__":
    daemonize('/dev/null', '/tmp/daemon_stdout.log', '/tmp/daemon_error.log')
    main()
