#!/usr/bin/python
#coding=utf-8
# !!!key: This is a python 2.7 version, and you need a Appkit py module.
__author__ = 'natas'

from AppKit import  *
import re, time, os
# 剪切版类
class clipboard:
    def __init__(self):
        self.pb = NSPasteboard.generalPasteboard()

    def __call__(self):
        return self.pb.stringForType_(NSStringPboardType)


# 测试内容是否是我们所需的
class content_checker:
    def __init__(self, re_str):
        self.re_obj = re.compile(re_str)

    def __call__(self, content):
        matches = self.re_obj.findall(content)
        if len(matches) == 0:
            return FALSE
        else:
            return TRUE
# http://baidu.com

def main():
    # init
    pb = clipboard();
    cont_chk = content_checker(ur'^http\://')
    last_clip = ''
    while TRUE:
        clip = pb()
        if (clip != last_clip) & cont_chk(clip):
            os.system('echo %s' % clip)
        time.sleep(0.2)
        last_clip = clip

if __name__ == "__main__":
    main()