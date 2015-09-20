#!/usr/bin/env python3
#coding=utf-8
__author__ = 'natas'
# 这个文件用来完成批量的下载，并不播放，只是使用多线程下载

import flvcdapi
import threading
import sys

# 用来被作为单独的线程启动的部分
class multithread_download(threading.Thread):

    def __init__(self, thread_num, video_info):
        threading.Thread.__init__(self)     # 这里构造父对象 OOP里的概念
        self.thread_num = thread_num
        self.video_info = video_info

    def run(self):
        print('start thread %s' % self.thread_num)
        filename = flvcdapi.save2file(self.video_info[0], self.video_info[1], playnow=False)
        print('task %s : %s done.' % (self.thread_num, filename))


if __name__ == '__main__':
    count = 0
    thread_pool=[]
    print('MultiThread download.')
    try:
        while True:
            #readline = input()
            readline = sys.stdin.readline()
            readline = readline.rstrip()
            print('read: %s' % readline)
            video_info = flvcdapi.getflvcdresult(readline)
            # 如果返回'-'则表示出现了错误？从现象上来看是这样的，有待详细研究！
            if video_info[1] == '-':
                print('Here we got a error. Forget it.')
                continue
            count += 1
            # 添加任务，并启动
            th_item = multithread_download(count, video_info)
            th_item.start()
            thread_pool.append(th_item)
    except Exception as e:
        print(e)
    for th_obj in thread_pool:
        th_obj.join()
    print('end'*100)