import random
import sys

import cv2 as cv
import trans
from bmp_read import bmp_read
import  numpy as np
import math
import checkcrc
class divideMsg:
    def get_rand(self,maxframe,num):
        arr=random.sample(range(0,maxframe),2*num)
        dict={}
        dictBf={}
        self.checksum={}
        for i in range(num):
            self.checksum[arr[i]] = 0
            dict[arr[i]]=""
        for j in range(num,2*num):
            dictBf[arr[j]]=""
        return  dict,dictBf

    def divide(self,maxframe,num,path,mode=1):
        self.dict,self.dictBf=self.get_rand(maxframe,num)
        if(mode==1):
            info = self.getRGBinfo(path)
            length=len(info)
            k=math.ceil(length/num)
            now=0
            keyBf=list(self.dictBf.keys())
            temp=0
            for key in self.dict.keys():
                self.dict[key]=info[now:min(length,now+k)]
                self.dictBf[keyBf[temp]] = self.dict[key]
                temp=temp+1
                now=now+k
                self.checksum[key]=checkcrc.getcrc(self.dict[key])
        else :
            info1,info2=self.getBMPinfo(path)

    def getBMPinfo(self,path):
        Readmachine = bmp_read()
        Readmachine.bmp_img_read_save_hist(path)
        return (str(np.array(Readmachine.color_index)),str(np.array(Readmachine.color_table)))

    def getRGBinfo(self,path):
        irgb = cv.imread(path)
        self.shape=irgb.shape
        irgb=trans.numtobit(irgb)
        return irgb



if __name__=="__main__":
    # im=np.zeros(10)
    # print(type(im.shape))
    anode=divideMsg()
    anode.divide(maxframe=255,num=80,path='.\infohide\\infoimg\\down.png')
    # print(anode.dict)
    # for i in list(anode.checksum.values()):
    #     print(i)
    print(list(anode.checksum.values()))

