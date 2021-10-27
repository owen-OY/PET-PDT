#!/usr/bin/evn python
# -*- coding:utf-8 -*-
import xlrd
import pandas as pd
import os
import re
import time
import sys

def get_filepath():
    filelist = []
    dir = os.getcwd()
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if name.split('.')[-1] == 'xls':
                filelist.append(name)
    if len(filelist) > 1:
        print('该目录下存在多个xls类型文件，请留其中一个')
        time.sleep(2)
        sys.exit()
    else:
        path = dir + '\\' + filelist[0]
        return path

def change_xlsx(path):
    df_list = pd.read_html(path)
    buglist = pd.ExcelWriter('buglist.xlsx')
    if len(df_list) > 1:
        df_list[1].to_excel(buglist)
    else:
        df_list[0].to_excel(buglist)
    buglist.close()

def count_data():
    book = xlrd.open_workbook('buglist.xlsx')
    sheet = book.sheet_by_index(0)
    onerow_list = sheet.row_values(rowx=0)
    onecol_list = sheet.col_values(colx=1)
    onecol_list_last = re.findall('.*?(Generated) at.*?', onecol_list[-1])
    # print(onecol_list_last)
    if len(onecol_list_last)>0:
        # bug总数
        bugsum = sheet.nrows - 2
    else:
        # bug总数
        bugsum = sheet.nrows - 1

    # print(onerow_list)
    for i in onerow_list:
        if i == 'Issue Type' or i == '问题类型':
            onerow_list = sheet.row_values(rowx=0)
            break
        else:
            onerow_list = sheet.row_values(rowx=1)
    # print(onerow_list)


    for x in onerow_list:
        if x == 'Issue Type':
            question_type_col = onerow_list.index('Issue Type')
        elif x == '问题类型':
            question_type_col = onerow_list.index('问题类型')
    for x in onerow_list:
        if x == 'Priority':
            priority_col = onerow_list.index('Priority')
        elif x == '优先级':
            priority_col = onerow_list.index('优先级')
    for x in onerow_list:
        if x == 'Status':
            state_col = onerow_list.index('Status')
        elif x == '状态':
            state_col = onerow_list.index('状态')

    question_type_list = sheet.col_values(colx=question_type_col)
    del question_type_list[0]
    priority_list = sheet.col_values(colx=priority_col)
    del priority_list[0]
    state_col_list = sheet.col_values(colx=state_col)
    del state_col_list[0]




    #P0bug总数
    P0index_list = []
    for ind,val in enumerate(priority_list):
        if val == 'P0':
            P0index_list.append(ind)
    P0sum = len(P0index_list)


    # P1bug总数
    P1index_list = []
    for ind,val in enumerate(priority_list):
        if val == 'P1':
            P1index_list.append(ind)
    P1sum = len(P1index_list)

    # P2bug总数
    P2index_list = []
    for ind,val in enumerate(priority_list):
        if val == 'P2':
            P2index_list.append(ind)
    P2sum = len(P2index_list)

    # 已解决bug总数
    solvedindex_list = []
    for ind,val in enumerate(state_col_list):
        if val =='已关闭' or val == 'Solved' or val == 'CLOSED(REJECT)' or val == 'Rejected' or val == 'Closed':
            solvedindex_list.append(ind)
    bugsolved = len(solvedindex_list)

    # 未解决bug总数
    unsolvedindex_list = []
    for ind,val in enumerate(state_col_list):
        if val =='New' or val == 'Accept/Processing' or val == 'Suspended':
            unsolvedindex_list.append(ind)

    # 固件bug总数
    gujianindex_list = []
    for ind,val in enumerate(question_type_list):
        if val =='嵌入式Bug':
            gujianindex_list.append(ind)

    # Androidbug总数
    Androidindex_list = []
    for ind,val in enumerate(question_type_list):
        if val =='Android APP Bug':
            Androidindex_list.append(ind)

    # iOSbug总数
    iosindex_list = []
    for ind,val in enumerate(question_type_list):
        if val =='IOS APP Bug':
            iosindex_list.append(ind)

    #总bug解决率
    bug_Resolution_rate = bugsolved/bugsum
    bug_Resolution_rate = '%.2f%%' % (bug_Resolution_rate * 100)

    #P0解决率
    P0solvedindex_list = list(set(P0index_list).intersection(set(solvedindex_list)))
    P0solvedsum = len(P0solvedindex_list)
    P0solved_rate = P0solvedsum/P0sum
    P0solved_rate = '%.2f%%' % (P0solved_rate * 100)


    #-----------------------------------固件------------------------------------------
    # 固件未解P0个数
    GinterunsolvedP0 = list(set(P0index_list).intersection(set(unsolvedindex_list)))
    gujianunsolvedP0 = len(list(set(GinterunsolvedP0).intersection(set(gujianindex_list))))

    # 固件未解P1个数
    GinterunsolvedP1 = list(set(P1index_list).intersection(set(unsolvedindex_list)))
    gujianunsolvedP1 = len(list(set(GinterunsolvedP1).intersection(set(gujianindex_list))))

    # 固件未解P2个数
    GinterunsolvedP2 = list(set(P2index_list).intersection(set(unsolvedindex_list)))
    gujianunsolvedP2 = len(list(set(GinterunsolvedP2).intersection(set(gujianindex_list))))

    #固件bug解决率
    Gintersolved = list(set(solvedindex_list).intersection(set(gujianindex_list)))
    gujiansolved_rate =len(Gintersolved)/len(gujianindex_list)
    gujiansolved_rate = '%.2f%%' % (gujiansolved_rate * 100)

    #固件P0bug解决率
    GintersolvedP0 = list(set(P0index_list).intersection(set(Gintersolved)))
    GinterP0 = list(set(P0index_list).intersection(set(gujianindex_list)))
    gujiansolved_rateP0 =len(GintersolvedP0)/(len(GinterP0))
    gujiansolved_rateP0 = '%.2f%%' % (gujiansolved_rateP0 * 100)


    # -----------------------------------Android------------------------------------------
    # Android未解P0个数
    AinterunsolvedP0 = list(set(P0index_list).intersection(set(unsolvedindex_list)))
    AndroidunsolvedP0 = len(list(set(AinterunsolvedP0).intersection(set(Androidindex_list))))

    # Android未解P1个数
    AinterunsolvedP1 = list(set(P1index_list).intersection(set(unsolvedindex_list)))
    AndroidunsolvedP1 = len(list(set(AinterunsolvedP1).intersection(set(Androidindex_list))))

    # Android未解P2个数
    AinterunsolvedP2 = list(set(P2index_list).intersection(set(unsolvedindex_list)))
    AndroidunsolvedP2 = len(list(set(AinterunsolvedP2).intersection(set(Androidindex_list))))

    #Androidbug解决率
    Aintersolved = list(set(solvedindex_list).intersection(set(Androidindex_list)))
    Androidsolved_rate =len(Aintersolved)/len(Androidindex_list)
    Androidsolved_rate = '%.2f%%' % (Androidsolved_rate * 100)

    #AndroidP0bug解决率
    AintersolvedP0 = list(set(P0index_list).intersection(set(Aintersolved)))
    AinterP0 = list(set(P0index_list).intersection(set(Androidindex_list)))
    Androidsolved_rateP0 =len(AintersolvedP0)/(len(AinterP0))
    Androidsolved_rateP0 = '%.2f%%' % (Androidsolved_rateP0 * 100)


    # -----------------------------------IOS------------------------------------------
    # iOS未解P0个数
    IinterunsolvedP0 = list(set(P0index_list).intersection(set(unsolvedindex_list)))
    iosunsolvedP0 = len(list(set(IinterunsolvedP0).intersection(set(iosindex_list))))

    # iOS未解P1个数
    IinterunsolvedP1 = list(set(P1index_list).intersection(set(unsolvedindex_list)))
    iosunsolvedP1 = len(list(set(IinterunsolvedP1).intersection(set(iosindex_list))))

    # iOS未解P2个数
    IinterunsolvedP2 = list(set(P2index_list).intersection(set(unsolvedindex_list)))
    iosunsolvedP2 = len(list(set(IinterunsolvedP2).intersection(set(iosindex_list))))

    #iOSbug解决率
    Iintersolved = list(set(solvedindex_list).intersection(set(iosindex_list)))
    iossolved_rate =len(Iintersolved)/len(iosindex_list)
    iossolved_rate = '%.2f%%' % (iossolved_rate * 100)

    #iOSP0bug解决率
    IintersolvedP0 = list(set(P0index_list).intersection(set(Iintersolved)))
    IinterP0 = list(set(P0index_list).intersection(set(iosindex_list)))
    iossolved_rateP0 =len(IintersolvedP0)/(len(IinterP0))
    iossolved_rateP0 = '%.2f%%' % (iossolved_rateP0 * 100)

    os.remove('buglist.xlsx')

    sum = f'bug总数：{bugsum}个，P0-{P0sum}个，P1-{P1sum}个，P2-{P2sum}个，整体bug解决率{bug_Resolution_rate}，整体P0bug解决率{P0solved_rate}'
    gujian = f'固件：未解P0-{gujianunsolvedP0}个，P1-{gujianunsolvedP1}个，P2-{gujianunsolvedP2}个，整体bug解决率{gujiansolved_rate}，整体P0bug解决率{gujiansolved_rateP0}'
    android = f'Android：未解P0-{AndroidunsolvedP0}个，P1-{AndroidunsolvedP1}个，P2-{AndroidunsolvedP2}个，整体bug解决率{Androidsolved_rate}，整体P0bug解决率{Androidsolved_rateP0}'
    ios = f'IOS：未解P0-{iosunsolvedP0}个，P1-{iosunsolvedP1}个，P2-{iosunsolvedP2}个，整体bug解决率{iossolved_rate}，整体P0bug解决率{iossolved_rateP0}'

    f = open('BUGcount.txt', 'w', encoding='utf8')
    f.write(f'{sum}\n{gujian}\n{android}\n{ios}')
    f.close()

if __name__ == '__main__':
    change_xlsx(get_filepath())
    count_data()

    
