#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import pathlib
import time
import re
def readFile(filepath):
    f = open(filepath, "r", encoding='UTF-8-sig')
    Alldata = f.readlines()
    Length = len(Alldata)
    # print()
    Lables = re.split(',|\\t',Alldata[0].strip())
    data = []
    for index in range(1, len(Alldata)):
        data.append(Alldata[index].strip())
    # data=Alldata[1:]
    # print()
    #Lables为字段名，根据不同字段的位置可以直接修改Lables数组的标号
    f.close()
    return Lables, data


def citydict(Lables,data):
    cerr=[]
    cerrnum=0
    prodic = {}
    for Len in data:
        List = re.split(',|\\t', Len)
        datadic={}
        for index in range(0, len(List)):
            if index >= 13:
                break
            if index==0:
                if '-' in List[index]:
                    t=List[index].split(' ')[0].split('-')
                    #
                    List[index]=t[0]+'/'+str(int(t[1]))+'/'+str(int(t[2]))+' 00:00'
            List[index]=List[index].replace('\u3000','')
            List[index] = List[index].replace('\xa0\xa0', '')
            if index > 3 and (List[index] == '' or List[index] == None):
                datadic[Lables[index]] = '0'
            else:
                datadic[Lables[index]] = List[index].replace('.0', '')
        if prodic.get(datadic.get(Lables[2])) == None:
            prodic[datadic.get(Lables[2])]= []
            prodic[datadic.get(Lables[2])].append(datadic)
        else:
            prodic[datadic.get(Lables[2])].append(datadic)
        #Allarry.append(datadic)
    for pk in list(prodic.keys()):#pk 为省份
        if pk=='':
            continue
        cdic={}
        for dk in prodic.get(pk):#dk为该省份的数据
            #print(prodic.get(pk)[index])
            if cdic.get(dk.get(Lables[3]))==None:
                cdic[dk.get(Lables[3])]=[]
                cdic[dk.get(Lables[3])].append(dk)
            else:
                cdic[dk.get(Lables[3])].append(dk)

        for ck in list(cdic.keys()):#ck为城市
            if ck=='':
                continue
            ckAlldata=cdic.get(ck)
            # last保存前面所有日期的该城市累加值
            last = {Lables[4]: 0, Lables[5]: 0, Lables[6]: 0}
            for cday_data in ckAlldata:
                last[Lables[4]]+=(int(cday_data[Lables[4]])+ int(cday_data[Lables[7]]))
                last[Lables[5]] += int(cday_data[Lables[5]])+int(cday_data[Lables[8]])
                last[Lables[6]] += int(cday_data[Lables[6]])+int(cday_data[Lables[9]])
                # print(last)
                # break
                g =cday_data.get(Lables[0]).split('月')
                #print(g)
                g[1] = g[1].split('日')[0]
                # print(g)
                if int(g[0]) < 2:
                    continue
                elif int(g[0]) >= 2 and int(g[1]) < 16:
                    continue
                if last[Lables[4]]!=int(cday_data[Lables[10]]):
                    cerrnum+=1
                    cerr.append({cday_data[Lables[0]]:{pk:{ck:{Lables[4]:last[Lables[4]],
                                                               Lables[10]:cday_data[Lables[10]]}}}})
                if last[Lables[5]]!=int(cday_data[Lables[11]]):
                    cerrnum+=1
                    cerr.append({cday_data[Lables[0]]: {pk: {ck: {Lables[5]: last[Lables[5]],
                                                                  Lables[11]: cday_data[Lables[11]]}}}})
                if last[Lables[6]]!=int(cday_data[Lables[12]]):
                    cerrnum += 1
                    cerr.append({cday_data[Lables[0]]: {pk: {ck: {Lables[6]: last[Lables[6]],
                                                                  Lables[12]: cday_data[Lables[12]]}}}})
    return cerr,cerrnum
def writeCerr(filename,cerr):
    fp = open(filename, "a+", encoding="utf-8")
    fp.write("---------不符合规则:地区级复核，地区级当日之前的新增累加值 == 卫健委发布的当日累计值---------\n")
    for e in cerr:
        dates=list(e.keys())[0]
        g = dates.split('月')

        g[1] = g[1].split('日')[0]
        # print(g)
        if int(g[0]) < 2:
            continue
        elif int(g[0]) >= 2 and int(g[1]) < 16:
            continue
        pk=list(e.get(dates).keys())[0]
        ck=list(e.get(dates).get(pk).keys())[0]
        errs=e.get(dates).get(pk).get(ck)
        erk=list(errs.keys())
        wstr=dates+','+pk+','+ck+','+erk[0][2:4]+',地区级累加值为'+str(errs.get(erk[0]))+',卫健委累计值'+str(errs.get(erk[1]))
        fp.write(wstr+'\n')
    fp.write('\n')
def datedict(Lables, data):
    dateict = {}
    dateList = []
    for Len in data:
        List =re.split(',|\\t',Len)
        lable = {}
        for index in range(0, len(List)):
            if index>=13:
                break
            if index==0:
                if '-' in List[index]:
                    t=List[index].split(' ')[0].split('-')
                    #
                    List[index]=t[0]+'/'+str(int(t[1]))+'/'+str(int(t[2]))+' 00:00'
            List[index]=List[index].replace('\u3000','')
            List[index] = List[index].replace('\xa0\xa0', '')
            if index > 3 and (List[index] == '' or List[index] == None):
                lable[Lables[index]] = '0'
            else:
                lable[Lables[index]] = List[index].replace('.0','')
        if dateict.get(List[0]) == None:
            dateict[List[0]] = []
            dateict[List[0]].append(lable)
            dateList.append(List[0])
        else:
            dateict[List[0]].append(lable)
    return dateict, dateList


def prodict(dateict, dateList, Lables):
    prodicts = {}
    provins = {}
    for key in dateList:
        prodic = {}
        for k in dateict.get(key):
            #print(k)
            #通过正则表达式获取每个省的简称
            k[Lables[2]]=re.split('省|市|(回族)*自治区|特别行政区', k[Lables[2]])[0]
            if prodic.get(k[Lables[2]]) == None:
                prodic[k[Lables[2]]] = []
                prodic[k[Lables[2]]].append(k)
            else:
                prodic[k[Lables[2]]].append(k)
            if provins.get(k[Lables[2]]) == None and k[Lables[1]] != '国外':
                provins[k[Lables[2]]] = 0
        prodicts[key] = prodic
    return prodicts, list(provins.keys())

#每天的地区和省，以及每天的各省和全国的新增是否相等
def computeDay(prodicts, proLists, Lables):

    dayErr=0
    cdayWarning=0
    dateList = list(prodicts.keys())
    compdics = {}
    # 省级每天核查错误数据
    perrdics = {}
    # 国家每天核查错误数据
    cerrdics = {}
    for datekey in dateList:
        #print(prodicts.get(datekey).get('安徽')[0])
        prolist = list(prodicts.get(datekey).keys())
        prodic = prodicts.get(datekey)
        prodic_1 = {}
        perrdics[datekey] = []
        # 存储某天各省累计信息
        stypesum = {}
        for prokey in prolist:
            proArry = prodic.get(prokey)
            protype = {}
            types = []
            typesSum = []
            for p in proArry:
                if p.get(Lables[1])=='':
                    p[Lables[1]]='省级'
                if protype.get(p.get(Lables[1])) == None:
                    #print(p)
                    types.append(p.get(Lables[1]))
                    typesSum.append(p.get(Lables[1]) + "累计")
                    protype[p.get(Lables[1])] = []
                    protype[p.get(Lables[1])].append(p)
                    protype[p.get(Lables[1]) + "累计"] = {}
                    protype[p.get(Lables[1]) + "累计"][Lables[4]] = int(p.get(Lables[4]))
                    protype[p.get(Lables[1]) + "累计"][Lables[5]] = int(p.get(Lables[5]))
                    #print(Lables[7])
                    protype[p.get(Lables[1]) + "累计"][Lables[6]] = int(p.get(Lables[6]))
                    protype[p.get(Lables[1]) + "累计"][Lables[7]] = int(p.get(Lables[7]))
                    protype[p.get(Lables[1]) + "累计"][Lables[8]] = int(p.get(Lables[8]))
                    protype[p.get(Lables[1]) + "累计"][Lables[9]] = int(p.get(Lables[9]))
                else:
                    protype[p.get(Lables[1])].append(p)
                    protype[p.get(Lables[1]) + "累计"][Lables[4]] += int(p.get(Lables[4]))
                    protype[p.get(Lables[1]) + "累计"][Lables[5]] += int(p.get(Lables[5]))
                    protype[p.get(Lables[1]) + "累计"][Lables[6]] += int(p.get(Lables[6]))
                    protype[p.get(Lables[1]) + "累计"][Lables[7]] += int(p.get(Lables[7]))
                    protype[p.get(Lables[1]) + "累计"][Lables[8]] += int(p.get(Lables[8]))
                    protype[p.get(Lables[1]) + "累计"][Lables[9]] += int(p.get(Lables[9]))
            prodic_1[prokey] = protype
            # ========将每个省当天datekey省级与地区的数据放入数组中
            ss = []
            for i in range(0, len(typesSum)):
                ss.append({typesSum[i]: protype.get(typesSum[i])})
            stypesum[prokey] = ss
            # print(stypesum)
            # ====================================================

            # 复核每个省每天的数据============================
            if len(types)==1:
                g = datekey.split('月')

                g[1] = g[1].split('日')[0]
                # print(g)
                if int(g[0]) < 2:
                    continue
                elif int(g[0]) >= 2 and int(g[1]) < 16:
                    continue
                if typesSum[0]=='省级累计':
                    dayErr += 1
                    perrdics[datekey].append({prokey: {'': {Lables[4]:0},
                                  typesSum[0]: {Lables[4]:protype.get(typesSum[0])[Lables[4]]}}})
                #print(typesSum)
            if len(types) > 1 :
                #print(typesSum)
                if protype.get(typesSum[0])[Lables[4]] !=\
                        protype.get(typesSum[1])[Lables[4]]:
                    dayErr+=1
                    perrdics[datekey].append(
                        {prokey: {typesSum[0]: {Lables[4]:protype.get(typesSum[0])[Lables[4]]},
                                  typesSum[1]: {Lables[4]:protype.get(typesSum[1])[Lables[4]]}}})
                if protype.get(typesSum[0])[Lables[5]] != protype.get(typesSum[1])[Lables[5]]:
                    dayErr += 1
                    perrdics[datekey].append(
                        {prokey: {typesSum[0]:{Lables[5]: protype.get(typesSum[0])[Lables[5]]},
                                  typesSum[1]: {Lables[5]:protype.get(typesSum[1])[Lables[5]]}}})
                if protype.get(typesSum[0])[Lables[6]] != protype.get(typesSum[1])[Lables[6]]:
                    dayErr += 1
                    perrdics[datekey].append(
                        {prokey: {typesSum[0]: {Lables[6]:protype.get(typesSum[0])[Lables[6]]},
                                  typesSum[1]: {Lables[6]:protype.get(typesSum[1])[Lables[6]]}}})
                if protype.get(typesSum[0])[Lables[7]] != protype.get(typesSum[1])[Lables[7]]:
                    dayErr += 1
                    perrdics[datekey].append(
                        {prokey: {typesSum[0]: {Lables[7]: protype.get(typesSum[0])[Lables[7]]},
                                  typesSum[1]: {Lables[7]: protype.get(typesSum[1])[Lables[7]]}}})
                    # ===================================================
            # print(types,typesSum)
            # break
        # print(stypesum)
        # ===========复核每天各省和全国=====================
        prosum = {Lables[4]: 0, Lables[5]: 0, Lables[6]: 0, Lables[7]: 0}
        csum = None
        #print(proLists,stypesum.get('内蒙古'))
        for pro in proLists:
            if pro == '':
                #print(pro,datekey,stypesum.get(pro))
                if stypesum.get(pro)==None:
                    csum={'新增确诊病例': 0, '新增治愈出院数': 0, '新增死亡数': 0, '核减': 0,'国家缺少':0}
                else:
                    csum = stypesum.get(pro)[0].get('国家级累计')
            elif pro != None or pro != '':
                #print(stypesum.get(pro),pro,datekey)
                if stypesum.get(pro)==None:
                    continue
                for p in stypesum.get(pro):

                    d = p.get('省级累计')
                    # print(p)
                    if d != None:
                        prosum[Lables[4]] += d[Lables[4]]
                        prosum[Lables[5]] += d[Lables[5]]
                        prosum[Lables[6]] += d[Lables[6]]
                        prosum[Lables[7]] += d[Lables[7]]
        #print(prosum,csum)
        if csum==None:
            continue
        cerrdics[datekey] = []
        if (prosum[Lables[4]] ) != (csum[Lables[4]]):
            if csum.get('国家缺少')!=None:
                cdayWarning+=1
                cerrdics[datekey].append({Lables[4]: {'省级累计': prosum[Lables[4]], '国家级累计': '统计缺失'}})
            else:
                cdayWarning += 1
                cerrdics[datekey].append({Lables[4]:{'省级累计': prosum[Lables[4]], '国家级累计':  csum[Lables[4]] }})
        if prosum[Lables[5]] != csum[Lables[5]]:
            if csum.get('国家缺少') != None:
                cdayWarning += 1
                cerrdics[datekey].append({Lables[5]: {'省级累计': prosum[Lables[5]],
                                                      '国家级累计': '统计缺失'}})
            else:
                cdayWarning += 1
                cerrdics[datekey].append({Lables[5]:{'省级累计':  prosum[Lables[5]],
                                      '国家级累计':  csum[Lables[5]]}})
        if prosum[Lables[6]] != csum[Lables[6]]:
            if csum.get('国家缺少') != None:
                cdayWarning += 1
                cerrdics[datekey].append({Lables[6]: {'省级累计': prosum[Lables[6]],
                                                      '国家级累计': '统计缺失'}})
            else:
                cdayWarning += 1
                cerrdics[datekey].append({Lables[6]:{'省级累计': prosum[Lables[6]],
                                      '国家级累计': csum[Lables[6]]}})
        # break
        # ===================================================

        # 存储每天所有数据
        compdics[datekey] = prodic_1
        # break
    # print(perrdics)
    # print(cerrdics)
    return perrdics,cerrdics,compdics,dayErr,cdayWarning

#计算当前某天前面所有天的累加值
def computedS(dateList,compdics,proList,Lables):
    SumErr=0
    proDic={}
    Allpro={}
    for pk in proList:
        proDic[pk]=[]
    for datekey in dateList:
        if datekey=='' or compdics.get(datekey)==None:
            continue
        #print(datekey,)
        prokeys=list(compdics.get(datekey).keys())
        for pk in prokeys:
            proDic.get(pk).append({datekey:compdics.get(datekey).get(pk)})
    #print(proDic.get('安徽'))
    err=[]
    for pk in proList:
        if pk=='':
            continue
        Allpro[pk]={}
        #print(proDic.get(pk))
        index=0
        #last保存前面所有日期的省级累加值
        last={Lables[4]:0,Lables[5]:0,Lables[6]:0}
        #lastnow保存前面最新的卫健委累计数据
        lastnow={Lables[10]:0,Lables[11]:0,Lables[12]:0}
        for d in proDic.get(pk):
            d.get(list(d.keys())[0]).get('省级')
            now={Lables[10]:0,Lables[11]:0,Lables[12]:0}
            if d.get(list(d.keys())[0]).get('省级')==None:
                t=datekey.split(' ')[0].split('/')
                #print(t)
                #nowdate=t[0]+'/'+str(int(t[1]))+'/'+str(int(t[2])+1)+' 00:00'
                nowdate=t[0]
                err.append({pk: {nowdate: {'省级':'缺失'}}})
                continue
            #print(d.get(list(d.keys())[0]).get('省级'))
            for k in d.get(list(d.keys())[0]).get('省级'):
                datekey=k[Lables[0]]
                last[Lables[4]]+=(int(k.get(Lables[4]))+int(k.get(Lables[7])))
                last[Lables[5]] +=(int(k.get(Lables[5]))+int(k.get(Lables[8])))
                last[Lables[6]] +=(int(k.get(Lables[6]))+int(k.get(Lables[9])))
                now[Lables[10]]+=int(k.get(Lables[10]))
                now[Lables[11]]+= int(k.get(Lables[11]))
                now[Lables[12]]+= int(k.get(Lables[12]))
            pLk={}
            pLk[Lables[4]] = last[Lables[4]]
            pLk[Lables[5]] = last[Lables[5]]
            pLk[Lables[6]] = last[Lables[6]]
            Allpro[pk][datekey]={'省级积累':pLk,'卫健委':now}
            #保存第一天的累计
            if index == 0:
                lastnow=nowTolastnow(lastnow,now,Lables)
                index+=1
            #if pk=='广东':
                #print(now,Lables[8],last,Lables[4])
            #当当前累计值不为0时候核查否则就用lastnow的核查
            g = datekey.split('月')

            g[1] = g[1].split('日')[0]
            # print(g)
            if int(g[0]) < 2:
                continue
            elif int(g[0]) >= 2 and int(g[1]) < 16:
                continue

            if last.get(Lables[4])!=now.get(Lables[10]):
                if now.get(Lables[10])!=0:
                    SumErr+=1
                    err.append({pk:{datekey:{Lables[4]:last.get(Lables[4]),Lables[10]:now.get(Lables[10])}}})
                else:
                    if last.get(Lables[4]) != lastnow.get(Lables[10]):
                        SumErr += 1
                        err.append({pk: {datekey: {Lables[4]: last.get(Lables[4]), Lables[10]: lastnow.get(Lables[10])}}})
            if last.get(Lables[5])!=now.get(Lables[11]):
                if  now.get(Lables[11])!=0:
                    SumErr += 1
                    err.append({pk: {datekey: {Lables[5]: last.get(Lables[5]), Lables[11]: now.get(Lables[11])}}})
                else:
                    if last.get(Lables[5])!=lastnow.get(Lables[11]):
                        SumErr += 1
                        err.append({pk: {datekey: {Lables[5]: last.get(Lables[5]), Lables[11]: lastnow.get(Lables[11])}}})
            if last.get(Lables[6])!=now.get(Lables[12]):
                if now.get(Lables[12])!=0:
                    SumErr += 1
                    err.append({pk: {datekey: {Lables[6]: last.get(Lables[6]), Lables[12]: now.get(Lables[12])}}})
                else:
                    if last.get(Lables[6])!=lastnow.get(Lables[12]):
                        SumErr += 1
                        err.append({pk: {datekey: {Lables[6]: last.get(Lables[6]), Lables[12]: lastnow.get(Lables[12])}}})
            if now.get(Lables[10])!=0 :
                lastnow[Lables[10]]=now.get(Lables[10])
            if now.get(Lables[11])!=0 :
                lastnow[Lables[11]] = now.get(Lables[11])
            if now.get(Lables[12])!=0:
                lastnow[Lables[12]] = now.get(Lables[12])
        #print(err)
        #break
    #print(Allpro.get('安徽'))
    return err,Allpro,SumErr
def nowTolastnow(lastnow,now,Lables):
    lastnow[Lables[10]] = now[Lables[10]]
    lastnow[Lables[11]] = now[Lables[11]]
    lastnow[Lables[12]] = now[Lables[12]]
    return lastnow

def write1(filename,perrdics,dateList):
    fp = open(filename, "a+", encoding="utf-8")
    fp.write('3.Error Records\n')
    fp.write('---------不符合规则:省级复核，省级每天新增 == 其下辖地区新增和---------------------\n')
    for datekey in dateList:
        wstr = '';
        if len(perrdics.get(datekey))!=0:
            for index in range(0,len(perrdics.get(datekey))):
                prodic=perrdics.get(datekey)[index]
                pro=list(prodic.keys())[0]
                #print(prodic.get(pro))
                #if
                #prodic.get(pro)['地区级累计']
                if prodic.get(pro).get('地区级累计')==None:
                    wstr = pro + ',' + datekey + ',地区级数据缺失'
                # #
                # if type=='':

                else:
                    type = list(prodic.get(pro)['地区级累计'].keys())[0]
                #print(pro,datekey)
                    wstr = pro + ',' + datekey + ',地区级'+type+'累加值为' + str(prodic.get(pro)['地区级累计'].get(type)) + ',' \
                            + '省级新增' + str(prodic.get(pro)['省级累计'].get(type))
                #print(wstr)
                fp.write(wstr+'\n')
    fp.write('\n')
    fp.close()
def write2(filename,err):
    fp = open(filename, "a+", encoding="utf-8")
    fp.write('---------不符合规则:省级复核，省级当日之前的新增累加值 == 卫健委发布的当日累计值---------\n')
    for pk in err:
        pro=list(pk.keys())[0]
        dates=list(pk.get(pro).keys())[0]
        g=dates.split('月')

        g[1]=g[1].split('日')[0]
        #print(g)
        if int(g[0])<2:
            continue
        elif int(g[0])>=2 and int(g[1])<16:
            continue
        s=pk.get(pro).get(dates)
        wstr=''
        if s.get('省级')!=None:
            wstr=pro+','+dates+',省级数据缺失'
        else:
            #if  '确诊'in list(s.keys())[0]:
            #     s
            # else:
            wstr=pro+','+str(dates)+','+list(s.keys())[0][2:4]+',省级累加值'+str(s.get(list(s.keys())[0]))+\
                     ',卫健委累计'+str(s.get(list(s.keys())[1]))
            fp.write(wstr+'\n')
    fp.write('\n')
    fp.close()

def write3(filename,cerrdics,dateList):
    fp = open(filename, "a+", encoding="utf-8")
    fp.write('4. Warning Report\n')
    fp.write('-----不符合规则：全国级复核，各省每日新增累加值 == 国家级当日累计值-----------------\n')
    for datekey in dateList:
        wstr = '';
        if datekey=='':
            continue
        if len(cerrdics.get(datekey))!=0:
            for index in range(0,len(cerrdics.get(datekey))):
                prodic=cerrdics.get(datekey)[index]
                type=list(prodic.keys())[0]
                wstr = datekey + ','+type[2:4]+',各省累加值为' + str(prodic.get(type).get('省级累计')) + ',' \
                            + '国家当天新增' + str(prodic.get(type).get('国家级累计'))
                #print(wstr)
                fp.write(wstr+'\n')
    fp.write('\n')
    fp.close()
def writeCSV(filename,err,proAll,Lables):
    #print(proAll)
    fp = open(filename, "a+", encoding="utf-8-sig")
    fp.write('公开时间,省份,累计确诊,卫健委累计确诊,是否一致,累计出院,卫健委累计出院,是否一致,累计死亡,卫健委累计死亡,是否一致\n')
    errdic={}
    for pk in err:
        pro = list(pk.keys())[0]
        dates = list(pk.get(pro).keys())[0]
        if errdic.get(pro)==None:
            errdic[pro]={}
            errdic[pro][dates]=[]
            errdic[pro][dates].append(pk.get(pro).get(dates))
        else:
            if errdic.get(pro).get(dates)==None:
                errdic[pro][dates] = []
                errdic[pro][dates].append(pk.get(pro).get(dates))
            else:
                errdic[pro][dates].append(pk.get(pro).get(dates))
    #print(errdic)
    for pk in list(proAll.keys()):
        for Dk in list(proAll.get(pk).keys()):
            #print(errdic.keys())
            if  errdic.get(pk)==None or errdic.get(pk).get(Dk)==None:
                wstr=Dk+','+pk+','+str(proAll.get(pk).get(Dk).get('省级积累').get(Lables[4]))+','+\
                     str(proAll.get(pk).get(Dk).get('卫健委').get(Lables[10]))+',是'+','+\
                     str(proAll.get(pk).get(Dk).get('省级积累').get(Lables[5]))+','+\
                     str(proAll.get(pk).get(Dk).get('卫健委').get(Lables[11])) + ',是'+','+ \
                     str(proAll.get(pk).get(Dk).get('省级积累').get(Lables[6]))+','+ \
                     str(proAll.get(pk).get(Dk).get('卫健委').get(Lables[12])) + ',是'
                fp.write(wstr + '\n')
            else:
                for kk in  errdic.get(pk).get(Dk):
                    s=kk

                    if list(s.keys())[0]==Lables[4]:
                        wstr = Dk + ',' + pk + ',' + str(s.get(Lables[4])) + ',' + \
                            str(s.get(Lables[10])) + ',否' + ',' + \
                            str(proAll.get(pk).get(Dk).get('省级积累').get(Lables[5])) + ',' + \
                            str(proAll.get(pk).get(Dk).get('卫健委').get(Lables[11])) + ',是' + ',' + \
                            str(proAll.get(pk).get(Dk).get('省级积累').get(Lables[6])) + ',' + \
                            str(proAll.get(pk).get(Dk).get('卫健委').get(Lables[12])) + ',是'
                    elif list(s.keys())[0] == Lables[5]:
                        wstr = Dk + ',' + pk + ',' + str(proAll.get(pk).get(Dk).get('省级积累').get(Lables[4])) + ',' + \
                            str(proAll.get(pk).get(Dk).get('卫健委').get(Lables[10])) + ',是' + ',' + \
                            str(s.get(Lables[5])) + ',' + \
                            str(s.get(Lables[11])) + ',否' + ',' + \
                            str(proAll.get(pk).get(Dk).get('省级积累').get(Lables[6])) + ',' + \
                            str(proAll.get(pk).get(Dk).get('卫健委').get(Lables[12])) + ',是'
                    elif list(s.keys())[0] == Lables[6]:
                        wstr = Dk + ',' + pk + ',' + str(proAll.get(pk).get(Dk).get('省级积累').get(Lables[4])) + ',' + \
                            str(proAll.get(pk).get(Dk).get('卫健委').get(Lables[10])) + ',是' + ',' + \
                            str(proAll.get(pk).get(Dk).get('省级积累').get(Lables[5])) + ',' + \
                            str(proAll.get(pk).get(Dk).get('卫健委').get(Lables[11])) + ',是' + ',' + \
                            str(s.get(Lables[6])) + ',' + \
                            str(s.get(Lables[12])) + ',否'
                    fp.write(wstr+'\n')
    fp.close()
def writeHead(filename,checkname,checktime,errs,warnings):
    fp = open(filename, "a+", encoding="utf-8")
    fp.write('1. Check Result\n')
    if errs==0:
        fp.write('Pass\n\n')
    else:
        fp.write('Faile\n\n')
    fp.write('2. Check Summary\n')
    fp.write(' Checked file name:'+checkname+'\n')
    fp.write(' Check time:'+checktime+'\n')
    fp.write(' Check Result: '+str(errs)+' erros '+str(warnings)+' warnings\n\n')
def checkMain(CheckFilepath,logpath='./log'):

    filename=CheckFilepath

    Lables, data = readFile(filename)

    dateict, dateList = datedict(Lables, data)

    prodicts, proList = prodict(dateict, dateList, Lables)

    perrdics, cerrdics, compdics ,dayErr,cdayWarning= computeDay(prodicts, proList, Lables)
    #print(cerrdics)
    err,proAll,SumErr= computedS(dateList, compdics, proList, Lables)
    cerr ,cerrnum= citydict(Lables, data)



    checkname = re.split('/|\\\\',str(filename))[-1]
    checktime = time.strftime("%Y%m%d_%H-%M-%S", time.localtime(time.time()))
    errs = dayErr+SumErr+cerrnum
    #print(dayErr,SumErr,cerrnum)
    warnings = cdayWarning


    pathlib.Path(logpath).mkdir(parents=True, exist_ok=True)
    filename = logpath+'/' + checkname.split('.')[0] + '_CheckReport' + checktime + '.log'
    writeHead(filename, checkname, checktime, errs, warnings)
    write1(filename, perrdics, dateList)
    write2(filename, err)

    writeCerr(filename, cerr)

    write3(filename, cerrdics, dateList)
    filename = logpath+'/' + checkname.split('.')[0] + '_AcummulatedValueCheckResult'+ checktime +'.csv'
    #print(filename)
    #print(proAll)
    writeCSV(filename, err,proAll,Lables)
    #print('finished')
    if errs!=0:
        return 'Faile'
    else:
        return 'Pass'
def CMDUse():
    filePath=sys.argv[1]
    sys.exit(checkMain(filePath))
if __name__ == '__main__':
    # CheckFilepath = './Mergerdata/MergeData_20200217.csv'
    # print(checkMain(CheckFilepath))
    CMDUse()
    # filename = './Mergerdata/MergeData_20200216(3).csv'
    #
    # Lables, data = readFile(filename)


