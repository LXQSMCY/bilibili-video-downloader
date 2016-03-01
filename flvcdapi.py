#!/usr/bin/env python3
#coding: utf-8
# 这个文件用来完成将视频的地址提交到flvcd.com上，再对返回的结果做格式化处理
__author__ = 'natas'
import re, urllib, subprocess, sys
from urllib import request
from time import sleep

FLVCDURL=[r'http://www.flvcd.com/parse.php?format=&kw=', r"&format=super"]


def getflvcdresult(VIDEOURL):
    # 构造请求
    commiturl = FLVCDURL[0] + VIDEOURL + FLVCDURL[1]
    httpheaders = {'User-Agent': 'Mozilla/5.0 (Windows; '
                                 'U; '
                                 'Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = request.Request(commiturl, headers=httpheaders)
    resultcontent = request.urlopen(req).read()
    resultcontent = resultcontent.decode('gbk')
    #print(resultcontent)
    # 提取网页中返回的信息
    key2find = [u'下载地址：<a href=', u'var cliptitle = ']
    key = ['', '']
    print('INFO_Extract...')
    index = resultcontent.find(key2find[0])
    #print('Locate:%d' % (index))
    # URL
    key[0] = (((re.compile('".*?"')).findall(resultcontent[index+len(key2find[0])::]))[0])[1:-1:]
    index = resultcontent.find(key2find[1])
    #print('Locate:%d' % (index))
    # Title
    key[1] = (((re.compile('".*?"')).findall(resultcontent[index+len(key2find[1])::]))[0])[1:-1:].split(sep='/')[0]  # 可怕的文件名含有起卦自负
    print('URL:{0}\nTitle:{1}'.format(key[0], key[1]))
    # 这里返回了一个播放用的URL和标题
    return key[0], key[1]


def save2file(url, filename, directory=r'.', playnow = True):
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
    playerbin=r'/Applications/VLC.app/Contents/MacOS/VLC'
    subprocess.Popen([playerbin, filename])


def helper():
    print('Help:\n'
          '    This is a tool that can get bilibili.com video\'s download link address.\n'
          '    Just paste the video playing page url here. press [Enter]\n'
          '    Like this: {0} [Enter]\n'
          '    Exit with Ctrl+C qwq\n'.format(VIDEOURL))


if __name__ == '__main__':
    VIDEOURL = r'http://www.bilibili.com/video/av2769452/'
    helper()
    try:
        while True:
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
    except (KeyboardInterrupt, SystemExit):
        exit
    except Exception as e:
        print(e)
        pass
