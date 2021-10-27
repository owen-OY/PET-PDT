# -*- coding:utf-8  -*-
import xlwt
import re
import time
import xlrd

# 防止空数据
def re_none(fun, num=0):
    if fun == None:
        data = 'None'
    else:
        data = fun.group(num)
    return data

def get_sound_time(log_file):
    f = open(log_file, 'r', encoding='latin1')
    times_list = []
    for line in f:
        if line.find('sound confidence') != -1:
            times = re.search(r"(\d{1,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", line)
            times = re_none(times, 1)
            times = int(time.mktime(time.strptime(times, "%Y-%m-%d %H:%M:%S")))
            times_list.append(times)
    return times_list
    # workbook = xlwt.Workbook(encoding='utf-8')
    # sheet = workbook.add_sheet('stream_sheet',cell_overwrite_ok=True)
    # sheet.write(0, 0, 'time_info')
    # sheet.write(0, 1, 'count')
    # sheet.write(0, 3, 'sum_count')
    # sheet.write(0, 4, 'min_avg')
    # sheet_line = 1
    # keys = ''
    # values = 0
    # dict = {keys: values}
    # for i in times_list:
    #     if keys == '':
    #         keys = i
    #         values += 1
    #         dict.clear()
    #         dict = {keys: values}
    #         sheet.write(1, 0, keys)
    #         sheet.write(1, 1, values)
    #     elif i not in dict.keys():
    #         sheet_line += 1
    #         keys = i
    #         values = 1
    #         dict.clear()
    #         dict = {keys: values}
    #         sheet.write(sheet_line, 0, keys)
    #         sheet.write(sheet_line,1,values)
    #     elif i in dict.keys():
    #         values += 1
    #         dict[keys] = values
    #         sheet.write(sheet_line,1,values)
    # sum_count = len(times_list)
    # min_count =  len(list(set(times_list)))
    # min_avg = sum_count/min_count
    # sheet.write(1, 3,sum_count)
    # sheet.write(1, 4, min_avg)
    #
    #
    #
    # f.close()
    # file_name = os.path.splitext(os.path.basename(log_file))[0]
    # workbook.save('{}.xlsx'.format(file_name))

def get_csv_time(csv_file):
    book = xlrd.open_workbook(csv_file)
    sheet = book.sheet_by_index(0)
    onerow_list = sheet.row_values(rowx=0)
    start_time = onerow_list.index('开始时间')
    end_time = onerow_list.index('停止时间')
    noise_file = onerow_list.index('噪音文件')
    sound_file = onerow_list.index('声源样本')

    start_time_list = sheet.col_values(colx=start_time)
    del start_time_list[0]
    start_timestamp_list = []
    for i in start_time_list:
        start_timestamp = int(time.mktime(time.strptime(i, "%Y-%m-%d %H:%M:%S")))
        start_timestamp_list.append(start_timestamp)

    end_time_list = sheet.col_values(colx=end_time)
    del end_time_list[0]
    end_timestamp_list = []
    for j in end_time_list:
        end_timestamp = int(time.mktime(time.strptime(j, "%Y-%m-%d %H:%M:%S")))
        end_timestamp_list.append(end_timestamp)

    noise_file_list = sheet.col_values(colx=noise_file)
    del noise_file_list[0]


    sound_file_list = sheet.col_values(colx=sound_file)
    del sound_file_list[0]

    return start_timestamp_list,end_timestamp_list,noise_file_list,sound_file_list

def count_date(times_list,start_timestamp_list,end_timestamp_list,noise_file_list,sound_file_list):
    start_timestamp_list_len = len(start_timestamp_list)
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('stream_sheet',cell_overwrite_ok=True)
    sheet.write(0, 0, '测试序号')
    sheet.write(0, 1, '检测次数')
    sheet.write(0, 2, '噪音文件')
    sheet.write(0, 3, '声源样本')
    sheet_line = 1
    for x in range(start_timestamp_list_len):
        count_list = []
        for i in times_list:
            if start_timestamp_list[x] <= i and i <= end_timestamp_list[x]:
                count_list.append(i)
            else:
                pass
        if len(count_list)>0:
            sheet.write(sheet_line,0,x+1)
            sheet.write(sheet_line,1,len(count_list))
            sheet.write(sheet_line,2,noise_file_list[x])
            sheet.write(sheet_line,3,sound_file_list[x])
            sheet_line+=1
        else:
            pass
    workbook.save('dogsound.xlsx')


if __name__ == '__main__':
    log_file = input('请输入狗叫声log文件路径:')
    csv_file = input('请输入狗叫声结果csv文件路径:')
    get_sound_time = get_sound_time(log_file)
    start_timestamp_list,end_timestamp_list,noise_file_list,sound_file_list = get_csv_time(csv_file)
    count_date(get_sound_time,start_timestamp_list,end_timestamp_list,noise_file_list,sound_file_list)
    print('执行完成')
