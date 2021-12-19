import sys
import copy
import jpegio as jio
# import numpy as np
import random
import trans
import trans
INF =0x3f3f3f3f
def GetRandom():
    return random.randint(0,INF*INF)

def ListSave(l,name):
    """
       For Debug Only
    """
    with open(name, 'w') as f:
        for item in l:
            for i in item:
                f.write("%s " % i)
            f.write("\n")

def DealAc(DCT):
    """
        提取出所有可用AC系数，记录原位置信息。一个2维数组，记录AC系数，x，y坐标
        返回一个提取出的AC系数
    """
    res=[]
    for i in range(DCT.shape[0]):
        for j in range(DCT.shape[1]):
            if (i%8==0 and j%8==0) or DCT[i][j]==0 or DCT[i][j]==1: #i%8==0 and j%8==0 ->DC系数
                continue # 跳过不合法系数
            res.append([DCT[i][j],i,j])
    return res

def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    
def LCG(seed):
    """
        LCG算法，生成伪随机序列
    """
    a=134775813
    c=12347
    m=int(1e9+7)
    while True:
        seed=(a*seed+c)%m
        yield seed

    
def Scramb(AC,key):
    """
        根据密钥key，来置乱AC系数,返回置乱后的数组的克隆
    """
    AC=copy.deepcopy(AC)
   #  txtToList(AC,"hide.txt")
    length=len(AC)
    ran=LCG(key)
    for i in range(0,len(AC)):
        nx=next(ran)%length 
        swapPositions(AC,i,nx)
    return AC

def find_n_k(tot,Length):
    """
       找到合适n,k
    """
    res=1
    for i in range(2,Length+1):
        if Length%i==0:
            if(i>32) :
                continue
            if ((1<<i)-1)*(Length/i) <tot:
                res=i
    return res

def imbed(jpg,message,key=GetRandom()):
    """
        初始密钥k,将messag嵌入到AC系数中。
        返回生成密钥
    """
    key = GetRandom()
    coef=jpg.coef_arrays[0]
    Avaiable=DealAc(coef)
    cover=Scramb(Avaiable,key) # 得到初始置乱后的数组的副本,载体
    notone=0
    for i in range(len(cover)):
        if cover[i][0]!=1 and cover[i][0]!=-1:
            notone+=1
    # 计算确定 n, k ,g:组数
    totAC=len(cover)
    # print("Debug:所有可用AC：{}".format(totAC))
    # print("Debug:绝对值非1AC：{}".format(notone))
    if totAC < len(message): # 如果不够嵌入，程序退出
        sys.exit(0)
    k=find_n_k(totAC,len(message))
    # print("k: {}".format(k))
    CoverStep=(1<<k)-1
    j=0
    i=0
    count=0 # 如果测试了30组密钥还是没有找到符合条件的密钥，说明嵌入的消息过多，太容易碰撞
    max_count=50
    while(i<len(message)):
    # for i in range(0,len(message),k):
        strTmp=message[i:i+k]
        f=0
        tmp=j
        while(j<tmp+CoverStep):
            f^=(j-tmp+1)*(cover[j][0]&1) 
            j+=1
        s=f^int(strTmp,2)
        if s== 0:
            i+=k
            continue
        cover[tmp+s-1][0]^=1 # 最低位翻转
        if cover[tmp+s-1][0]==0: #  修改过后 系数为0了，不合法，根据旧key，生成新key，重新置乱
            count+=1
            if count >=max_count: # 说明消息长度过长，太容易发生碰撞
                print("Failed,碰撞次数达到上限")
                sys.exit(1)
            i=0
            j=0
            key=GetRandom()
            cover=Scramb(Avaiable,key)
            print("Test key{}: {}".format(count,key))
            continue
        i+=k
    # AC系数归位
    for i in range(0,len(cover)):
        coef[cover[i][1]][cover[i][2]]=cover[i][0]
    # 返回生成的key，jpeg图片   
    return key,jpg

def putInfo(inpath,outpath,message):
    jpeg=jio.read(inpath)
    key,jpeg=imbed(jpeg,message)
    jio.write(jpeg,outpath)
    return key



if __name__=="__main__":
    print(GetRandom())
    # print("依次输入载体jpg路径，所要嵌的消息, 输出文件名,每次输入以回车为结束：")
    # path=input()
    # message=input()
    # output=input()
    # print("消息长度：{}".format(len(message)))
    # message=trans.Str_encode(message)
    # jpeg = jio.read(path)
    # key,jpeg=imbed(jpeg,message)
    # print("生成解密key： {}".format(key))
    # jio.write(jpeg,output)
