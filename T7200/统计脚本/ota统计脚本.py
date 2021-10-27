      
import datetime
import os
import time
import re
from loguru import logger
import xlwt
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
    # logger.info(file_name)
    return file_name, file_dir, files_name

def re_none(fun, num=1):
    if fun == None or fun == '':
        data = "19:52:13"
    else:
        data = str(fun.group(num))
        # logger.info(data)
    return data


def total_time(start_time, last_time):
    # logger.info(start_time)
    # logger.info(last_time)
    lower = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    upper = datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
    total_times = (upper - lower).total_seconds()
    return total_times


def get_ota_log(file):
    down_fail_count, down_finish_count, upgrade_success, upgrade_fial, up_success, up_fail, up_fail_coint = 0, 0, 0, 0, 0, 0, 0
    start_time = '2020-01-01 00:00:05'
    last_time = ''
    ota_line = 0
    total_times = 0
    lines = 0
    version = ''
    ota_count_info = {}
    upgrade_fail_time, up_fail_time, down_fail_time = [], [], []
    ota_result_info = {}
    if ".log" in file:
        files_name = file
        file = open(file, "r+", encoding='latin1')

        for line in file.readlines():
            if line.find('get T7200_ota upgrade version info start') != -1:
                log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", line)
                # log_time = re.search(r"(\d{1,2}:\d{1,2}:\d{1,2})", line)
                start_time = re_none(log_time)
                start_time = '20' + str(start_time)
                total_times += 1
                ota_count_info[f'｜第{total_times}次ota时间'] = start_time
                up_fail_count = 0
                if lines <= ota_line or ota_line == 0:
                    ota_line = lines

            if line.find('main_sw_version : ') != -1:
                version = re.search(r'main_sw_version : (.*?\n)', line)
                version = str(version.group(1))

            if line.find('OTA task:all package has download success') != -1:  # ota包下载成功
                log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d+.\d+)", line)
                log_time = re.search(r"(\d{1,2}:\d{1,2}:\d{1,2})", line)
                last_time = re_none(log_time)
                last_time = '2021-06-05 ' + str(last_time)
                times = total_time(start_time, last_time)
                if ota_line > 0 and times <= 900:
                    down_finish_count += 1

            if line.find('OTA task:package has download fail') != -1:  # ota包下载失败

                log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", line)
                # log_time = re.search(r"(\d{1,2}:\d{1,2}:\d{1,2})", line)
                last_time = re_none(log_time)
                last_time = '20' + str(last_time)
                times = total_time(start_time, last_time)
                if ota_line > 0 and times <= 900:
                    log_time = str(log_time.group())
                    # logger.info(type(log_time))
                    down_fail_time.append(log_time)
                    down_fail_count += 1

            if line.find('OTA task:upgrade final result is success') != -1:  # ota上报信息成功

                log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", line)
                # log_time = re.search(r"(\d{1,2}:\d{1,2}:\d{1,2})", line)
                last_time = re_none(log_time)
                last_time = '20' + str(last_time)
                times = total_time(start_time, last_time)
                if ota_line > 0 and times <= 900:
                    up_success += 1
                    ota_count_info[f'第{total_times}次ota上报成功时间'] = last_time

            if line.find('OTA task:upgrade final result is fail') != -1:  # ota上报信息失败
                log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", line)
                # log_time = re.search(r"(\d{1,2}:\d{1,2}:\d{1,2})", line)
                last_time = re_none(log_time)
                last_time = '20' + str(last_time)
                times = total_time(start_time, last_time)
                if ota_line > 0 and times <= 900:
                    log_time = str(log_time.group())
                    up_fail_time.append(log_time)
                    up_fail += 1
                    up_fail_count += 1
                    ota_count_info[f'第{total_times}次ota上报失败次数'] = up_fail

            # if line.find('OTA task:p2p notify last') != -1:
            #     # log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d+.\d+)", line)
            #     log_time = re.search(r"(\d{1,2}:\d{1,2}:\d{1,2})", line)
            #     last_time = re_none(log_time)
            #     last_time = '21-06-05 ' + str(last_time)
            #     times = total_time(start_time, last_time)
            #     if ota_line > 0 and times <= 900:
            #         continue

            if line.find('OTA task:upgrade final result is success') != -1:  # ota擦写成功
                # log_time = re.search(r"(\d{1,2}:\d{1,2}:\d{1,2})", line)
                log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", line)
                last_time = re_none(log_time)
                last_time = '20' + str(last_time)
                times = total_time(start_time, last_time)
                if ota_line > 0 and times <= 900:
                    upgrade_success += 1

            if line.find('OTA task:upgrade final result is fail') != -1: # ota擦写失败次数
                log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", line)
                # log_time = re.search(r"(\d{1,2}:\d{1,2}:\d{1,2})", line)
                last_time = re_none(log_time)
                last_time = '20' + str(last_time)
                times = total_time(start_time, last_time)
                if ota_line > 0 and times <= 900:
                    log_time = str(log_time.group())
                    upgrade_fail_time.append(log_time)
                    upgrade_fial += 1

            lines += 1

        ota_result_info['total_times'] = total_times  # ota总初始化次数
        ota_result_info['ota_line'] = ota_line  # ota开始行数
        ota_result_info['down_finish_count'] = down_finish_count  # ota包下载成功次数
        ota_result_info['down_fail_time'] = down_fail_time  # ota包下载失败时间
        ota_result_info['down_fail_count'] = down_fail_count  # ota包下载失败次数
        ota_result_info['up_success'] = up_success  # ota上报成功次数
        ota_result_info['up_fail_time'] = up_fail_time  # ota上报失败时间
        ota_result_info['up_fail'] = up_fail  # ota上报失败次数
        ota_result_info['upgrade_success'] = upgrade_success  # ota升级成功次数
        ota_result_info['upgrade_fail'] = upgrade_fial  # ota擦写失败次数
        ota_result_info['upgrade_fail_time'] = upgrade_fail_time  # ota擦写失败时间
        ota_result_info['version'] = version  # ota版本
        # logger.info(ota_result_info['down_finish_count'])
        # logger.info(ota_result_info['down_fail_time'])
        # logger.info(ota_result_info['down_fail_count'])
        # logger.info(ota_result_info['up_success'])
        # logger.info(ota_result_info['up_fail_time'])
        # logger.info(ota_result_info['up_fail'])
        # logger.info(ota_result_info['upgrade_success'])
        logger.info(ota_count_info)
        logger.info(ota_result_info)
        logger.info('读取完成')
        str_ota_count_info = str(ota_count_info)
        list_ota_count_info = str_ota_count_info.split('｜')
        del list_ota_count_info[0]
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet = workbook.add_sheet('ota_sheet')
        sheet.write(0,1, 'ota总次数')
        sheet.write(1,1,ota_result_info['total_times'])
        sheet.write(0,2, '下载失败次数')
        sheet.write(1,2,ota_result_info['down_fail_count'])
        sheet.write(0,3, '上报成功次数')
        sheet.write(1,3,ota_result_info['up_success'])
        sheet.write(0,4, '上报失败次数')
        sheet.write(1,4,ota_result_info['total_times']-ota_result_info['up_success'])
        sheet.write(0,5, '升级成功次数')
        sheet.write(1,5,ota_result_info['upgrade_success'])
        sheet.write(0,6, '升级失败次数')
        sheet.write(1,6,ota_result_info['upgrade_fail'])
        sheet.write(0,7, '上报成功率')
        sheet.write(1,7,'%.2f%%' % (ota_result_info['up_success']/ota_result_info['total_times'] * 100))
        sheet.write(0,8, '升级成功率')
        sheet.write(1,8,'%.2f%%' % (ota_result_info['upgrade_success']/ota_result_info['up_success'] * 100))
        sheet.write(0,9, '升级版本')
        sheet.write(1,9,ota_result_info['version'])
        r = 0
        for i in list_ota_count_info:
            sheet.write(r, 0, i)
            r+=1
        workbook.save('ota.xlsx')
        # return ota_count_info,ota_result_info

    else:
        file_name, file_dir, files_name = get_file_name(file)
        for i in range(len(file_name)):
            logger.info(file_name[i])
            f = file_name[i]
            file = open(f, "r+", encoding='latin1')

            for line in file.readlines():
                if line.find('get T7200_ota upgrade version info start') != -1:
                    log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", line)
                    # log_time = re.search(r"(\d{1,2}:\d{1,2}:\d)", line)
                    start_time = re_none(log_time)
                    start_time = '20' + str(start_time)
                    total_times += 1
                    if lines <= ota_line or ota_line == 0:
                        ota_line = lines

                if line.find('main_sw_version : ') != -1:
                    version = re.search(r'main_sw_version : (.*?\n)', line)
                    version = str(version.group(1))
                #
                # if line.find('OTA task:all package has download success') != -1:  # ota包下载成功
                #     # log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d+.\d+)", line)
                #     log_time = re.search(r"(\d{1,2}:\d{1,2}:\d)", line)
                #     last_time = re_none(log_time)
                #     last_time = '21 ' + str(last_time)
                #     times = total_time(start_time, last_time)
                #     if ota_line > 0 and times <= 900:
                #         down_finish_count += 1

                if line.find('OTA task:package has download fail') != -1:  # ota包下载失败

                    log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", line)
                    # log_time = re.search(r"(\d{1,2}:\d{1,2}:\d)", line)
                    last_time = re_none(log_time)
                    last_time = '20' + str(last_time)
                    times = total_time(start_time, last_time)
                    if ota_line > 0 and times <= 900:
                        log_time = str(log_time.group())
                        # logger.info(type(log_time))
                        down_fail_time.append(log_time)
                        down_fail_count += 1

                if line.find('OTA task:upgrade final result is success') != -1:  # ota上报信息成功

                    log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", line)
                    # log_time = re.search(r"(\d{1,2}:\d{1,2}:\d)", line)
                    last_time = re_none(log_time)
                    last_time = '20' + str(last_time)
                    times = total_time(start_time, last_time)
                    if ota_line > 0 and times <= 900:
                        up_success += 1

                if line.find('OTA task:upgrade final result is fail') != -1:  # ota上报信息失败
                    log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", line)
                    # log_time = re.search(r"(\d{1,2}:\d{1,2}:\d)", line)
                    last_time = re_none(log_time)
                    last_time = '20' + str(last_time)
                    times = total_time(start_time, last_time)
                    if ota_line > 0 and times <= 900:
                        log_time = str(log_time.group())
                        up_fail_time.append(log_time)
                        up_fail += 1
                if line.find('OTA task:p2p notify last') != -1:
                    log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", line)
                    # log_time = re.search(r"(\d{1,2}:\d{1,2}:\d)", line)
                    last_time = re_none(log_time)
                    last_time = '20' + str(last_time)
                    if start_time == '':
                        start_time = re_none(start_time)
                        start_time = '20' + start_time
                    times = total_time(start_time, last_time)
                    if ota_line > 0 and times <= 900:
                        continue

                if line.find('OTA task:total size 4,done size 4') != -1:  # ota擦写成功
                    log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", line)
                    # log_time = re.search(r"(\d{1,2}:\d{1,2}:\d)", line)
                    last_time = re_none(log_time)
                    last_time = '20' + str(last_time)
                    if start_time == '':
                        start_time = re_none(start_time)
                        start_time = '20' + start_time
                    times = total_time(start_time, last_time)
                    if ota_line > 0 and times <= 900:
                        upgrade_success += 1

                if line.find('OTA task:upgrade final result is fail') != -1: # ota擦写失败次数
                    log_time = re.search(r"(\d{1,2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", line)
                    # log_time = re.search(r"(\d{1,2}:\d{1,2}:\d)", line)
                    last_time = re_none(log_time)
                    last_time = '20' + str(last_time)
                    times = total_time(start_time, last_time)
                    if ota_line > 0 and times <= 900:
                        log_time = str(log_time.group())
                        upgrade_fail_time.append(log_time)
                        upgrade_fial += 1
                lines += 1

            ota_result_info['total_times'] = total_times  # ota总初始化次数
            ota_result_info['ota_line'] = ota_line  # ota开始行数
            # ota_result_info['down_finish_count'] = down_finish_count  # ota包下载成功次数
            ota_result_info['down_fail_time'] = down_fail_time  # ota包下载失败时间
            ota_result_info['down_fail_count'] = down_fail_count  # ota包下载失败次数
            ota_result_info['up_success'] = up_success  # ota上报成功次数
            ota_result_info['up_fail_time'] = up_fail_time  # ota上报失败时间
            ota_result_info['up_fail'] = up_fail  # ota上报失败次数
            ota_result_info['upgrade_success'] = upgrade_success  # ota升级成功次数
            ota_result_info['upgrade_fail'] = upgrade_fial  # ota擦写失败次数
            ota_result_info['upgrade_fail_time'] = upgrade_fail_time  # ota擦写失败时间
            ota_result_info['version'] = version  # ota版本
            # logger.info(ota_result_info['down_finish_count'])
            # logger.info(ota_result_info['down_fail_time'])
            # logger.info(ota_result_info['down_fail_count'])
            # logger.info(ota_result_info['up_success'])
            # logger.info(ota_result_info['up_fail_time'])
            # logger.info(ota_result_info['up_fail'])
            # logger.info(ota_result_info['upgrade_success'])
            logger.info(ota_result_info)
            logger.info(ota_count_info)
            logger.info('读取完成')
            str_ota_count_info = str(ota_count_info)
            list_ota_count_info = str_ota_count_info.split('｜')
            del list_ota_count_info[0]
            workbook = xlwt.Workbook(encoding='utf-8')
            sheet = workbook.add_sheet('ota_sheet')
            sheet.write(0, 1, 'ota总次数')
            sheet.write(1, 1, ota_result_info['total_times'])
            sheet.write(0, 2, '下载失败次数')
            sheet.write(1, 2, ota_result_info['down_fail_count'])
            sheet.write(0, 3, '上报成功次数')
            sheet.write(1, 3, ota_result_info['up_success'])
            sheet.write(0, 4, '上报失败次数')
            sheet.write(1, 4, ota_result_info['total_times'] - ota_result_info['up_success'])
            sheet.write(0, 5, '升级成功次数')
            sheet.write(1, 5, ota_result_info['upgrade_success'])
            sheet.write(0, 6, '升级失败次数')
            sheet.write(1, 6, ota_result_info['upgrade_fail'])
            sheet.write(0, 7, '上报成功率')
            sheet.write(1, 7, '%.2f%%' % (ota_result_info['up_success'] / ota_result_info['total_times'] * 100))
            sheet.write(0, 8, '升级成功率')
            sheet.write(1, 8, '%.2f%%' % (ota_result_info['upgrade_success'] / ota_result_info['up_success'] * 100))
            sheet.write(0, 9, '升级版本')
            sheet.write(1, 9, ota_result_info['version'])
            r = 0
            for i in list_ota_count_info:
                sheet.write(r, 0, i)
                r += 1
            workbook.save('ota_count.xlsx')
            # return ota_count_info,ota_result_info




if __name__ == '__main__':
    log_f = input('请输入log文件路径:')
    # log_f = r'C:\Users\anker\Desktop\ota\COM3_20210914_213404.log'
    get_ota_log(log_f)

    
