# -*- coding:utf-8 -*-

# @Author       : kintan.wang
# @Date         : 2021/9/27 18:03
# @File         : codes_单线程_站长素材_T7200狗叫声音频素材爬虫.py
'''
# @Mark         :
                # 1.合入多线程爬虫代码
                # 2.增加log打印级别以及log文件输出
'''
# @NewestUpdateDate   :2021/9/27 18:03


import re
import requests
import datetime
import os
import time
import eyed3
from loguru import logger

timeinfo = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}  # 头部信息


class GetMp3(object):
    def getCatsound(self):
        if not os.path.exists('./log'):
            os.mkdir('./log')  # 在工程下创建./log目录
            logger.info('创建./log目录成功！')
        else:
            logger.info('当前已存在./log目录，不再创建！')
        logger.add(f'./log/{timeinfo}_codes_单线程_站长素材_T7200狗叫声音频素材爬虫.log', rotation='50MB', encoding='utf-8', enqueue=True)  # 输出控制台中的log文件
        if not os.path.exists(f'./result'):
            os.mkdir(f'./result')  # 在工程下创建./result目录
            logger.info(f'创建./result目录成功！')
        else:
            logger.info(f'当前已存在./result目录，不再创建！')

        for num in range(1, 4): # 最大页码数
            urlList = f'https://sc.chinaz.com/yinxiao/index_{num}.html?keyword=%E7%8B%97%E5%8F%AB'
            soundLinkAfterList1 = []
            responce = requests.get(urlList, headers=HEADERS, timeout=60)
            responce.encoding = 'utf-8' # 防止输出的网页代码出现中文乱码；
            soundLinkAfter1 = re.findall('<audio preload="none" src="(.*?)"></audio>', responce.text)
            soundLinkAfterList1.extend(soundLinkAfter1) # 已取出当前页面的所有音频下载链接
            for j in range(30):
                videoUrl = 'https:' + f'{soundLinkAfterList1[j]}'
                filename = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
                res = requests.get(videoUrl, stream=True, timeout=60)
                logger.info('开始下载：{}'.format(videoUrl))
                with open(f'./result/{filename}.mp3', 'wb') as f:
                    for chunk in res.iter_content(chunk_size=10240):
                        f.write(chunk)
                    f.close()
                    logger.info('下载音频成功！--对应的页码为%d' % num)
                    for root, dirs, files in os.walk(f'./result'):
                        filesCount = 0
                        logger.info(f'此时./result的目录文件数为%d' % len(files))
                        filesCount += len(files)
                        if filesCount < 41:  # 增加判断，给音频下载增加时间，不然获取了84个音频下载的连接，但下载的音频数远远小于84
                            time.sleep(10)
    #     self.deleteFile()
    #
    # def deleteFile(self):
    #     for root, dirs, files in os.walk(f'./result'):  # 判断下载的音频时长，小于3S则删除该文件
    #         for file in files:
    #             musicPath = rf'./result/{file}'
    #             time.sleep(0.5)
    #             mp3Info = eyed3.load(musicPath).info.time_secs
    #             time.sleep(0.5)
    #             if mp3Info < 3:
    #                 logger.info('正在删除文件--%s' % musicPath)
    #                 os.remove(musicPath)

if __name__ == '__main__':
    getMp3 = GetMp3()
    try:
        getMp3.getCatsound()
    except:
        print('本循环轮次获取音频失败！')
