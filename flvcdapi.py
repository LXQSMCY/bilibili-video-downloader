#!/usr/bin/env python
# coding: utf-8
# 这个文件用来完成将视频的地址提交到flvcd.com上，再对返回的结果做格式化处理
# 兼容python2，3
from __future__ import print_function, unicode_literals
from builtins import input
from six.moves import urllib
# try:
#     from urllib import request
# except:
#     import urllib as request

__author__ = 'natas'

import re
import subprocess
import sys
import os
from time import sleep

FLVCDURL=[r'http://www.flvcd.com/parse.php?format=&kw=', r"&format=super"]
FNULL=open(os.devnull, 'w')

def getflvcdresult(VIDEOURL):
    # TODO: 这里写的太麻烦了，不如用BeautifulSoup重写
    # 构造请求
    commiturl = FLVCDURL[0] + VIDEOURL + FLVCDURL[1]
    httpheaders = {'User-Agent': 'Mozilla/5.0 (Windows; '
                   'U; '
                   'Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(commiturl, headers=httpheaders)
    resultcontent = urllib.request.urlopen(req).read()
    resultcontent = resultcontent.decode('gbk')
    # 提取网页中返回的信息
    key2find = [u'下载地址：<a href=', u'var cliptitle = ']
    key = ['', '']
    print('INFO_Extract...')
    index = resultcontent.find(key2find[0])
    # URL
    key[0] = (((re.compile('".*?"')).findall(resultcontent[index+len(key2find[0])::]))[0])[1:-1:]
    index = resultcontent.find(key2find[1])
    # Title
    key[1] = (((re.compile('".*?"')).findall(resultcontent[index+len(key2find[1])::]))[0])[1:-1:].split(sep='/')[0]
    print('URL:{0}\nTitle:{1}'.format(key[0], key[1]))
    # 这里返回了一个播放用的URL和标题
    return key[0], key[1]


def save2file(url, filename, directory=r'.', playnow = True):
    # TODO: 重写下载方法提高下载速度
    full_path=directory + '/' + filename
    print('Save file to: {0}'.format(full_path))
    open(full_path, 'w').close()
    if playnow :
        print('Call player')
        openPlayer(full_path)
    urllib.request.urlretrieve(url, full_path)
    print('Downloaded.'  '🍺')
    return filename


def openPlayer(filename):
    # TODO: 重写打开播放器的方式，不生成新的进程而是用原有的进程播放
    playerbin=r'/Applications/VLC.app/Contents/MacOS/VLC'
    subprocess.Popen([playerbin, filename], stdout=FNULL, stderr=FNULL)


def helper():
    print('Help:\n'
          '    This is a tool that can get bilibili.com video\'s download link address.\n'
          '    Just paste the video playing page url here. press [Enter]\n'
          '    Like this: {0} [Enter]\n'
          '    Exit with Ctrl+C qwq\n'.format(VIDEOURL))


if __name__ == '__main__':
    VIDEOURL = r'http://www.bilibili.com/video/av2769452/'
    helper()
    while True:
        try:
            print('Input here: ', end='')
            user_input=input()
            if user_input == '':
                continue
            VIDEOURL=user_input
            video_info = getflvcdresult(VIDEOURL)
            # 如果返回'-'则表示出现了错误？从现象上来看是这样的，有待详细研究！
            if video_info[1] == '-':
                print('Here we got a error. Forget it.')
                continue
            save2file(video_info[0], video_info[1])
        # 处理 C-c异常
        except (KeyboardInterrupt, SystemExit) as e:
            print("\n退出")
            break
        except Exception as e:
            raise
        print("End loop.")
