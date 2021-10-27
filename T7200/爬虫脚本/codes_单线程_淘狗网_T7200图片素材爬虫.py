# -*- coding:utf-8 -*-

# @Author       : kintan.wang
# @Date         : 2021/8/10 17:27
# @File         : codes_单线程_淘狗网_T7200图片素材爬虫.py
# @Mark         :
                # 1.增加log打印级别以及log文件输出
# @NewestUpdateDate   :2021/9/22  16:49


import re
import requests
import time
import datetime
from loguru import logger
import os

timeinfo = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'} # 头部信息


class GetImg(object):
    def getDogPicture(self, num):
        while True:
            urlList = [f'http://www.dog126.com/buydog.html?page={num}']
            pictureLinkAfterList = []
            for i in urlList:
                responce1 = requests.get(i, headers=HEADERS, timeout=60)
                responce1.encoding = 'utf-8'  # 防止输出的网页代码出现中文乱码
                pictureLinkAfter1 = re.findall('src=".*?" data-original="(.*?.jpeg)"', responce1.text)
                pictureLinkAfterList.extend(pictureLinkAfter1)
                for getPictureLink in pictureLinkAfterList:
                    responce2 = requests.get(getPictureLink, headers=HEADERS, timeout=60)
                    responce1.encoding = 'utf-8'  # 防止输出的网页代码出现中文乱码
                    filename = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
                    if not os.path.exists('./log'):
                        os.mkdir('./log')  # 在工程下创建log目录
                        logger.info('创建log目录成功！')
                    if not os.path.exists('./result'):
                        os.mkdir('./result')  # 在工程下创建result目录
                        logger.info('创建result目录成功！')
                    logger.add(f'./log/{timeinfo}_codes_单线程_淘狗网_T7200图片素材爬虫.log', rotation='50MB', encoding='utf-8',
                               enqueue=True)  # 输出控制台中的log文件
                    time.sleep(1) # 防止生成图片时发生覆盖下载
                    try:
                        with open(f'./result/{filename}.jpg', 'wb') as f:
                            f.write(responce2.content)
                            f.close()
                            logger.info('获取图片成功！--对应的页码为%d' % num)
                    except:
                        logger.info('获取图片失败！--对应的页码为%d' % num)
            num += 1


if __name__ == '__main__':
    getimg = GetImg()
    while True:
        try:
            getimg.getDogPicture(num=1) # 设置起始页码
        except:
            logger.info('本循环轮次获取图片失败！')
