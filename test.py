#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2015-2018 Shenzhen Auto-link world Information Technology Co., Ltd.
  All Rights Reserved

  Name: test.py
  Purpose:

  Created By:    Clive Lau <liuxusheng@auto-link.com.cn>
  Created Date:  2018-03-01

  Changelog:
  Date         Desc
  2018-03-01   Created by Clive Lau
"""

import threading
from time import sleep


class TimerRepeater(object):
    """
    A simple timer implementation that repeats itself
    """
    # Constructor
    def __init__(self, name, interval, target, args=[], kwargs={}):
        """
        Creates a timer

        :param name:     name of the thread
        :param interval: interval in second between execution of target
        :param target:   function that is called every 'interval' seconds
        :param args:     non keyword-argument list for target function
        :param kwargs:   keyword-argument list for target function
        """
        # define thread and stopping thread event
        self._name = name
        self._thread = None
        self._event = None
        # initialize target and its arguments
        self._target = target
        self._args = args
        self._kwargs = kwargs
        # initialize timer
        self._interval = interval

    # Runs the thread that emulates the timer
    def _run(self):
        """
        Runs the thread that emulates the timer

        :return: None
        """
        while not self._event.wait(self._interval):
            self._target(*self._args, **self._kwargs)

    # Starts the timer
    def start(self):
        """
        Starts the timer

        :return: None
        """
        # avoid multiple start calls
        if self._thread is None:
            self._event = threading.Event()
            self._thread = threading.Thread(None, self._run, self._name)
            self._thread.start()

    # Stops the timer
    def stop(self):
        """
        Stops the timer

        :return: None
        """
        if self._thread is not None:
            self._event.set()
            self._thread = None


def tmrRead_Tick():
    print('Hello World')


def tmrWrite_Tick():
    print('World Hello')


if __name__ == '__main__':
    tmrRead = TimerRepeater("tmrRead", 1, tmrRead_Tick)
    tmrWrite = TimerRepeater("tmrWrite", 1, tmrWrite_Tick)
    tmrRead.start()
    tmrWrite.start()
    try:
        while True:
            sleep(4)
    except KeyboardInterrupt:
        tmrRead.stop()
        tmrWrite.stop()
