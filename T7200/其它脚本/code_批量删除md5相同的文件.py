# -*- coding:utf-8 -*-

# @Author       : xuanye.wang
# @Date         : 2021/10/27 22:14
# @File         : code_批量删除md5相同的文件.py
'''
@Mark:          :1、如果文件的内容一样，只是文件名不一样，可用该脚本执行，利用md5查重；
                 2、输入需要md5查重的目录路径即可；
                 3、该脚本可查重图片、音频、视频；
'''

import hashlib
import os
from loguru import logger
from collections import Counter


def getFileMD5(filepath):
    '''
    :param filepath:
    :return: md5
    '''
    f = open(filepath, 'rb')
    md5 = hashlib.md5()
    md5.update(f.read())
    hash = md5.hexdigest()
    f.close()
    return str(hash)

def checkRemove(path):
    files = []
    fileMd5s = []
    lines = os.listdir(path)

    for idx, file in enumerate(lines):
        Md5 = getFileMD5(path + file)
        fileMd5s.append(Md5)
        files.append(file)

    tmp = dict(zip(files, fileMd5s))
    logger.info('构建文件与MD5映射完毕！')
    chachong = Counter(fileMd5s)
    logger.info('查重中......')
    for key, value in chachong.items():
        if int(value) > 1:
            logger.info(key, value)
            chongfu = [key2 for key2, value2 in tmp.items() if value2 == key]
            logger.info(chongfu)
            with open('chongfu.txt', 'a') as fw: # 输入md5重复的文件名
                fw.write(str(chongfu)[1:-1] + '\n')
            for i in range(len(chongfu)-1): # 删除md5重复的文件，保留一个
                rmf = path + chongfu[i]
                logger.info(rmf)
                try:
                    os.remove(f'{rmf}')
                except:
                    logger.info('删除文件失败！')


if __name__ == '__main__':
    path = input('请输入需要查重的目录：')
    checkRemove(path)
