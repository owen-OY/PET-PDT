# -*- coding:utf-8 -*-

# @Author       : kintan.wang
# @Date         : 2021/9/27 18:03
# @File         : codes_单线程_觅知网_T7200猫叫声音频素材爬虫.py
# @Mark         :
                # 1.合入多线程爬虫代码
                # 2.增加log打印级别以及log文件输出
# @NewestUpdateDate   :2021/9/27 18:03


import re
import requests
import datetime
import os
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
        logger.add(f'./log/{timeinfo}_codes_单线程_觅知网_T7200猫叫声音频素材爬虫.log', rotation='50MB', encoding='utf-8',
                   enqueue=True)  # 输出控制台中的log文件
        if not os.path.exists(f'./result'):
            os.mkdir(f'./result')  # 在工程下创建./result目录
            logger.info(f'创建./result目录成功！')
        else:
            logger.info(f'当前已存在./result目录，不再创建！')

        for num in range(1, 5): # 最大页码数加1
            urlList = [f'https://www.51miz.com/so-sound/3550099/p_{num}/']
            soundLinkAfterList1 = []
            responce = requests.get(urlList, headers=HEADERS, timeout=60)
            responce.encoding = 'utf-8' # 防止输出的网页代码出现中文乱码；
            soundLinkAfter1 = re.findall('<source src="(.*?)" type="audio/mpeg">', responce.text)
            soundLinkAfterList1.extend(soundLinkAfter1) # 已取出当前页面的所有音频下载链接
            for j in range(30):
                videoUrl = 'https:' + f'{soundLinkAfterList1[j]}'
                filename = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
                res = requests.get(videoUrl, stream=True)
                logger.info('开始下载：{}'.format(videoUrl))
                with open(f'./result/{filename}.mp3', 'wb') as f:
                    logger.info('音频文件下载成功！')
                    for chunk in res.iter_content(chunk_size=10240):
                        f.write(chunk)
                    f.close()
                    logger.info('获取图片成功！--对应的页码为%d' % num)


if __name__ == '__main__':
    getMp3 = GetMp3()
    try:
        getMp3.getCatsound()
    except:
        print('本循环轮次获取音频失败！')
