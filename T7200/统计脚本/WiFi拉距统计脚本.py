# _*_ coding:utf-8 _*_

# @Time     : 2021/3/29
# @Author   : mancheng
# @File     : T7200_log_wifi_info.py

import xlwt
import re
import os
from numpy import *


# 防止空数据
def re_none(fun, num=0):
    if fun == None:
        data = 'None'
    else:
        data = fun.group(num)
    return data

def floodlight_info(log_file):
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('stream_sheet')
    sheet.write(0, 0, 'time_info')
    sheet.write(0, 1, 'V_FR')
    sheet.write(0, 2, 'A_FR')
    sheet.write(0, 3, 'P2P_buf')
    sheet.write(0, 4, 'up_speed')
    sheet.write(0, 5, 'time_info')
    sheet.write(0, 6, 'rssi')
    sheet.write(0, 8, 'rssi')
    sheet.write(0,9,'V_FR')
    sheet.write(0,10,'A_FR')
    sheet.write(0,11,'P2P_buf')
    sheet.write(0,12,'up_speed')
    sheet_line,rssi_line = 0,0
    f = open(log_file, 'r', encoding='latin1')
    V_FR_list = []
    A_FR_list = []
    P2P_buf_list = []
    up_speed_list = []
    rssi_list = []
    for line in f:
        if line.find('P2P_MediaWrite:322') != -1:
            sheet_line += 1
            time = re.search(r"(\d{1,2}:\d{1,2}:\d+.\d+)", line)
            time = re_none(time, 1)
            sheet.write(sheet_line, 0, time)

            V_FR = re.search('V_FR: (.*?)F/s', line)
            V_FR = re_none(V_FR, 1)
            V_FR_list.append(int(V_FR))
            sheet.write(sheet_line, 1, V_FR)

            A_FR = re.search('A_FR:(.*?)F/s', line)
            A_FR = re_none(A_FR, 1)
            A_FR_list.append(int(A_FR))
            sheet.write(sheet_line, 2, A_FR)

            P2P_buf = re.search('P2P_buf: (.*?)KB', line)
            P2P_buf = re_none(P2P_buf, 1)
            P2P_buf_list.append(int(P2P_buf))
            sheet.write(sheet_line, 3, P2P_buf)

            up_speed = re.search('up_speed: (.*?)KB/s', line)
            up_speed = re_none(up_speed, 1)
            up_speed_list.append(int(up_speed))
            sheet.write(sheet_line, 4, up_speed)

        if line.find('wifi_io_ctrl.c:wl_get_rssi') != -1:
            rssi_line += 1
            time = re.search(r"(\d{1,2}:\d{1,2}:\d+.\d+)", line)
            time = re_none(time, 1)
            sheet.write(rssi_line, 5, time)

            rssi = re.search('wl_get_rssi, rssi = (.*?)\n', line)
            rssi = re_none(rssi, 1)
            rssi_list.append(int(rssi))
            sheet.write(rssi_line, 6, rssi)

    rssi_AVG = mean(rssi_list)
    V_FR_AVG = mean(V_FR_list)
    A_FR_AVG = mean(A_FR_list)
    P2P_buf_AVG = mean(P2P_buf_list)
    up_speed_AVG = mean(up_speed_list)
    sheet.write(1, 8, rssi_AVG)
    sheet.write(1, 9, V_FR_AVG)
    sheet.write(1, 10, A_FR_AVG)
    sheet.write(1, 11, P2P_buf_AVG)
    sheet.write(1, 12, up_speed_AVG)
    f.close()
    file_name = os.path.splitext(os.path.basename(log_file))[0]
    workbook.save('{}.xlsx'.format(file_name))

if __name__ == '__main__':
    log_f = input('请输入log文件路径：')
    # log_f = r'C:\Users\anker\Downloads\T7200第三轮WiFi拉距0727_log\T7200P102128004C_1号设备\10_1\1号_10_1_1.log'
    floodlight_info(log_f)
    print('执行完成')   
