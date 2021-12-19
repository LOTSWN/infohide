import re

import numpy as np


def Str_encode(s:str,rule='utf-8'):
    '''
    将明文字符串按照rule的格式转化为01字符串
    :param s: 待编码字符串
    :param rule: 编码方案 默认utf-8
    :return: 字符串对应01字符串
    '''
    sc=s.encode(rule)
    bc=[bin(int(i))[2:].rjust(8,'0') for i in sc ]
    rtn=''.join(bc)
    return rtn

def Str_decode(s:str,rule='utf-8'):
    '''
    将01字符串（不加任何标识符和纠错码）转化为对应的明文字符串（默认UTF-8)
    :param s:01字符串
    :return:解码原文
    '''
    if len(s)==0:
        return '>>内容为空<<'
    if len(s)%8!=0:
        raise SyntaxError('编码不是八的倍数')
        #至少是字节的倍数才能操作

    msg=re.sub(r'0x','',hex(int(s,2)))
    str=""
    for i in range(int(len(s)/4)-len(msg)):
        str=str+"0"
    msg=str+msg
    rtn=bytes.fromhex(msg).decode(rule)
    return rtn

#bitstr=000000010000001000000011...
#shape=[2,2] 图形尺寸
def numtobit(pix):
	bitstr = ""
	j = 0
	pixString = ''.join('%s' %i for i in pix)	#将列表转为字符串
	a = re.findall('\d+',pixString,re.S)		#提取字符串里的数字

	while j < len(a):
		c = '{:08b}'.format(int(a[j]))		#将10进制转换成8位2进制
		j +=1
		bitstr += c

	return bitstr

def bittonum(bitstr,shape):
    j = 0
    bitlist = []
    output = [bitstr[i:i+8] for i in range(0,len(bitstr),8)]#对二进制流先进行8个8个分组
    while j < len(output):
        dec = int(output[j],2)				#对8位的2进制转换成10进制
        bitlist.append(dec)
        j +=1
    pix=np.zeros(shape=shape)

    nownum=0
    for i in range(shape[0]):
        for j in range(shape[1]):
            pix[i,j]=np.array([bitlist[nownum],bitlist[nownum+1],bitlist[nownum+2]])
            nownum=nownum+3
    pix=pix.astype(int)
    return pix

if __name__=="__main__":
    # print("输入要转换的字符串：")
    # message=input()
    # bit=Str_encode(message)
    # print(bit)
    # res = Str_decode(bit)
    # print(res)
    pix = [[[1, 2, 0], [1,2,1]],[[1,2,2], [1,2,3]]]
    pix=np.array(pix)
    bitstr=numtobit(pix)
    bittonum(bitstr,pix.shape)

