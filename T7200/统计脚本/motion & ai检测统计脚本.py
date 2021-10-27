# -*- coding:utf-8 -*-

# @Author       : kintan.wang
# @Date         : 2021/10/1 19:00
# @File         : code_motion ai触发统计脚本.py
'''
@Mark           :

'''


import xlrd # 读取excel中的数据
import xlwt # 向excel中写入数据
import pandas
import os
import re
import time
import sys
from loguru import logger


# 防止空数据时，出现脚本报错
def none(fun, num=0):
    if fun == None or fun == '':
        data = 'None'
    else:
        data = str(fun.group(num))
    return data

# 获取log中的数据
def getData(logFilePath):
    data = open(logFilePath, 'r', encoding='latin1')
    sensitivityIdxTimeInfoList = []
    sensitivityIdxInfoList = []
    for line in data:
        if line.find('sensitivity_idx:') != -1: # 有找到相关的数据
            sensitivityIdxTimeInfo = re.search(r'(\d{1,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}.\d{1,3})', line)
            sensitivityIdxInfo = re.search(r'sensitivity_idx:(.)', line)
            sensitivityIdxTimeInfoNew = none(sensitivityIdxTimeInfo, 1)
            sensitivityIdxTimeInfoList.append(sensitivityIdxTimeInfoNew)
            sensitivityIdxInfoList.append(sensitivityIdxInfo)
    return sensitivityIdxTimeInfoList,sensitivityIdxInfoList

def countData(sensitivityIdxTimeInfList, sensiivityIdxInfoList):
    '''
    往excel表格中写入数据
    :param timeList:
    :return:
    '''
    workbook = xlwt.Workbook(encoding='utf-8')
    timeListLen = len(sensitivityIdxTimeInfoList)
    sheet = workbook.add_sheet('result', cell_overwrite_ok=True) # cell_overwrite_ok=True表示这个表格可以覆盖
    sheet.write(0, 0, '测试序号')
    sheet.write(0, 1, '时间')
    sheet.write(0, 2, '当前档位')
    # sheet.write(0, 2, '检测类型')
    # sheet.write(0, 3, '开始等待视频AI检测')
    # sheet.write(0, 4, 'motion触发')
    # sheet.write(0, 5, 'AI检测成功')
    # sheet.write(0, 6, '开始录制')
    # sheet.write(0, 7, '向MMC发送录制指令')
    # sheet.write(0, 8, '触发狗脸/狗体检测')
    # sheet.write(0, 9, '确认录制有效，有文件生成')
    # sheet.write(0, 10, '获取视频大小')
    # sheet.write(0, 11, '等待发送录制视频数')
    # sheet.write(0, 12, '失败重传')
    sheetLine = 1
    for i in range(timeListLen):
        countList = []
        for j in sensitivityIdxTimeInfoList:
            countList.append(j)
        if len(countList) > 0:
            sheet.write(sheetLine, 0, i+1)
            sheet.write(sheetLine, 1, sensitivityIdxTimeInfoList[i])
            sheet.write(sheetLine, 2, sensitivityIdxInfoList[i])
            sheetLine += 1


    workbook.save('result.xlsx')


if __name__ == '__main__':
    while True:
        logFilePath = input('请输入motion&AI检测的log文件绝对路径：')
        getdata = getData(logFilePath)
        countData(getdata)
        logger.info('执行完成！')
        time.sleep(2)
