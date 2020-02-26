def ReadLastFileName():
    fp=open('LastDataFile.txt', "r", encoding='UTF-8-sig')
    datas=fp.readlines()
    name=datas[0].strip()
    num=datas[1]
    fp.close()
    return str(name),int(num)
def WriteLastFileName(name,num):
    fp=open('LastDataFile.txt', "w", encoding='UTF-8-sig')
    fp.write(name+'\n')
    fp.write(str(num)+'\n')
    fp.close()
#if __name__ == "__main__":
    #print(ReadLastFileName())
    #WriteLastFileName('merge.csv')
    #print(ReadLastFileName())