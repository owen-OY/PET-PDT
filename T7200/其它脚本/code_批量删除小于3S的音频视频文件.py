# -*- coding:utf-8 -*-

# @Author       : xuanye.wang
# @Date         : 2021/10/29 22:14
# @File         : code_批量删除小于自定义时长的音频视频文件.py
'''
@Mark:          :1、该脚本只能删除音频视频文件；
                 2、输入需要目录路径即可；
'''

import eyed3
import time
import os
from loguru import logger

for root, dirs, files in os.walk(f'./result'):  # 判断下载的音频时长，小于3S则删除该文件
    for file in files:
        musicPath = rf'./result/{file}'
        time.sleep(0.5)
        mp3Info = eyed3.load(musicPath).info.time_secs
        if mp3Info < 3:
            logger.info('正在删除文件--%s' % musicPath)
            os.remove(musicPath)
