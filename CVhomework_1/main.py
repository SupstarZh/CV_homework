import cv2 
import os 
import math
import time
import inspect
import pathlib
import datetime
import subprocess
import numpy as np
from utils.util import cv2ImgAddText, gif_split
from utils.clock import Clock
from utils.special import Anime
from utils.draw import draw

def MainWindow(img_root='./img/', fps=8, savefile='resultVideo.avi', width=1200, height=800):
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    videoWriter = cv2.VideoWriter(savefile, fourcc, fps, (width, height), True)

    zju_path = pathlib.Path('./zju/')
    zju_images = [f for f in zju_path.iterdir() if f.suffix=='.jpg']
    zju_images = sorted(zju_images, key=lambda x: int(x.stem))
    zju_images = [cv2.imread(str(f)) for f in zju_images]
    begin_video = Anime((900,700), 4, 3, 6)
    begin = begin_video.make(zju_images, repeat=2)

    sdwlb = gif_split("img/sdwlb.gif", (900, 700))

    # 新建一个画板并初始化
    img = np.zeros((height, width, 3), np.uint8)
    img[:] = (255, 255, 255)
    cv2.line(img, (960, 0), (960, 800), (0, 0, 0), 3)

    # 浙大校徽
    zju_p = cv2.imread('./img/zju2.jpg')
    zju_p = cv2.resize(zju_p, (200,150))
    img[220:370, 970:1170] = zju_p[:, :]
                                                                                                           
    # 个人信息
    myphoto = cv2.imread('./img/2.png')
    myphoto = cv2.resize(myphoto, (200, 300))
    img[480:780, 970:1170] = myphoto[:, :]
    img = cv2ImgAddText(img, "姓名：卓文杰", 970, myphoto.shape[1]+160, (0, 0, 0), 22)
    img = cv2ImgAddText(img, "学号：12021057", 970, myphoto.shape[1]+200, (0, 0, 0), 22)
    img = cv2ImgAddText(img, "个人照片:", 970, myphoto.shape[1]+240, (0, 0, 0), 22)

    clock = Clock(img, 1080, 100)
    clock.Initialize()

    count = 0
    count2 = 0
    count3 = 0 

    temp_img = img
    while(1):
        count = count+1
        if count>100+len(begin):
            count2 = count2+1
        if count2>40:
            count3 = count3+1
        # 循环显示每一帧
        temp = clock.Update() # 时钟更新
        temp[0:800, 0:900] = (255, 255, 255) #显示界面清屏
        if count>=1 and count<=20:
            temp = cv2ImgAddText(temp, "ComputerVision homework 一", 200, 300, (255-15*(count-1), 255-20*(count-5), 255-(count+5)*10), 50+count-8)
        # 浙大校徽
        if count>20 and count<=40:
            temp = cv2ImgAddText(temp, "首位嘉宾是", 300+(count-20)*3, 300, (0+(count-20)*10, 0, 255-(count-20)*10), 50+(count-20)-8)
        if count>40 and count<=60:
            temp = cv2ImgAddText(temp, "浙 江 大 学！", 350-(count-40)*3, 300, (150-(count-40)*10, 0, 100+(count-40)*10), 50-(count-40)+23)
        if count>60 and count<=100:
            zju = cv2.imread('./img/zju.jpg')
            zju = zju[:,70:zju.shape[1]-70]
            temp[(count-10)*3+0:(count-10)*3+zju.shape[0], (count-10)*4+0: (count-10)*4+zju.shape[1]] = zju[:, :]
        # 浙大元素照片
        if count>100 and count<=100+len(begin):
            zju_photo = begin[count-101]
            temp[50:750, 30:930] = zju_photo[:, :]
        
        if count2>0 and count2 <=20:
            temp = cv2ImgAddText(temp, "The Next is", 330+count2*3, 300, (0+count2*10, 0, 255-count2*10), 50+count2-8)
        if count2>20 and count2<=40:
            temp = cv2ImgAddText(temp, "我的儿童画", 380-(count2-14)*3, 300, (150-(count2-10)*10, 0, 100+(count2-10)*10), 50-count2+23)
        
        if count3>0 and count3<460:
            temp_img = draw(temp_img, count3)
            temp[0:800, 0:980] = temp_img[0:800, 0:980]
            temp_img = temp
        if count3>=460 and count3<480:
            temp = cv2ImgAddText(temp, "最 后", 330+(count3-460)*3, 300, (0+(count3-460)*10, 155+int(math.pow(-1, (count3-460))*(count3-470)*10), 255-(count3-460)*10), 50+(count3-460)-8)
        if count3>=480 and count3<500:
            temp = cv2ImgAddText(temp, "让我表演一套", 310+(count3-480)*3, 300, (0+(count3-480)*10, 155+int(math.pow(-1, (count3-480))*(count3-490)*10), 255-(count3-480)*10), 50+(count3-480)-8)
        if count3>=500 and count3<520:
            temp = cv2ImgAddText(temp, "闪电五连鞭", 310+(count3-500)*3, 300, (0+(count3-500)*10, 155+int(math.pow(-1, (count3-500))*(count3-510)*10), 255-(count3-500)*10), 50+(count3-500)-8)
        if count3>=520 and count3<520+len(sdwlb):
            sd = sdwlb[count3-520]
            temp[50:750, 30:930] = sd[:, :]
        if count3>=520+len(sdwlb) and count3<540+len(sdwlb):
            t = count3-520-len(sdwlb)
            temp = cv2ImgAddText(temp, "Ending", 310+t*3, 300, (0+t*10, 155+int(math.pow(-1, t*(t-10))*10), 255-t*10), 50+t-8)
        if count3>=540+len(sdwlb) and count3<560+len(sdwlb):
            t = count3-540-len(sdwlb)
            temp = cv2ImgAddText(temp, "谢谢大家～", 310+t*3, 300, (0+t*10, 155+int(math.pow(-1, t*(t-10))*10), 255-t*10), 50+t-8)
        if count3>=560+len(sdwlb) and count3<580+len(sdwlb):
            t = count3-560-len(sdwlb)
            temp = cv2ImgAddText(temp, "期待下一次再见", 310+t*3, 300, (0+t*10, 155+int(math.pow(-1, t*(t-10))*10), 255-t*10), 50+t-8)
        if count3>=580+len(sdwlb) and count3<632+len(sdwlb):
            t = count3-580-len(sdwlb)
            temp[:,:,:] = (255-t*5, 255-t*5, 255-t*5)
            temp = cv2ImgAddText(temp, "谢  幕",  380, 330, (t*5, t*5, t*5), 55-t)
        if count3>=632+len(sdwlb):
            count = 0 
            count2 = 0
            count3 = 0
        cv2.imshow('cv1', temp)  #展现动画
        videoWriter.write(temp) # 将每一帧写入视频中
        if cv2.waitKey(50) == 27:  # 按下ESC键退出
            break
        if cv2.waitKey(50) & 0xFF == ord(' '): # 按空格暂停
            cv2.waitKey(0)

if __name__ == '__main__':
    MainWindow(savefile='resultVideo.avi')