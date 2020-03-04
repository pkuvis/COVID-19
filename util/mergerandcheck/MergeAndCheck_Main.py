import check_v4 as Merger
import MergeData_Check as check
import os
import sys
import shutil
import ReadLastFilename as LastFile
#传入参数说明：
#Checkprovins:省份文件夹名:如安徽省,则参数为:anhui
#Checkfilename:为上传文件名:如：anhuiCaseStatistics_20200219.xlsx
#返回参数sming：
#checkresult:返回校验结果,值为Pass或者Faile
#logfilePath:为生成的log文件路径
#None,None 说明通过成功的文件重复上传
#Mergetemp.csv为最新无错误的mergedata文件
def Merge(Checkprovins,Checkfilename):
    parentpath = os.path.realpath('../../')
    #print(parentpath)
    chekfile = parentpath + '/data/unchecked/manual_collect/china/'+Checkprovins+'/'+Checkfilename

    movePath = parentpath + '/data/checked/china/' + chekfile.split('/')[-2] + '/' + chekfile.split('/')[-1]
    if os.path.exists(movePath):
        # os.remove(chekfile)
        return None,None
    LastFilename,checknum=LastFile.ReadLastFileName()
    #print(LastFilename)
    mergeFile,merge_result=Merger.checkv4_Main(LastFilename,chekfile)

    checkresult,logFilePath=check.checkMain(mergeFile)
    if merge_result!='1':
        checkresult='Faile'
        logFilePath='/'+merge_result
        logfilePath=os.path.realpath('.').replace('\\','/')+logFilePath
        return checkresult,logfilePath

    if checkresult=='Pass':
        # if checknum!=0:
        #     os.remove(LastFilename)
        checknum+=1
        checknum%=35
        #os.rename(mergeFile,'Mergetemp.csv')
        LastFile.WriteLastFileName(mergeFile,checknum)
        # shutil.move(chekfile, movePath)
    else:
        os.remove(mergeFile)
    logfilePath=os.path.realpath('.').replace('\\','/')+logFilePath[1:]
    return checkresult,logfilePath

if __name__ == "__main__":
    #Merger.checkv4_Main('MergeData_20200219.csv')
    #check.checkMain('MergeData_20200220_19-35-12.csv')
    result, log = Merge('hubei', 'hubeiCaseStatistics_20200228.xlsx')
    # result, log = Merge(sys.argv[1], sys.argv[2])
    print(result)
    print(log)
