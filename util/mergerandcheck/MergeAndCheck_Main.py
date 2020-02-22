import check_v4 as Merger
import MergeData_Check as check
import os
import sys
import shutil
#传入参数说明：
#Checkprovins:省份文件夹名:如安徽省,则参数为:anhui
#Checkfilename:为上传文件名:如：anhuiCaseStatistics_20200219.xlsx
#返回参数sming：
#checkresult:返回校验结果,值为Pass或者Faile
#logfilePath:为生成的log文件路径
#None,None 说明通过成功的文件重复上传
#Mergetemp.csv为最新无错误的mergedata文件
def Merge(Checkprovins,Checkfilename):
    parentpath = sys.argv[0].replace('/util/mergerandcheck/Main.py', '')
    chekfile = parentpath + '/data/unchecked/manual_collect/china/'+Checkprovins+'/'+Checkfilename

    movePath = parentpath + './data/checked/china/' + chekfile.split('/')[-2] + '/' + chekfile.split('/')[-1]
    if os.path.exists(movePath):
        os.remove(chekfile)
        return None,None
    mergeFile=Merger.checkv4_Main('Mergetemp.csv')

    checkresult,logFilePath=check.checkMain(mergeFile)
    if checkresult=='Pass':
        os.remove('Mergetemp.csv')
        os.rename(mergeFile,'Mergetemp.csv')
        shutil.move(chekfile, movePath)
    else:
        os.remove(mergeFile)
    logfilePath=sys.argv[0].replace('Main.py','')+logFilePath[2:]
    return checkresult,logfilePath
#if __name__ == "__main__":
    #Merger.checkv4_Main('MergeData_20200219.csv')
    #check.checkMain('MergeData_20200220_19-35-12.csv')





