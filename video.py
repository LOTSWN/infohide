import sys

import moviepy.editor as mp
import numpy as np
from scipy.io import wavfile
import cv2 as cv
import os
import wave
from natsort import ns, natsorted

import checkcrc
import trans
from subprocess import call,STDOUT

from hide import putInfo
from extrac import getInfo
from divideMsg import divideMsg
class hideVideo:
    def decode_fourcc(self,cc):
        return "".join([chr((int(cc) >> 8 * i) & 0xFF) for i in range(4)])

    def __init__(self,path,videoName):
        #初始化视频
        self.path=path
        self.video = cv.VideoCapture(path+"\\"+videoName)

        self.fps = self.video.get(cv.CAP_PROP_FPS)
        self.frameNum=int(self.video.get(cv.CAP_PROP_FRAME_COUNT))
        #提取音频文件
        # my_clip.audio.write_audiofile('video.wav')


    # 隐藏音频
    def hiddenWav(self,inpath):
        sampleRate, musicData = wavfile.read(inpath)
        print("左声道：",musicData[:,0])
        print("右声道：",musicData[:,1])
        # print(trans.Str_encode("SSSS"))
        # info1,info2=self.show()
        # hide1=hidelsb()
        # hide2=hidelsb()

    # 生成音频
    def generateWav(self,wave_data,outpath,channels=1,sampwidth=2,framerate=44100):
        f = wave.open(outpath, "wb")
        f.setnchannels(channels)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        f.writeframes(wave_data.tobytes())
        f.close()

    # 获取帧列表
    def getFramelist(self,inpath):
        filelist=os.listdir(inpath)
        filelist = natsorted(filelist, alg=ns.PATH)  #要加alg=ns.PATH参数才和windows系统名称排序一致
        imglist=[]
        for file in filelist:
            imglist.append(inpath+"\\"+file)
        return imglist

    # 生成视频
    def generateVideo(self,inpath,outpath,fps):
        filelist=os.listdir(inpath)
        filelist = natsorted(filelist, alg=ns.PATH)  #要加alg=ns.PATH参数才和windows系统名称排序一致
        imagelist=[]
        for file in filelist:
            if os.path.splitext(file)[1] == '.jpg':  # 想要保存的文件格式
                im=cv.imread(inpath+"\\"+file)
                imagelist.append(im)
        thesize=(imagelist[0].shape[1],imagelist[0].shape[0])
        print("S")
        fourcc = cv.VideoWriter_fourcc(*"mp4v")
        videout = cv.VideoWriter(outpath, fourcc, fps, thesize)
        for im in imagelist:
            videout.write(im)
        videout.release()

    # 提取视频帧
    def videoFrame(self,outpath,timeF=1):
        success, frame = self.video.read()
        i = 0
        j = 0
        while success:
            if (i % timeF == 0):
                j = j + 1
                cv.imwrite(outpath +"\\frame"+ str(j) + '.jpg', frame, [int(cv.IMWRITE_JPEG_QUALITY), 100])
            i = i + 1
            success, frame = self.video.read()

    # 初始化隐藏信息
    def initInfo(self,inpath,listpath,num):
        anode = divideMsg()
        anode.divide(self.frameNum-1, num, inpath)
        self.shape=anode.shape
        self.checksum=anode.checksum
        imglist=self.getFramelist(listpath)
        self.keys=[]
        self.lengths=[]
        self.indexs=[]
        num=0
        for (i,value) in anode.dict.items():
            print(num)
            num+=1
            savepath=listpath+"\\"+"frame"+str(i)+".jpg"
            self.indexs.append(i)
            self.lengths.append(len(value))
            self.keys.append(putInfo(imglist[i], savepath, value))
        self.keys2=[]
        self.indexs2=[]
        for (i,value) in anode.dictBf.items():
            print(num)
            num+=1
            savepath=listpath+"\\"+"frame"+str(i)+".jpg"
            self.indexs2.append(i)
            self.keys2.append(putInfo(imglist[i], savepath, value))

    # 提取隐藏信息
    def extraInfo(self,listpath,keys,lengths,indexs,index2,keys2):
        imglist=self.getFramelist(listpath)
        now=0
        str=""
        for index in indexs:
            infostr1, check1 = getInfo(imglist[index],keys[now],lengths[now])
            infostr2, check2 = getInfo(imglist[index2[now]], keys2[now], lengths[now])
            num1=checkcrc.judgecheck(check1,self.checksum[now])
            num2=checkcrc.judgecheck(check2,self.checksum[now])
            if(num1>num2):
                print(now,"I")
                str=str+infostr1
            else:
                print(now,"O")
                str=str+infostr2
            now=now+1
        ansinfo=trans.bittonum(str,self.shape)
        cv.imwrite('info_get.png', ansinfo)  #保存写有信息的图片


    def show(self):
        str1="info frames:"+str(self.indexs)
        str2="keys:"+str(self.keys)
        print("info frames:", self.indexs)
        print("keys:", self.keys)
        print("对应分组长度(2进制编码):", self.lengths)
        print("infobf frames:", self.indexs2)
        print("keysbf:", self.keys2)
        print("checksum:", self.keys2)

        return str1,str2


#if __name__ == "__main__":
    # 隐藏
    # myproject=hideVideo(path='.\\infohide\\video',videoName='initvideo.avi')
    # # myproject.videoFrame(outpath='.\\infohide\\frame')
    # myproject.initInfo(inpath=".\infohide\infoimg\down.png",listpath='.\\infohide\\frame',num=80)
    # # myproject.extraInfo(listpath='.\\infohide\\frame',keys=myproject.keys,lengths=myproject.lengths,indexs=myproject.indexs)
    # # myproject.generateVideo(inpath='.\\infohide\\frame',outpath='.\\infohide\\video\\videohide.mp4',fps=myproject.fps)
    # myproject.show()
    #
    #
