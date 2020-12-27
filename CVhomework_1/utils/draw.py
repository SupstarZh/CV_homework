import random 
import cv2 
import os 
import math
import datetime
import numpy as np
import matplotlib.pyplot as plt
from utils.util import cv2ImgAddText

def draw_face(img, count): # 脸型
    if count>=0 and count<16: # 0-16
        cv2.ellipse(img, (500, 300), (130, 80), 10, 180+count*10, 190+count*10, (0, 0, 0), 3) # 340
    if count>=16 and count<21: #5
        temp = count-16
        cv2.line(img, (371-temp*6, 280+temp*8), (371-6-temp*6, 280+8+temp*8), (0, 0, 0), 3)
    if count>=21 and count<26: #5
        temp = count-21
        cv2.line(img, (341-temp*5, 319+temp*4), (336-temp*5, 324+temp*4), (0, 0, 0), 3)
    if count>=26 and count<44: #18
        temp = count-26 
        cv2.ellipse(img, (315, 450), (110, 110), -10, 100+temp*10, 110+temp*10, (0, 0, 0), 3)
    if count>=44 and count<67: #23
        temp = count-44
        cv2.line(img, (303+temp*10, 562-temp), (313+temp*10, 560-temp), (0, 0, 0), 3)
    if count>=67 and count< 78: #11
        temp = count - 67
        cv2.line(img, (534+temp*10, 542-temp*5), (544+temp*10, 537-temp*5), (0, 0, 0), 3)
    return img

def draw_hair(img, count): # 头发
    if count>=78 and count<136: #58s
        temp = count-78
        cv2.line(img, (422+3*temp, 228+temp), (425+3*temp, 229+temp), (0, 0, 0), 10) #172, 58
        cv2.line(img, (440+3*temp, 224+temp), (443+3*temp, 225+temp), (0, 0, 0), 10) #175, 59
        if count<126:
            cv2.line(img, (455+3*temp, 222+temp), (458+3*temp, 223+temp), (0, 0, 0), 10) #145, 48
        if count<119:
            cv2.line(img, (475+3*temp, 220+temp), (478+3*temp, 221+temp), (0, 0, 0), 13) #123, 40
        if count<104:
            cv2.line(img, (500+3*temp, 216+temp), (503+3*temp, 217+temp), (0, 0, 0), 7) #77, 27
    if count>=136 and count<174:
        temp = count-136
        if count<163:
            cv2.line(img, (608+temp, 275+3*temp), (609+temp, 278+3*temp), (0, 0, 0), 20) #27, 80
        cv2.line(img, (595+temp, 287+2*temp), (596+temp, 289+2*temp), (0, 0, 0), 20) #38, 80
    return img

def draw_eyes(img, count): # 眼睛
    if count>=174 and count<210:
        temp = count-174
        cv2.ellipse(img, (420, 370), (45, 45), 0, 0+temp*10, 10+temp*10, (0, 0, 0), -1)
        cv2.ellipse(img, (531, 400), (45, 45), 0, 0+temp*10, 10+temp*10, (0, 0, 0), -1)
    if count>=210 and count<246:
        temp = count-210
        cv2.ellipse(img, (420, 370), (20, 20), 0, 0+temp*10, 10+temp*10, (255, 255, 255), -1)
        cv2.ellipse(img, (531, 400), (20, 20), 0, 0+temp*10, 10+temp*10, (255, 255, 255), -1)
    return img

def draw_mouth(img, count): # 嘴巴
    if count>=246 and count<261:
        temp = count-246
        cv2.ellipse(img, (320, 480), (70, 45), 0, 0+temp*10, 10+temp*10, (0, 0, 0), 3)
    return img

def draw_ears(img, count): # 耳朵
    if count>=261 and count<271:
        temp = count-261
        cv2.line(img, (625+2*temp, 376-2*temp), (627+2*temp, 374-2*temp), (0, 0, 0), 3) #20, 25
    if count>=271 and count<289:
        temp = count-271
        cv2.ellipse(img, (644, 421), (60, 70), 0, 270+10*temp, 280+10*temp, (0, 0, 0), 3)
    return img    

def draw_brow(img, count): # 眉毛
    if count>=289 and count<305:
        temp = count-289
        cv2.ellipse(img, (425, 325), (50, 40), 20, 180+10*temp, 190+10*temp, (0, 0, 0), 15)
        cv2.ellipse(img, (550, 350), (50, 40), 30, 180+10*temp, 190+10*temp, (0, 0, 0), 15)
    return img

def addcatoonText(img, count):
    temp_img = img
    count3 = count
    if count3>305 and count3<310:
        temp_img = cv2ImgAddText(temp_img,"蜡", 70, 70, (255, 0, 0), 50)
    if count3>=310 and count3<315:
        temp_img = cv2ImgAddText(temp_img,"笔", 120, 70, (0, 255, 0), 50)
    if count3>=315 and count3<320:
        temp_img = cv2ImgAddText(temp_img,"小", 170, 70, (255, 255, 0), 50)
    if count3>=320 and count3<325:
        temp_img = cv2ImgAddText(temp_img,"新", 220, 70, (0, 0, 255), 50)
    
    return temp_img

def addselfintroText(img, count):
    temp_img = img 
    #325 400
    text1 = "Hi~小姐姐。我叫野原新之助，今年5岁了，喜欢巧克力饼干，最讨厌吃胡萝卜和青椒。"
    text2 = "小姐姐请问你吃纳豆加不加葱花呢。小姐姐你喜不喜欢吃胡萝卜和青椒呢。我想要一份充满小"
    text3 = "姐姐爱的外卖。小姐姐想不想做我的三轮车兜风？"
    if count>=325 and count<330:
        temp_img = cv2.rectangle(temp_img, (60, 600),(890, 730), (0, 0, 0), 2)
    elif count>=330 and count<330+40:
        temp = count-330
        temp_img = cv2ImgAddText(temp_img, text1[temp], 100+20*temp, 620, (0, 0, 0), 20)
    elif count>=370 and count<411:
        temp = count-370
        temp_img = cv2ImgAddText(temp_img, text2[temp], 70+20*temp, 650, (0, 0, 0), 20)
    elif count>=411 and count<433:
        temp = count-411
        temp_img = cv2ImgAddText(temp_img, text3[temp], 70+20*temp, 680, (0, 0, 0), 20)
    return temp_img

def draw(img, count):
    count = count-1
    if count<0:
        return 0
    elif count<78:
        return draw_face(img, count)
    elif count<174:
        return draw_hair(img, count)
    elif count<246:
        return draw_eyes(img, count)
    elif count<261:
        return draw_mouth(img, count)
    elif count<289:
        return draw_ears(img, count)
    elif count<305:
        return draw_brow(img, count)
    elif count<325:
        return addcatoonText(img, count)
    elif count<433:
        return addselfintroText(img, count)
    else:
        return img
