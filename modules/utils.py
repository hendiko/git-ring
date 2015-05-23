#!/usr/bin/env python
# -*- coding: utf8 -*-
# Created by Xavier Yin on 2015/2/11


import subprocess
import sys
import threading


def monkey():
    p = subprocess.Popen(["adb", "shell", "monkey", "-p", "com.shuqi.controller", "-v", "5000"], stdout=subprocess.PIPE)

    while True:
        line = p.stdout.readline()
        if not line:
            break
        print "Read: ", line


def read():
    th = threading.Thread(target=monkey)
    th.start()
    print "1"
    while True:
        print "2"
        line = sys.stdin.readline()
        if not line:
            break
        print "READ: ", line

if __name__ == "__main__":
    monkey()