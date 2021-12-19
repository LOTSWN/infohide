import numpy as np
def getcrc(codelis):
    now = 0
    ans = ""
    cnt=0
    for i in codelis:
        cnt=cnt+1
        j=int(i)
        now=j^now
        if(cnt%500==0):
            ans=ans+str(now)
            now=0
    return ans

def judgecheck(a,b):
    num=0
    for i in range(len(a)):
        if(a[i]==b[i]):
            num+=1
    return num

# m = np.array([1, 1, 0, 0, 1, 1])  # 发送数据比特序列
# m = list(m)  # 转化为列表类型
# crc = CRC(m, 4)
# crc.print_format()
