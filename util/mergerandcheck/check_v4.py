import numpy as np
import pandas as pd
import csv
import os
from pandas import DataFrame
from array import array
import math
import time
import datetime
from xlrd import xldate_as_tuple
import platform
import newname
import MergeData_Check as check

is_null_data=[]
is_error_data=[]
colums=['序号','统计级别','数据起始时间','数据结束时间','国家','省份','城市','区县','新增确诊人数','新增疑似人数','新增治愈人数','新增死亡人数','累计确诊人数','累计疑似人数','累计治愈人数','累计死亡人数','核减人数','累计核减人数','数据源','数据发布时间','数据源文本','数据源链接','数据间接发布时间','数据间接发布来源','数据间接发布来源链接','数据收集时间','数据收集方式','数据收集人员/程序姓名','数据是否核查','数据首次核查时间','数据首次核查方式','数据首次核查人员/程序姓名','数据首次核查状态','更正人员','更正时间','数据再次核查时间','数据再次核查方式','数据再次核查人员/程序姓名','数据再次核查状态','备注']
daily_data=['新增确诊人数','新增疑似人数','新增治愈人数','新增死亡人数','累计确诊人数','累计疑似人数','累计治愈人数','累计死亡人数','核减人数','累计核减人数']
old_colums=['公开时间','类别','省份','城市','新增确诊病例','新增治愈出院数','新增死亡数','核减','治愈核减','死亡核减','累计确诊人数','累计治愈人数','累计死亡人数']

time_today=datetime.datetime.now().strftime('%Y%m%d')
time_Nowhour=datetime.datetime.now().strftime('%H-%M-%S')
time_yesterday=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y%m%d')
outputfile='MergeData_'+time_today+'_'+time_Nowhour+'.csv'
log_file='log_'+time_today+'.txt'
log_yes_file='log_'+time_yesterday+'.txt'
completed_file='completed_'+time_today+'.txt'
yes_completed_file='completed_'+time_yesterday+'.txt'
Completed=[]

def check_error_data(data):
    re_value=0
    data_shape=data.shape[0]
    province_daily_data=[0,0,0,0,0,0,0,0,0,0]
    province_total_data=[0,0,0,0,0,0,0,0,0,0]
    for row in range(0,data_shape):
        temp_data=data.iloc[row,:].copy()
        if temp_data[1]=='省级' or temp_data[1]=='国家级':

            for i in range(0,10):
                if temp_data[daily_data[i]]!=temp_data[daily_data[i]]:
                    temp_data.loc[daily_data[i]]=0
            
            province_total_data[0]=int(temp_data[daily_data[0]])
            province_total_data[1]=int(temp_data[daily_data[1]])
            province_total_data[2]=int(temp_data[daily_data[2]])
            province_total_data[3]=int(temp_data[daily_data[3]])
            province_total_data[4]=int(temp_data[daily_data[4]])
            province_total_data[5]=int(temp_data[daily_data[5]])
            province_total_data[6]=int(temp_data[daily_data[6]])
            province_total_data[7]=int(temp_data[daily_data[7]])
            province_total_data[8]=int(temp_data[daily_data[8]])
            province_total_data[9]=int(temp_data[daily_data[9]])
        elif temp_data['统计级别']=='城市级':

            for i in range(0,10):
                if temp_data[daily_data[i]]!=temp_data[daily_data[i]]:
                    temp_data.loc[daily_data[i]]=0
                    
            province_daily_data[0]+=int(temp_data[daily_data[0]])
            province_daily_data[1]+=int(temp_data[daily_data[1]])
            province_daily_data[2]+=int(temp_data[daily_data[2]])
            province_daily_data[3]+=int(temp_data[daily_data[3]])
            province_daily_data[4]+=int(temp_data[daily_data[4]])
            province_daily_data[5]+=int(temp_data[daily_data[5]])
            province_daily_data[6]+=int(temp_data[daily_data[6]])
            province_daily_data[7]+=int(temp_data[daily_data[7]])
            province_daily_data[8]+=int(temp_data[daily_data[8]])
            province_daily_data[9]+=int(temp_data[daily_data[9]])

    for i in range(0,10):
        current_value=province_total_data[i]-province_daily_data[i]
        if current_value!=0:
            if data_shape==1:
                break
            out_info='{} 起始{}结束{}的数据{}为{}，地区累计数据为{}'.format(temp_data[5],temp_data[2],temp_data[3],daily_data[i],province_total_data[i],province_daily_data[i])
            #print(out_info)
            is_error_data.append(out_info)
            re_value=1

    #print(is_error_data)
    #print(province_daily_data,province_total_data)
    return re_value

def check_null_data(data):
    data_shape=data.shape[0]
    for row in range(0,data_shape):
        temp_data=data.iloc[row,:]
        nan_result=temp_data.isnull().values.any()
        nan_value=temp_data.isna().sum()
        if nan_result==True:
            if temp_data[39]=='' and nan_value==1:
                continue
            if temp_data[1]=='省级':

                if np.isnan(temp_data[7]):
                    if isinstance(temp_data[6],float):
                        nan_value-=3
                        out_info='第{}行 {}有{}处未填数据'.format(row+2,temp_data[5],nan_value)
                    else:
                        nan_value-=2
                        #省级地区数据中“区县”、“备注”可留空
                        out_info='第{}行 {}{}有未填{}处未填数据'.format(row+2,temp_data[5],temp_data[6],nan_value)
                is_null_data.append(out_info)
    return 0

def entoch(charter,province):
    ch_result=''
    if '甘肃' in province:
        days_2=[4,6,9,11]
        month=charter.month
        day=charter.day
        day=day+1
        
        if day==32:
            month=str(1+month)
            day=1
        elif day==31:
            if month in days_2:
                month=str(1+month)
                day=1
        elif day==30:
            if month==2:
                month=str(1+month)
                day=1
        
        ch_result=str(month)+'月'+str(day)+'日'
        #print(ch_result)
    else:
        ch_result=str(charter.month)+'月'+str(charter.day)+'日'
    return ch_result

def exchangetooldcol(data):
    #确诊时间,类别,省份,城市,新增确诊病例,新增治愈出院数,新增死亡数,核减
    judge_type=data.columns.values.tolist()[0]
    if judge_type != '序号':
        judge_data=data.copy()
        out_info='{}文件格式存在问题'.format(judge_data.iloc[2,5])
        #print(out_info)
        is_error_data.append(out_info)
        return 1
    daily={}
    Diagnosed_time=[]
    start_time=[]
    end_time=[]
    type=[]
    province=[]
    city=[]
    in_diagnosed=[]
    in_cure=[]
    in_die=[]
    in_check=[]
    sum_diag=[]
    sum_cure=[]
    sum_die=[]
    cure_check=[]
    die_check=[]
    data_1=''
    data_check_1=''
    data_check_2=''
    data_2=''
    data_3=''
    data_4=''
    data_5=''
    data_6=''
    data_7=''
    data_8=''
    data_9=''
    data_10=''
    data_11=''
    data_xinjiang=[0,0,0,0,0,0,0,0,0,0]
    data_shape=data.shape[0]
    for row in range(0,data_shape):
        temp_data=data.iloc[row,:].copy()
        if temp_data[1]=='省级' or temp_data[1]=='国家级':
            for i in range(5,23):
                if temp_data[colums[i-5]]!=temp_data[colums[i-5]]:
                    temp_data.loc[colums[i-5]]=''

            date=''
            temp_date=str(temp_data[colums[2]])
            if '/' in temp_date:
                try: 
                    date=datetime.datetime.strptime(temp_date.split('\r')[0],'%Y/%m/%d %H:%M:%S')
                except Exception as e:
                    date=datetime.datetime.strptime(temp_date.split('\r')[0],'%Y/%m/%d')
            else:
                try: 
                    date=datetime.datetime.strptime(temp_date.split('\r')[0],'%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    date=datetime.datetime.strptime(temp_date.split('\r')[0],'%Y-%m-%d')
            date=entoch(date,temp_data['省份'])

            if temp_data[1]=='省级':
                temp_data.loc['省份']=newname.get_pure_province_name(temp_data['省份'])
            
            if '新疆' in temp_data['省份']:
                #temp_data.loc['省份']=newname.get_pure_province_name(temp_data['省份'])
                for i in range(0,10):
                    #if temp_data[daily_data[i]]!=temp_data[daily_data[i]]:
                    if temp_data[daily_data[i]]=='':
                        temp_data.loc[daily_data[i]]=0
                for count in range(0,10):
                    data_xinjiang[count]+=int(temp_data[daily_data[count]])
                for count_ in range(0,10):
                    temp_data.loc[daily_data[count_]]=data_xinjiang[count_] 

            data_1=date
            #data_time_1=str(temp_data[colums[2]])
            #data_time_2=str(temp_data[colums[3]])
            data_2=str(temp_data[colums[1]])
            data_3=str(temp_data[colums[5]])
            data_5=str(temp_data[daily_data[0]])
            data_6=str(temp_data[daily_data[2]])
            data_7=str(temp_data[daily_data[3]])
            data_8=str(temp_data[daily_data[8]])
            data_9=str(temp_data[colums[12]])
            data_10=str(temp_data['累计治愈人数'])
            data_11=str(temp_data['累计死亡人数'])
            data_check_1=''
            data_check_2=''

        elif temp_data['统计级别']=='城市级':
            
            for i in range(0,18):
                if temp_data[colums[i]]!=temp_data[colums[i]]:
                    temp_data.loc[colums[i]]=''  
            
            temp_data.loc['统计级别']='地区级'
            temp_data.loc['省份']=newname.get_pure_province_name(temp_data['省份'])
            temp_data.loc['城市']=newname.get_pure_city_name(temp_data['城市'])
            date=''
            temp_date=str(temp_data[colums[2]])
            if '/' in temp_date:
                try: 
                    date=datetime.datetime.strptime(temp_date.split('\r')[0],'%Y/%m/%d %H:%M:%S')
                except Exception as e:
                    date=datetime.datetime.strptime(temp_date.split('\r')[0],'%Y/%m/%d')
            else:
                try: 
                    date=datetime.datetime.strptime(temp_date.split('\r')[0],'%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    date=datetime.datetime.strptime(temp_date.split('\r')[0],'%Y-%m-%d')
            date=entoch(date,temp_data['省份'])

            #start_time.append(str(temp_data[colums[2]]))
            #end_time.append(str(temp_data[colums[3]]))
            Diagnosed_time.append(date)
            type.append(str(temp_data[colums[1]]))
            province.append(str(temp_data[colums[5]]))
            city.append(str(temp_data[colums[6]]))
            in_diagnosed.append(str(temp_data[daily_data[0]]))
            in_cure.append(str(temp_data[daily_data[2]]))
            in_die.append(str(temp_data[daily_data[3]]))
            in_check.append(str(temp_data[daily_data[8]]))
            sum_diag.append(str(temp_data[colums[12]]))
            sum_cure.append(str(temp_data['累计治愈人数']))
            sum_die.append(str(temp_data['累计死亡人数']))
            cure_check.append('')
            die_check.append('')

    Diagnosed_time.append(data_1)
    #start_time.append(data_time_1)
    #nd_time.append(data_time_2)
    type.append(data_2)
    province.append(data_3)
    city.append(data_4)
    in_diagnosed.append(data_5)
    in_cure.append(data_6)
    in_die.append(data_7)
    in_check.append(data_8)
    sum_diag.append(data_9)
    sum_cure.append(data_10)
    sum_die.append(data_11)
    cure_check.append(data_check_1)
    die_check.append(data_check_2)

    daily={
        '公开时间':Diagnosed_time,
        #'数据起始时间':start_time,
        #'数据结束时间':end_time,
        '类别':type,
        '省份':province,
        '城市':city,
        '新增确诊病例':in_diagnosed,
        '新增治愈出院数':in_cure,
        '新增死亡数':in_die,
        '核减':in_check,
        '治愈核减':cure_check,
        '死亡核减':die_check,
        '累计确诊人数':sum_diag,
        '累计治愈人数':sum_cure,
        '累计死亡人数':sum_die
    }
    return daily

def time_transfer(date):
    days_2=['4','6','9','11']
    month=date.split('月')[0]
    day=date.split('月')[1].split('日')[0]
    day_end=str(int(day)+1)
    month_end=month

    if day=='31':
        month_end=str(1+int(month))
        day_end='1'
    elif day=='30':
        if month in days_2:
            month_end=str(1+int(month))
            day_end='1'
    elif day=='29':
        if month=='2':
            month_end=str(1+int(month))
            day_end='1'
    start_time='2020/'+month+'/'+day+' 00:00'
    end_time='2020/'+month_end+'/'+day_end+' 00:00'
    return start_time,end_time

def get_file_path(root_path,file_list,dir_list):   
    #获取该目录下所有的文件名称和目录名称    
    dir_or_files = os.listdir(root_path)    
    for dir_file in dir_or_files:        
        #获取目录或者文件的路径        
        dir_file_path = os.path.join(root_path,dir_file)        
        #判断该路径为文件还是路径        
        if os.path.isdir(dir_file_path):            
            dir_list.append(dir_file_path)            
            #递归获取所有文件和目录的路径            
            get_file_path(dir_file_path,file_list,dir_list)        
        else:            
            file_list.append(dir_file_path)

def check_last_data(data):
    daily={}
    Diagnosed_time=[]
    start_time=[]
    end_time=[]
    type=[]
    province=[]
    city=[]
    in_diagnosed=[]
    in_cure=[]
    in_die=[]
    in_check=[]
    sum_diag=[]
    sum_cure=[]
    sum_die=[]
    sum_cure_check=[]
    sum_die_check=[]
    data_shape=data.shape[0]
    map_colums=['公开时间','类别','省份','城市','新增确诊病例','新增治愈出院数','新增死亡数','核减','治愈核减','死亡核减','累计确诊人数','累计治愈人数','累计死亡人数']
    for row in range(0,data_shape):
        temp_data=data.iloc[row,:].copy()
        #print(temp_data)
        if temp_data['类别']=='国外':
            continue
        
        for i in range(0,13):
            if temp_data[map_colums[i]]!=temp_data[map_colums[i]]:
                temp_data.loc[map_colums[i]]=''

        #start_time_p,end_time_p=time_transfer(temp_data['公开时间'])
        #start_time.append(start_time_p)
        #end_time.append(end_time_p)
        Diagnosed_time.append(temp_data['公开时间'])
        type.append(str(temp_data['类别']))
        province.append(str(temp_data['省份']))
        city.append(str(temp_data['城市']))
        in_diagnosed.append(str(temp_data['新增确诊病例']))
        in_cure.append(str(temp_data['新增治愈出院数']))
        in_die.append(str(temp_data['新增死亡数']))
        in_check.append(str(temp_data['核减']))
        sum_cure_check.append(str(temp_data['治愈核减']))
        sum_die_check.append(str(temp_data['死亡核减']))
        sum_diag.append(str(temp_data['累计确诊人数']))
        sum_cure.append(str(temp_data['累计治愈人数']))
        sum_die.append(str(temp_data['累计死亡人数']))

    daily={
        '确诊时间':Diagnosed_time,
        #'数据起始时间':start_time,
        #'数据结束时间':end_time,
        '类别':type,
        '省份':province,
        '城市':city,
        '新增确诊病例':in_diagnosed,
        '新增治愈出院数':in_cure,
        '新增死亡数':in_die,
        '核减':in_check,
        '治愈核减':sum_cure_check,
        '死亡核减':sum_die_check,
        '累计确诊人数':sum_diag,
        '累计治愈人数':sum_cure,
        '累计死亡人数':sum_die
    }
        
    return daily

def date_ex(data):
    data_shape=data.shape[0]
    for row in range(0,data_shape):
        temp_data=data.iloc[row,:].copy()
        tuple_time=xldate_as_tuple(int(temp_data['公开时间']),0)
        untrans_date=datetime.datetime(*tuple_time)
        if temp_data['类别']=='地区级':
            data.loc[row,'类别']='城市级'
        data.loc[row,'公开时间']=entoch(untrans_date)
    return data

def add_last_data(file):
    try:
        data=pd.read_csv(file,error_bad_lines=False)
        daily=check_last_data(data)
        data=pd.DataFrame(daily)
        data.to_csv(outputfile, mode='a',index=False, header=False,encoding='utf_8_sig')

    except Exception as e:
        #print(e)
        #print(file)
        with open(log_file,"w",encoding='utf_8_sig') as log:
            log.write('异常原因:'+str(e)+'\n')
            log.write(file+'\n')

def check_all_data():
    file_list=[]
    dir_list=[]
    root_path='./china'
    get_file_path(root_path,file_list,dir_list)
    i=0
    for file in file_list:
        try:
            data=pd.read_csv(file,error_bad_lines=False)
            check_null_data(data)
            check_error_data(data)
            daily=exchangetooldcol(data)
            data=pd.DataFrame(daily)
            data.to_csv(outputfile, mode='a',index=False, header=False,encoding='utf_8_sig')

        except Exception as e:
            print(e)
            print(file)

    with open(log_file,"a",encoding='utf_8_sig') as log:
        for log_info in is_error_data:
            log.write(log_info+'\n')
        log.write('\n*******************************\n\n')
        for log_info in is_null_data:
            log.write(log_info+'\n')

def xlsx_to_csv(file):
    ex=pd.read_excel(file,encoding='utf_8_sig')
    file_name=file.split('.')[0]
    ex=date_ex(ex)
    return ex

#def check_xlsx_data(root_path):
def check_xlsx_data(file):
    file_list=[]
    dir_list=[]
    merge_result='1'
    #get_file_path(root_path,file_list,dir_list)
    sys_str=platform.system()
    flag=''
    if sys_str=='Windows' or sys_str=='windows':
        flag='\\'
    else:
        flag='/'

    try:
        #for file in file_list:

        if time_yesterday in file:
            data=pd.read_excel(file,encoding='utf_8_sig')
            daily=exchangetooldcol(data)
            if daily==1:
                judge_data=data.copy()
                merge_result=log_file
                out_info='{}文件格式存在问题'.format(judge_data.iloc[2,5])
                with open(log_file,"w",encoding='utf_8_sig') as log:
                    log.write(time_today+'_'+time_Nowhour+'\n')
                    log.write('异常原因:'+out_info+'\n')
                return merge_result
            data=pd.DataFrame(daily)
            data.to_csv(outputfile, mode='a',index=False, header=False,encoding='utf_8_sig')

        with open(completed_file,"a",encoding='utf_8_sig') as com:
            com.write(file+'\n')
        #print('end check')
        '''
        with open(log_file,"a",encoding='utf_8_sig') as log:
            for log_info in is_error_data:
                log.write(log_info+'\n')
        '''
    except Exception as e:
        #print('异常原因:',e)
        #print(file)
        merge_result=log_file
        with open(log_file,"w",encoding='utf_8_sig') as log:
            log.write(time_today+'_'+time_Nowhour+'\n')
            log.write('异常原因:'+str(e)+'\n')
            log.write(file+'\n')

    return merge_result

'''
mergeDataFile:前日所生成的合并文件
         如：MergeData_20200220.csv
data_dir:需要进行合并、校验的文件 
         如：../../data/......./china/anhui/anhuiCaseStatistics_20200221.csv
'''
def checkv4_Main(mergeDataFile,data_dir):
    #生成当日MergeData_date.csv文件
    if not os.path.exists(outputfile):
        with open(outputfile,'w',newline='',encoding='utf_8_sig') as f:
            csv_write = csv.writer(f)
            csv_head = old_colums
            csv_write.writerow(csv_head)
    
    if os.path.exists(yes_completed_file):
        os.remove(yes_completed_file)
    if os.path.exists(log_yes_file):
        os.remove(log_yes_file)

    if os.path.exists(completed_file):
        with open(completed_file,"r",encoding='utf_8_sig') as log:
            for data in log:
                Completed.append(data)

    '''
    add_last_data()
    func:读取基础数据，包含自运行起日之前日所有数据的MergeData_date.csv文件
    para:输入参数为前日已保存的MergeData_date.csv文件
    introduce:date为文件中日期标识符，如20200219，即2020年2月19日所生成,
              MergeData文件与脚本所在同一级目录
    '''
    add_last_data(mergeDataFile)
    '''
    check_xlsx_data()
    func:校验今日所上传的数据文件,将当日上传文件中的数据合并至MergeData_date.csv中
    para:上传数据的完整目录文件名,如../../data/
    '''
    merge_result=check_xlsx_data(data_dir)

    return outputfile,merge_result
    #check.checkMain(outputfile,'./log')
