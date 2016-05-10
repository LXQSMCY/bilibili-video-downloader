#!/usr/bin/python
# coding: utf-8
# !!!key: This is a python 2.7 version, and you need a Appkit py module.


import re
import time
import os

import AppKit

__author__ = 'natas'

# 剪切版类
class Clipboard:
    def __init__(self):
        self.pb = AppKit.NSPasteboard.generalPasteboard()

    def __call__(self):
        return self.pb.stringForType_(AppKit.NSStringPboardType)


# 测试内容是否是我们所需的
class ContentChecker:
    def __init__(self, re_str):
        self.re_obj = re.compile(re_str)

    def __call__(self, content):
        matches = self.re_obj.findall(content)
        if len(matches) == 0:
            return False
        else:
            return True


# http://baidu.com

def main():
    # init
    pb = Clipboard()
    cont_chk = ContentChecker(ur'^http\://')
    last_clip = ''
    while True:
        clip = pb()
        if (clip != last_clip) & cont_chk(clip):
            print(clip)
        time.sleep(0.2)
        last_clip = clip


if __name__ == "__main__":
    main()
