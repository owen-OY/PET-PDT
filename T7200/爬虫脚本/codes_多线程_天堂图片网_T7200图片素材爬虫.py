# -*- coding:utf-8 -*-

# @Author       : mancheng.ni
# @Date         : 2021/8/9 20:17
# @File         : codes_多线程_天堂图片网_T7200图片素材爬虫.py
# @Mark         :
                # 1.合入多线程爬虫代码
                # 2.增加log打印级别以及log文件输出
# @NewestUpdateDate   :2021/9/22  14:54


import threading
import re
import requests
import time
import os
import datetime
from loguru import logger
from queue import Queue

timeinfo = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
jpg_lock = threading.RLock()


class ProducerThread(threading.Thread):
    """
    图片的数据生产
    """
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.init_url = 'https://www.ivsky.com/tupian/gougou_t1003/'

    def getHtml(self,page):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
        for i in range(5):
            try:
                if page == 1:
                    r = requests.get(self.init_url, headers=header, timeout=30)
                else:
                    r = requests.get(self.init_url + 'index_{}.html'.format(str(page)), headers=header, timeout=30)
                r.encoding = 'utf-8'
                logger.info('解析html{},{}'.format('/index_{}.html'.format(str(page)), str(len(r.text))))
                return r.text
            except:
                logger.info('解析html失败{},重试{}次'.format('/index_{}.html'.format(str(page)), str(i+1)))

    def getImg(self, content):
        reg = '<img src="(.*?.jpg)"'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, content)
        for i in imglist:
            imgUrl = 'https:' + i
            imgUrl = imgUrl.replace('img.ivsky', 'img-pre.ivsky').replace('/t/', '/pre/')
            logger.info(imgUrl)
            self.queue.put(imgUrl)

    def run(self):
        i = 1
        while True:
            html = self.getHtml(i)
            if html.find('抱歉，您所浏览的页面不存在或暂时无法访问') != -1:
                break
            else:
                self.getImg(html)
            i += 1


class consumeThread(threading.Thread):
    """
    图片的数据消费
    """
    def __init__(self, name, queue):
        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue
        logger.info('start consumeThread ' + name)
        if not os.path.exists('./result'):
            os.mkdir('./result')

    def down_img(self, imgurl):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
        logger.info('消费线程{}下载图片'.format(self.name))
        img_name = imgurl.split('/')[-1]
        img = requests.get(imgurl, headers=header)
        if not os.path.exists('./log'):
            os.mkdir('./log') # 在工程下创建log目录
            logger.info('创建log目录成功！')
        if not os.path.exists('./result'):
            os.mkdir('./result') # 在工程下创建result目录
            logger.info('创建result目录成功！')
        logger.add(f'./log/{timeinfo}_codes_多线程_天堂图片网_T7200图片素材爬虫.log', rotation='50MB', encoding='utf-8', enqueue=True) # 输出控制台中的log文件
        with open('./result/{}'.format(img_name), 'wb') as f:
            logger.info(len(img.content))
            f.write(img.content)

    def run(self):
        global jpg_lock
        while True:
            if self.queue.empty():
                logger.info('{}消费线程处理完毕'.format(self.name))
                break
            img = self.queue.get()
            logger.info('消费线程{}取出1个元素,还剩{}个元素'.format(self.name, self.queue.qsize()))
            jpg_lock.acquire()
            jpg_lock.release()
            self.down_img(img)
            # for i in range(3):
            #     try:
            #         self.down_img(img)
            #         break
            #     except:
            #         logger.info('消费线程{}下载图片失败,重试第{}次'.format(self.name, i + 1))
            time.sleep(0.2)


if __name__ == '__main__':
    q = Queue()
    ImgProducerThread = ProducerThread(q)
    ImgProducerThread.start()
    time.sleep(3)
    threadList = []
    for i in range(5): # 队列数可更改
        thread = consumeThread('consume-%s' % i, q)
        threadList.append(thread)
    for thread in threadList:
        thread.start()
    ImgProducerThread.join()
    for thread in threadList:
        thread.join()
