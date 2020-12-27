import cv2 
import numpy as np
import copy
from PIL import Image, ImageDraw, ImageFont, ImageSequence

def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "font/Xingkai.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

def gif_split(path, size):
    img = Image.open(path)
    imageset = []
    for i in range(img.n_frames):
        img.seek(i)
        new = img.convert("RGB")
        new = cv2.cvtColor(np.asarray(new), cv2.COLOR_RGB2BGR)
        new = cv2.resize(new, size)
        imageset.append(new)
    return imageset

if __name__ == '__main__':
    imageset = gif_split("/Users/zhuowenjie/PycharmProjects/img/sdwlb.gif")
    for i in range(len(imageset)):
        cv2.imshow("sdwlb", imageset[i])
        cv2.waitKey(50)
    