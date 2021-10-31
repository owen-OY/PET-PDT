# -*- coding:utf-8 -*-

# @Author       : xuanye.wang
# @Date         : 2021/10/27 22:14
# @File         : code_将多个文件夹中的文件移动到一个目录.py
'''
@Mark:          :1、输入多个文件夹的目录路径；
                 2、输入新目录的路径；
                 3、输入新目录的名称；
                 4、移动完文件后，自动删除源文件；
'''


import os
import shutil
from loguru import logger


def mergeDir(dirPath, newDirPath):
    for root, dirs, files in os.walk(dirPath, topdown=False):
        for name in files:
            filePath = os.path.join(root, name) # 文件存放路径
            movePath = os.path.join(newDirPath, name) # movePath：指定移动文件夹
            shutil.copyfile(filePath, movePath)
            logger.info('文件移动完毕，开始删除源文件...')
            try:
                os.remove(filePath)
            except:
                logger.info('删除文件失败！')


if __name__ == '__main__':
    mergeDir(dirPath=input('请输入要处理的目录路径：'), newDirPath=input('请输入要新目录路径：'))
