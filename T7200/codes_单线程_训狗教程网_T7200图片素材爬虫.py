# -*- coding:utf-8 -*-

# @Author       : kintan.wang
# @Date         : 2021/8/6 15:00
# @File         : codes_单线程_训狗教程网_T7200图片素材爬虫.py
# @Mark         :
                # 1.增加log打印级别以及log文件输出
# @NewestUpdateDate   :2021/9/22  16:19


import requests
import re
import time
import datetime
import os
from loguru import logger


timeinfo = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}


class GetImg(object):
    def dog_img(self, num):
        while True:
            urlList = [f'http://www.boqii.com/pet-all/dog/?p={num}']
            htmlNumList = []
            for i in urlList:
                responce1 = requests.get(i, headers=HEADERS, timeout=60)
                responce1.encoding = 'utf-8'  # 防止输出的网页代码出现中文乱码
                dogHtmlList = re.findall('<dl><dt><a target="_blank" href="http://www.boqii.com/entry/detail/(.*?).html"><img',responce1.text)
                htmlNumList.extend(dogHtmlList)
                for j in dogHtmlList:
                    dog_img_html = 'http://www.boqii.com/entry/album/' + j
                    responce2 = requests.get(dog_img_html, headers=HEADERS, timeout=60) # 请求后跳转
                    dog_name = re.findall('html">(.*?)</a> > 词条相册</div>', responce2.text)[0] # 获取图片的命名
                    dog_img_list = re.findall('<img alt=".*?" src="(.*?)".*?></a></dt></dl>', responce2.text)
                    if not os.path.exists('./log'):
                        os.mkdir('./log')  # 在工程下创建log目录
                        logger.info('创建log目录成功！')
                    if not os.path.exists('./result'):
                        os.mkdir('./result')  # 在工程下创建result目录
                        logger.info('创建result目录成功！')
                    logger.add(f'./log/{timeinfo}_codes_单线程_训狗教程网_T7200图片素材爬虫.log', rotation='50MB', encoding='utf-8',
                               enqueue=True)  # 输出控制台中的log文件
                    for k in dog_img_list:
                        time.sleep(1) # 防止生成图片时发生覆盖下载
                        get_img = requests.get(k, headers=HEADERS, timeout=60)
                        filename1 = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
                        try:
                            with open(f'./result/{filename1}.jpg', 'wb') as f:
                                f.write(get_img.content)
                                f.close()
                                logger.info('获取图片成功！--对应的页码为%d' % num)
                        except:
                            logger.info('获取图片失败！--对应的页码为%d' % num)
            num += 1


if __name__ == '__main__':
    getimg = GetImg()
    while True:
        try:
            getimg.dog_img(num=1)  # 设置起始页码
        except:
            logger.info('本循环轮次获取图片失败！')
