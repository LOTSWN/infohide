import jpegio as jio
#   置乱的代码，重用一些函数
from hide import DealAc,Scramb,find_n_k
import numpy as np
import trans
import checkcrc
def extra(jpeg,key,messageLen):
    """
        jpeg，嵌入后的载体
        key，密钥
        messageLen,所需要提取的消息长度
    """
    coef=jpeg.coef_arrays[0]
    Ava=DealAc(coef)

    cover=Scramb(Ava,key)
    totAC=len(cover)
    # 组数关系：  tot/message>=(2^k-1)/k,找到上界
    k=1
    k=find_n_k(totAC,messageLen)
    CoverStep=(1<<k)-1
    j=0
    res=""
    while(len(res)<messageLen):
        f=0
        tmp=j
        while(j<tmp+CoverStep):
            f ^= (j - tmp + 1) * (cover[j][0] & 1)
            j += 1
        res+=bin(f)[2:].zfill(k)

    return res

def getInfo(inpath,key,length):
    jpeg = jio.read(inpath)
    str = extra(jpeg,key,length)
    checknum=checkcrc.getcrc(str)
    return str,checknum


if __name__=="__main__":
    # Test
    print("待提取水印的图片路径,依次输入解密钥key，提取消息的长度,以回车为一个输入结束：")
    test_path=input()
    jpeg = jio.read(test_path)
    key=int(input())
    messageLen=int(input())
    messageLen*=8
    print("提取的message: "+extra(jpeg,key,messageLen))