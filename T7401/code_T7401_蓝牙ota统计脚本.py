# -*- coding:utf-8 -*-

# @Author       : kintan.wang
# @Date         : 2021/10/20 10:00
# @File         : code_T7401_蓝牙ota统计脚本.py
'''
@Mark           :
                1、2021年10月21日：
                    更改代码的整体风格；
                2、2021年10月27日：
                    将result表格的样式跟报告对应；
'''
import openpyxl

'''
Instructions    :1、在控制台输入日志的绝对路径即可；
                 2、生成的excel结果在脚本所在的目录；
TODO            :1、自动生成散点图；
'''


import datetime
import os
import xlrd
import xlwt
import re
import time
import pandas
import matplotlib.pyplot as plt # 绘制散点图
from loguru import logger

# from openpyxl.styles import Font, colors, Alignment


resultFilename = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
# 防止空数据时，出现脚本报错
def reNone(fun, num=1):
    if fun == None or fun == '':
        data = "None"
    else:
        data = str(fun.group(num))
    return data

# 根据使用者填写的路径，查找是否有log文件，预处理
def getFileName(logPath):
    everyFileNameList, filesNameList = [], []
    for files in os.listdir(logPath):
        if '.log' in files:
            everyFile = os.path.join(logPath, files)
            everyFileNameList.append(everyFile)
            filesNameList.append(files)
        else:
            logger.info('当前目录中不存在任何的.log文件')
    return everyFileNameList, logPath, filesNameList

# 统计每轮次ota的耗时
totalTimesList = [] # ota耗时列表
def totalTime(startTime, lastTime):
    lower = datetime.datetime.strptime(startTime, '%Y:%m:%d-%H:%M:%S:%f') # ota开始时间
    upper = datetime.datetime.strptime(lastTime, '%Y:%m:%d-%H:%M:%S:%f') # ota结束时间
    totalTimes = (upper - lower).total_seconds()
    totalTimesList.append(totalTimes)
    # print(totalTimes)
    return totalTimes # ota耗时

# 获取log中的数据
def getOtaLog(everyFile):
    otaEndCount, otaDownloadSuccessCount, otaDownloadFailCount = 0, 0, 0 # ota结束次数、ota下载成功次数、ota下载失败次数
    otaLines, totalCounts, lines = 0, 0, 0 # 找到ota记录的总行数、ota总次数、ota记录对应的行数
    otaCountInfoDict, otaResultInfoDict = {}, {} # ota次数信息字典、ota结果信息字典
    upgradeFailTime, upFailTime, downloadFailTimeList, downloadSuccessTimeList = [], [], [], [] # 升级失败时间、上报ota状态失败时间、下载失败时间列表、下载成功时间列表

    startTime = '2020-01-01 00:00:05'
    if ".log" in everyFile:
        everyFile = open(everyFile, "r+", encoding='latin1')
        for line in everyFile.readlines():
            # ota开始标识
            if line.find('image_transfer_start') != -1: # 能找到记录
                logTime = re.search(r"(\d{1,2}.\d{1,2}.\d{1,2}.\d{1,2}:\d{1,2}:\d{1,2}:\d{1,3})", line)
                startTime = reNone(logTime) # 判断是否为空数据
                startTime = '20' + str(startTime)
                totalCounts += 1
                otaCountInfoDict[f'｜第{totalCounts}次ota开始时间'] = startTime
                if lines <= otaLines or otaLines == 0:
                    otaLines = lines

            # ota完成，结束ota标识
            if line.find('Image is received completely') != -1: # 能找到记录
                logTime = re.search(r"(\d{1,2}.\d{1,2}.\d{1,2}.\d{1,2}:\d{1,2}:\d{1,2}:\d{1,3})", line)
                lastTime = reNone(logTime) # 判断是否为空数据
                lastTime = '20' + str(lastTime.strip(',"'))
                times = totalTime(startTime, lastTime)
                if otaLines > 0 and times <= 900:
                    logTime = str(logTime.group())
                    downloadSuccessTimeList.append(logTime)
                    otaCountInfoDict[f'第{totalCounts}次ota下载成功时间'] = lastTime
                    otaDownloadSuccessCount += 1
                    otaEndCount += 1

            lines += 1
        successRate = '%.2f%%' % ((otaEndCount / totalCounts) * 100)
        downloadRate = '%.2f%%' % ((otaDownloadSuccessCount / totalCounts) * 100)
        otaResultInfoDict['total_count'] = totalCounts  # ota总次数
        otaResultInfoDict['start_count'] = totalCounts  # ota开始次数
        otaResultInfoDict['download_success'] = otaDownloadSuccessCount  # ota下载成功
        otaResultInfoDict['download_fail'] = otaDownloadFailCount  # ota下载失败
        otaResultInfoDict['end_count'] = otaEndCount  # ota结束次数
        otaResultInfoDict['下载成功率'] = downloadRate  # 下载成功率
        otaResultInfoDict['升级成功率'] = successRate  # 升级成功率
        logger.info('执行完成')

        str_otaCountInfoDict = str((otaCountInfoDict))
        list_otaCountInfo = str_otaCountInfoDict.split(", '｜")
        one = list_otaCountInfo[0].replace("{", '')
        newOne = one.replace('｜', '') # 去除ota时间信息中的头部花括号
        two = list_otaCountInfo[-1].replace("}", '') # 去除ota时间信息中的头部花括号
        newTwo = "'" + two
        list_otaCountInfo[0] = newOne
        list_otaCountInfo[-1] = newTwo
        # print('list_otaCountInfo', list_otaCountInfo)

        # 设置表头居中对齐的样式
        headStyle = xlwt.XFStyle()
        al = xlwt.Alignment()
        al.horz = 0x02  # 设置水平居中
        al.vert = 0x01  # 设置垂直居中
        headStyle.alignment = al

        # 设置表头边框样式
        borders = xlwt.Borders()
        borders.left, borders.right, borders.top, borders.bottom = xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN
        borders.left_colour, borders.right_colour, borders.top_colour, borders.bottom_colour = 0x40, 0x40, 0x40, 0x40
        headStyle.borders = borders

        # 设置表头字体
        font = xlwt.Font()
        font.name = 'Arial' # 字体名称
        font.bold = True # 加粗
        font.underline = False # 不加下划线
        font.italic = False # 不加斜体
        font.colour_index = 1 # 纯白色字体颜色
        headStyle.font = font

        # # 设置表头背景色
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['dark_blue'] # Anker标准蓝
        headStyle.pattern = pattern

        # 设置居中对齐的样式
        style = xlwt.XFStyle()
        al = xlwt.Alignment()
        al.horz = 0x02 # 设置水平居中
        al.vert = 0x01 # 设置垂直居中
        style.alignment = al

        # 设置边框样式
        borders = xlwt.Borders()
        borders.left, borders.right, borders.top, borders.bottom = xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN
        borders.left_colour, borders.right_colour, borders.top_colour, borders.bottom_colour = 0x40, 0x40, 0x40, 0x40
        style.borders = borders

        # 向单元格中写入数据
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet = workbook.add_sheet('BlueOta_Result_Data')
        newSheet = workbook.add_sheet('BlueOta_Result_Chart')

        sheet.write(0, 0, 'ota时间信息', headStyle)
        sheet.write(0, 1, '耗时/S', headStyle)
        sheet.write(0, 2, 'ota总次数', headStyle)
        sheet.write(0, 3, 'ota开始次数', headStyle)
        sheet.write(0, 4, 'ota结束次数', headStyle)
        sheet.write(0, 5, 'ota成功率', headStyle)
        sheet.write(0, 6, '下载成功次数', headStyle)
        sheet.write(0, 7, '下载成功率', headStyle)
        sheet.write(1, 2, totalCounts, style)
        sheet.write(1, 3, totalCounts, style)
        sheet.write(1, 4, otaEndCount, style)
        sheet.write(1, 5, successRate, style)
        sheet.write(1, 6, otaDownloadSuccessCount, style)
        sheet.write(1, 7, downloadRate, style)

        newSheet.write(0, 0, '测试序号', headStyle)
        newSheet.write(0, 1, '耗时/S', headStyle)

        r = 1
        for i in list_otaCountInfo:
            sheet.write(r, 0, i, style)
            sheet.row(r-1).height_mismatch = True # 设置(初始化行-1)行为16的行高
            sheet.row(r-1).height = 20 * 16
            sheet.row(r).height_mismatch = True # 设置初始化行为16的行高
            sheet.row(r).height = 20 * 16
            r += 1

        p = 1
        for j in list_otaCountInfo:
            newData = j.split("'")
            if p==1:
                startTimeInfo = newData[3]
                endTimeInfo = newData[-2]
                lowerInfo = datetime.datetime.strptime(startTimeInfo, '%Y:%m:%d-%H:%M:%S:%f')
                upperInfo = datetime.datetime.strptime(endTimeInfo, '%Y:%m:%d-%H:%M:%S:%f')
                timeendTimeInfo = (upperInfo - lowerInfo).total_seconds()
                sheet.write(p, 1, timeendTimeInfo, style)
                newSheet.write(p, 0, p)
                newSheet.write(p, 1, timeendTimeInfo)
            elif p==len(list_otaCountInfo):
                startTimeInfo = newData[3]
                endTimeInfo = newData[-2]
                lowerInfo = datetime.datetime.strptime(startTimeInfo, '%Y:%m:%d-%H:%M:%S:%f')
                upperInfo = datetime.datetime.strptime(endTimeInfo, '%Y:%m:%d-%H:%M:%S:%f')
                timeendTimeInfo = (upperInfo - lowerInfo).total_seconds()
                sheet.write(p, 1, timeendTimeInfo, style)
                newSheet.write(p, 0, p)
                newSheet.write(p, 1, timeendTimeInfo)
            else:
                startTimeInfo = newData[2]
                endTimeInfo = newData[-2]
                lowerInfo = datetime.datetime.strptime(startTimeInfo, '%Y:%m:%d-%H:%M:%S:%f')
                upperInfo = datetime.datetime.strptime(endTimeInfo, '%Y:%m:%d-%H:%M:%S:%f')
                timeendTimeInfo = (upperInfo - lowerInfo).total_seconds()
                sheet.write(p, 1, timeendTimeInfo, style)
                newSheet.write(p, 0, p)
                newSheet.write(p, 1, timeendTimeInfo)
            p += 1

        # 设置适合的列宽
        sheet.col(0).width = 22050
        sheet.col(1).width = 3000
        sheet.col(2).width = 3500
        sheet.col(3).width = 3500
        sheet.col(4).width = 3500
        sheet.col(5).width = 3500
        sheet.col(6).width = 3500
        sheet.col(7).width = 3500

        # 保存文件
        file = f'BlueOtaResult_{resultFilename}.xlsx'
        workbook.save(file)

        # Todo:生成散点图
        # data = xlrd.open_workbook(rf'./{file}')
        # table = data.sheets()[1]
        #
        # plt.figure(figsize=(9, 12))
        # plt.subplot(311)
        # plt.plot(data['测试序号'], y, 'ro')
        # plt.title('测试序号')
        # plt.grid()
        #
        # plt.tight_layout()
        # plt.show()


if __name__ == '__main__':
    getOtaLog(input('请输入log文件路径:'))
