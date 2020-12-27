import cv2 
import matplotlib.pyplot as plt 
import sys
import getopt
import operator
import argparse 
from scipy.ndimage import convolve1d
from math import exp
from scipy import signal
from PIL import Image
from pylab import *
import numpy as np 


class Harris_Corner:
    '''
    img: cv2 format
    '''
    def __init__(self, img, bsize=1, ksize=3, k=0.04):
        self.img = img 
        self.gray = self.BGR2GRAY(self.img)
        self.Ix2, self.Iy2, self.Ixy = self.Sobel_filter(self.gray)
        self.Ix2 = self.gaussian_filter(self.Ix2, kernel_size = ksize)
        self.Iy2 = self.gaussian_filter(self.Iy2, kernel_size = ksize)
        self.Ixy = self.gaussian_filter(self.Ixy, kernel_size = ksize)
        self.l1, self.l2 = self.get_eigvals(self.Ix2, self.Iy2, self.Ixy)
        self.out, self.R = self.corner_detect(self.gray, self.Ix2, self.Iy2, self.Ixy, k=k, th=0.01, bsize=bsize)

    def BGR2GRAY(self, img):
        gray = 0.114*img[..., 0] + 0.587*img[..., 1] + 0.299*img[...,2]
        gray = gray.astype(np.uint8)
        return gray 

    def Sobel_filter(self, gray):
        H, W = gray.shape
        sobely = np.array(((1,2,1), (0,0,0), (-1,-2,-1)), dtype=np.float32)
        sobelx = np.array(((1,0,-1), (2,0,-2),(1,0,-1)), dtype=np.float32)

        tmp = np.pad(gray, (1, 1), 'edge')
        Ix = np.zeros_like(gray, dtype = np.float32)
        Iy = np.zeros_like(gray, dtype = np.float32)
        im = gray
        #for i in range(1,im.shape[0]-1):
            #for j in range(1,im.shape[1]-1):
                #Ix[i][j] = int(float(im[i+1][j]) - float(im[i-1][j]))
                #Iy[i][j] = int(float(im[i][j+1]) - float(im[i][j-1]))
        for y in range(H):
            for x in range(W):
                Ix[y, x] = np.mean(tmp[y:y+3, x:x+3] * sobelx)
                Iy[y, x] = np.mean(tmp[y:y+3, x:x+3] * sobely)
        
        Ix2 = Ix**2
        Iy2 = Iy**2
        Ixy = Ix*Iy 
        return Ix2, Iy2, Ixy 
    
    def get_eigvals(self, Ix2, Iy2, Ixy):
        lam1 = (Ix2+Iy2) / 2 + np.sqrt(4*Ixy**2 + (Ix2-Iy2)**2) / 2
        lam2 = (Ix2+Iy2) / 2 - np.sqrt(4*Ixy**2 + (Ix2-Iy2)**2) / 2
        l1 = lam1 
        l2 = lam2 
        H, W = lam1.shape 
        for i in range(H):
            for j in range(W):
                if lam1[i, j]>=lam2[i,j]:
                    l1[i,j] = lam1[i, j]
                    l2[i,j] = lam2[i, j]
                else:
                    l1[i,j] = lam2[i,j]
                    l2[i,j] = lam1[i,j]
        return l1, l2

    def gaussian_filter(self, I, kernel_size=3, sigma=1):
        H, W = I.shape
        I_t = np.pad(I, (kernel_size//2, kernel_size//2), 'edge')

        K = np.zeros((kernel_size, kernel_size), dtype=np.float32)
        for x in range(kernel_size):
            for y in range(kernel_size):
                _x = x - kernel_size//2
                _y = y - kernel_size//2
                K[y, x] = np.exp(-(_x**2 + -y**2) / (2 * (sigma**2)))
        
        K /= (sigma * np.sqrt(2*np.pi))
        K /= K.sum()

        for y in range(H):
            for x in range(W):
                I[y, x] = np.sum(I_t[y:y+kernel_size, x:x+kernel_size] * K)
        
        return I 
    
    def corner_detect(self, gray, Ix2, Iy2, Ixy, k=0.05, th=0.001, bsize=2):
        out = np.array(self.img)

        R = (Ix2*Iy2 - Ixy**2) - k * ((Ix2+Iy2)**2)
        maxR = np.max(R)
        #out[R >= np.max(R) * th] = [255, 0, 0]
        for i in range(out.shape[0]):
            for j in range(out.shape[1]):
                if R[i][j] > th*maxR:
                    flag = False 
                    for ii in range(max(0, i-bsize), min(out.shape[0], i+bsize)):
                        if flag:
                            break 
                        for jj in range(max(0, j-bsize), min(out.shape[1], j+bsize)):
                            if R[i][j] < R[ii][jj]:
                                flag = True 
                                break 
                    if not flag:
                        cv2.circle(out, (j, i), 5, (0, 0, 255))
        out = out.astype(np.uint8)
        return out, R
    
    def get_values(self):
        return self.out, self.R/np.max(self.R)*255, self.l1/np.max(self.l1)*255, self.l2/np.max(self.l2)*255
    
    def draw(self, out, i, j):
        cv2.circle(out, (j, i), 5, (0, 0, 255))

    
    

if __name__ == '__main__':
    img = cv2.imread("images/4.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hc = Harris_Corner(img)
    out, R, l1, l2 = hc.get_values()
    cv2.imshow("test", out)
    cv2.imwrite("/results/R0.jpg", R)
    cv2.imwrite("/results/corner0.jpg", out)
    cv2.imwrite("/results/max_eig0.jpg", l1)
    cv2.imwrite("/results/min_eig0.jpg", l2)
    cv2.waitKey(0)