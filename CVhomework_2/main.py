import numpy as np 
import cv2 
import argparse
from Harris_Corner import Harris_Corner

def main(video_file = ""):
    if video_file == "": #没有文件，则调用摄像头
        video_cap = cv2.VideoCapture(0)
    else:
        video_cap = cv2.VideoCapture(video_file)
    time = 1
    while True:
        ret, frame = video_cap.read()
        if cv2.waitKey(1) & 0xff == 27:
            break 
        if cv2.waitKey(1) & 0xff == ord(' '):
            hc = Harris_Corner(frame)
            out, R, l1, l2 = hc.get_values()
            cv2.imshow("Corner", out)
            cv2.imshow("R", R)
            cv2.imshow("max_eig", l1)
            cv2.imshow("min_eig", l2)
            cv2.imwrite("results/corner"+str(time)+".jpg", out)
            cv2.imwrite("results/R"+str(time)+".jpg", R*10)
            cv2.imwrite("results/max_eig"+str(time)+".jpg", l1*10)
            cv2.imwrite("results/min_eig"+str(time)+".jpg", l2*10)
            cv2.waitKey(0)
            time = time+1
            cv2.destroyWindow("Corner")
            cv2.destroyWindow("R")
            cv2.destroyWindow("max_eig")
            cv2.destroyWindow("min_eig")
        cv2.imshow("video", frame) 

    video_cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Harris Corner Detection")
    parser.add_argument('-i', '--inputfile', type=str, default="", help = 'filename of input image')
    args = parser.parse_args()
    main(args.inputfile)