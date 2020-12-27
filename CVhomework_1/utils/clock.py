import cv2 
import os 
import math
import datetime
import numpy as np

class Clock:
    def __init__(self, img, x, y):
        self.radius = 80 # 圆的半径
        self.center = (x, y) # 圆心
        self.center_x = x 
        self.center_y = y
        self.margin = 2
        self.img = img
    
    def Initialize(self):
        # 1. 画出圆盘
        cv2.circle(self.img, self.center, self.radius, (0, 0, 0), thickness=2)

        self.pt1 = []
        # 2. 画出60条秒和分钟的刻线
        for i in range(60):
            # 最外部圆，计算A点
            x1 = self.center_x+(self.radius-self.margin)*math.cos(i*6*np.pi/180.0)
            y1 = self.center_y+(self.radius-self.margin)*math.sin(i*6*np.pi/180.0)
            self.pt1.append((int(x1), int(y1)))

            # 同心小圆，计算B点
            x2 = self.center_x+(self.radius-15)*math.cos(i*6*np.pi/180.0)
            y2 = self.center_y+(self.radius-15)*math.sin(i*6*np.pi/180.0)

            cv2.line(self.img, self.pt1[i], (int(x2), int(y2)), (0, 0, 0), thickness=1)

        # 3. 画出12条小时的刻线
        for i in range(12):
            # 12条小时刻线应该更长一点
            x = self.center_x+(self.radius-25)*math.cos(i*30*np.pi/180.0)
            y = self.center_y+(self.radius-25)*math.sin(i*30*np.pi/180.0)
            # 这里用到了前面的pt1
            cv2.line(self.img, self.pt1[i*5], (int(x), int(y)), (0, 0, 0), thickness=2)
        return self.img

    def Update(self):
        temp = np.copy(self.img)
        # 4. 获取系统时间，画出动态的时-分-秒三条刻线
        now_time = datetime.datetime.now()
        hour, minute, second = now_time.hour, now_time.minute, now_time.second

        # 画秒刻线
        # OpenCV中的角度是顺时针计算的，所以需要转换下
        sec_angle = second*6+270 if second <= 15 else (second-15)*6
        sec_x = self.center_x+(self.radius-self.margin)*math.cos(sec_angle*np.pi/180.0)
        sec_y = self.center_y+(self.radius-self.margin)*math.sin(sec_angle*np.pi/180.0)
        cv2.line(temp, self.center, (int(sec_x), int(sec_y)), (0, 0, 255), 1)

        # 画分刻线
        min_angle = minute*6+270 if minute <= 15 else (minute-15)*6
        min_x = self.center_x+(self.radius-35)*math.cos(min_angle*np.pi/180.0)
        min_y = self.center_y+(self.radius-35)*math.sin(min_angle*np.pi/180.0)
        cv2.line(temp, self.center, (int(min_x), int(min_y)), (10, 10, 10), 3)

        # 画时刻线
        hour_angle = hour*30+270 if hour <= 3 else (hour-3)*30
        hour_x = self.center_x+(self.radius-45)*math.cos(hour_angle*np.pi/180.0)
        hour_y = self.center_y+(self.radius-45)*math.sin(hour_angle*np.pi/180.0)
        cv2.line(temp, self.center, (int(hour_x), int(hour_y)), (0, 0, 0), 6)
        # 5. 添加当前日期文字
        font = cv2.FONT_HERSHEY_SIMPLEX
        time_str = now_time.strftime("%YY/%mM/%dD")
        cv2.putText(temp, time_str, (self.center_x-self.radius+10, self.center_y+110), font, 0.5, (0, 0, 0), 1)
        time_str2 = now_time.strftime("%Hh/%Mm/%Ss")
        cv2.putText(temp, time_str2, (self.center_x-self.radius+25, self.center_y+20), font, 0.5, (0, 0, 0), 1)
        return temp

if __name__ == '__main__':
    # 1. 新建一个画板并填充成白色
    img = np.zeros((1000, 1000, 3), np.uint8)
    img[:] = (255, 255, 255)
    clock = Clock(img, 225, 225)
    clock.Initialize()
    # 到这里基本的表盘图就已经画出来了
    while(1):
        temp = clock.Update()
        cv2.imshow('clocking', temp)
        if cv2.waitKey(1) == 27:  # 按下ESC键退出
            break