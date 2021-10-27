import datetime
import os
import time
import xlwt
import re
from loguru import logger
# from src.P2P.P2P_camera import get_file_name

def get_file_name(file_dir):
    file_name, files_name = [], []
    for files in os.listdir(file_dir):
        # print(type(files))
        if '.log' in files:
            file = os.path.join(file_dir, files)
            # print(file)
            files_name.append(files)
            file_name.append(file)
    logger.info(file_name)
    # print(files_name)
    return file_name, file_dir, files_name

def re_none(fun, num=1):
    if fun == None or fun == '':
        data = "none"
    else:
        data = str(fun.group(num))
        # logger.info(data)
    return data

def total_time(start_time, last_time):
    # logger.info(start_time)
    # logger.info(last_time)
    lower = datetime.datetime.strptime(start_time, '%Y:%m:%d-%H:%M:%S:%f')
    upper = datetime.datetime.strptime(last_time, '%Y:%m:%d-%H:%M:%S:%f')
    total_times = (upper - lower).total_seconds()
    return total_times


def get_ota_log(file):
    ota_end_count= 0
    ota_download_success_count = 0
    ota_download_fail_count = 0
    start_time = '2020:01:01-00:00:00:000'
    ota_line = 0
    total_times = 0
    lines = 0
    ota_count_info = {}
    upgrade_fail_time, up_fail_time, down_fail_time, down_success_time = [], [], [], []
    ota_result_info = {}
    file_name = (file.rsplit('\\')[-1]).rsplit('.log')[0]
    if ".log" in file:
        # files_name = file
        # print(files_name)
        file = open(file, "r+", encoding='latin1')

        for line in file.readlines():
            #OTA开始
            if line.find('start download Wi-Fi OTA file') != -1:
                log_time = re.search(r"(\d{1,2}.\d{1,2}.\d{1,2}.\d{1,2}:\d{1,2}:\d{1,2}:\d{1,3})", line)
                # print(log_time)
                start_time = re_none(log_time)
                start_time = '20' + str(start_time)
                # print(start_time)
                total_times += 1
                ota_count_info[f'｜第{total_times}次ota开始时间'] = start_time
                if lines <= ota_line or ota_line == 0:
                    ota_line = lines

            #下载成功
            if line.find('Wi-Fi OTA file download success') != -1:
                log_time = re.search(r"(\d{1,2}.\d{1,2}.\d{1,2}.\d{1,2}:\d{1,2}:\d{1,2}:\d{1,3})", line)
                last_time = re_none(log_time)
                last_time = '20' + str(last_time)
                times = total_time(start_time, last_time)
                if ota_line > 0 and times <= 900:
                    log_time = str(log_time.group())
                    # logger.info(type(log_time))
                    down_success_time.append(log_time)
                    ota_count_info[f'第{total_times}次ota下载成功时间'] = last_time
                    ota_download_success_count += 1

            #下载失败
            if line.find('Wi-Fi OTA file download failed') != -1:
                log_time = re.search(r"(\d{1,2}.\d{1,2}.\d{1,2}.\d{1,2}:\d{1,2}:\d{1,2}:\d{1,3})", line)
                last_time = re_none(log_time)
                last_time = '20' + str(last_time)
                times = total_time(start_time, last_time)
                if ota_line > 0 and times <= 900:
                    log_time = str(log_time.group())
                    # logger.info(type(log_time))
                    down_fail_time.append(log_time)
                    ota_count_info[f'第{total_times}次ota下载失败时间'] = last_time
                    ota_download_fail_count += 1

            #OTA检验成功
            if line.find('iot_updata.csum OK') != -1:
                log_time = re.search(r"(\d{1,2}.\d{1,2}.\d{1,2}.\d{1,2}:\d{1,2}:\d{1,2}:\d{1,3})", line)
                last_time = re_none(log_time)
                last_time = '20' + str(last_time)
                times = total_time(start_time, last_time)
                if ota_line > 0 and times <= 900:
                    log_time = str(log_time.group())
                    # logger.info(type(log_time))
                    down_fail_time.append(log_time)
                    ota_count_info[f'第{total_times}次ota结束时间'] = last_time
                    ota_end_count += 1

            lines += 1
        if total_times == 0:
            logger.info('怎么搞的，升级一次没成功！！快让开发看看吧')
        else:
            success_rate = '%.2f%%' % ((ota_end_count / total_times) * 100)
            download_rate = '%.2f%%' % ((ota_download_success_count / total_times) * 100)
            ota_result_info['total_count'] = total_times  # ota总次数
            ota_result_info['start_count'] = total_times  # ota开始次数
            ota_result_info['download_success'] = ota_download_success_count  # ota下载成功
            ota_result_info['download_fail'] = ota_download_fail_count  # ota下载失败
            ota_result_info['end_count'] = ota_end_count  #ota结束次数
            ota_result_info['下载成功率'] = download_rate  # 下载成功率
            ota_result_info['升级成功率'] = success_rate  # 升级成功率
            logger.info(ota_count_info)
            logger.info(ota_result_info)
            logger.info('读取完成')
            str_ota_count_info = str(ota_count_info)
            list_ota_count_info = str_ota_count_info.split('｜')
            del list_ota_count_info[0]
            workbook = xlwt.Workbook(encoding='utf-8')
            sheet = workbook.add_sheet('ota_sheet')
            sheet.write(0,1, 'ota总次数')
            sheet.write(1,1,total_times)
            sheet.write(0,2, 'ota开始次数')
            sheet.write(1,2,total_times)
            sheet.write(0,3, 'ota结束次数')
            sheet.write(1,3,ota_end_count)
            sheet.write(0,4, 'ota成功率')
            sheet.write(1,4,success_rate)
            sheet.write(0,5, '下载成功次数')
            sheet.write(1,5,ota_download_success_count)
            sheet.write(0,6, '下载成功率')
            sheet.write(1,6,download_rate)

            r = 0
            for i in list_ota_count_info:
                sheet.write(r, 0, i)
                r+=1
            workbook.save(file_name + '.xlsx')
if __name__ == '__main__':
    log_f = input('请输入log文件路径:')
    # log_f = r'C:\Users\anker\Downloads\serial_serial-cu.slab_usbtouart19-2021-10-18_211508.log '
    log_f = log_f.rsplit()[0]
    get_ota_log(log_f)    
