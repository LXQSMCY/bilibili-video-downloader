# coding:utf-8
from setuptools import setup, find_packages

requirements = []

setup(
    name='flvcdAPI',
    version='v1.0',
    packages=find_packages(),
    url='https://github.com/zhaohui8969/bilibili-video-downloader',
    license='GPLv2',
    author='natas',
    author_email='natas_hw@163.com',
    description=u'OS X 下的一个bilibili视频下载器',
    entry_points={
        'console_scripts': [
            'flvcdapi = flvcdapi.flvcdapi:main',
        ]
    },
)
