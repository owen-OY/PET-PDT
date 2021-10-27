# -*- coding:utf-8 -*-

# @Author       : kintan.wang
# @Date         : 2021/8/10 20:41
# @File         : codes_多线程_veer_T7200狗狗图片素材爬虫.py
# @Mark         :
                # 1.合入多线程爬虫代码
                # 2.增加log打印级别以及log文件输出
                # 3.增加当前结果目录满一定数量图片后(约25000张)，自动新增并写入下一个文件夹
# @NewestUpdateDate   :2021/9/24  15:51


import re
import requests
import datetime
import threading
import os
from loguru import logger
import time

timeinfo = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}  # 头部信息


class GetImg(object):
    def __init__(self, num, dirnum):
        self.num = num
        self.dirnum = dirnum

    def getDogPicture(self):
        while True:
            urlList = [f'https://www.veer.com/search-image/gou/?utm_source=baidusem&utm_medium=cpc&utm_campaign=B1-%E5%9B%BE%E7%89%87-%E4%BA%A7%E5%93%81%E9%95%BF%E5%B0%BE%E8%AF%8D1&utm_content=%E4%BA%A7%E5%93%81%E9%95%BF%E5%B0%BE%E8%AF%8D-01&utm_term=%E7%8B%97&chid=901&bd_vid=8225438318471432986&page={self.num}']
            pictureLinkAfterList1 = []
            for i in urlList:
                    responce = requests.get(i, headers=HEADERS, timeout=60)
                    responce.encoding = 'utf-8' # 防止输出的网页代码出现中文乱码
                    pictureLinkAfter1 = re.findall('<a class="asset_link draggable" href="(.*?)" target="_blank"', responce.text)
                    pictureLinkAfterList1.extend(pictureLinkAfter1)
                    for j in range(int(len(pictureLinkAfterList1)/10)):
                        for k in range(10):
                            t = threading.Thread(target=GetImg(self.num, self.dirnum).run, args=(pictureLinkAfterList1, j, k))  # 开一个新线程
                            t.setDaemon(True)  # 守护进程
                            # time.sleep(0.2) # 可防止图片漏下载，但获取图片的速度就缓慢了许多
                            t.start()  # 启动进程
            self.num += 1
            if not os.path.exists('./log'):
                os.mkdir('./log')  # 在工程下创建./log目录
                logger.info('创建./log目录成功！')
            else:
                logger.info('当前已存在./log目录，不再创建！')
            logger.add(f'./log/{timeinfo}_codes_多线程_veer_T7200狗狗图片素材爬虫.log', rotation='50MB', encoding='utf-8', enqueue=True)  # 输出控制台中的log文件

            if not os.path.exists(f'./result{self.dirnum}'):
                os.mkdir(f'./result{self.dirnum}')  # 在工程下创建./result目录
                logger.info(f'创建./result{self.dirnum}目录成功！')
            else:
                logger.info(f'当前已存在./result{self.dirnum}目录，不再创建！')

            for root, dirs, files in os.walk(f'./result{self.dirnum}'):
                filesCount = 0
                logger.info(f'此时./result{self.dirnum}的目录文件数为%d' % len(files))
                filesCount += len(files)
                if filesCount > 25000: # 因为是以每轮次获取的图片为计量单位，所以不可能等于某个数量，会涉及到requests失败的情况
                    print('filrcount为%d' % filesCount)
                    self.dirnum += 1
                    os.mkdir(f'./result{self.dirnum}')
                    logger.info(f'创建./result{self.dirnum}目录成功！')
            else:
                logger.info(f'当前已存在./result{self.dirnum}目录，不再创建！')
            '''文件计数的第二种方法：
            for dirpath, dirname, filename in os.walk(f'./result{self.dirnum}'):
                fileCount = 0
                for file in filename:
                    fileCount += 1
                    if fileCount == 10:
            '''

    def run(self, pictureLinkAfterList1, j, k):
        html2 = requests.get(pictureLinkAfterList1[j * 10 + k], headers=HEADERS, timeout=180).text
        pictureLinkAfter2 = re.findall('<img alt=.*? src="(.*?)"', html2)
        pictureUrl = 'https:' + f'{pictureLinkAfter2[0]}'
        try:
            getImg = requests.get(pictureUrl, headers=HEADERS, timeout=180)
            filename1 = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            with open(f'./result{self.dirnum}/{filename1}{j}{k}.jpg', 'wb') as f:
                logger.warning(f'此时写文件的目录为./result{self.dirnum}')
                f.write(getImg.content)
                f.close()
                logger.info('获取图片成功！--对应的页码为%d' % self.num)
        except:
            logger.info('获取图片失败！--对应的页码为%d' % self.num)


if __name__ == '__main__':
    getimg = GetImg(1, 1) # 设置起始页码、起始结果目录
    while True:
        try:
            getimg.getDogPicture()
        except:
            logger.info('本循环轮次获取图片失败！')
