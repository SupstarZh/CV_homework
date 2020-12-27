import inspect
import pathlib
import cv2
import math
import subprocess

def transition(img1, img2, func, N):
    u, v = img1.shape[:2]
    a = []
    for h in range(N):
        img1 = img1.copy()
        for i in range(u):
            for j in range(v):
                if any(img1[i,j] != img2[i,j]) and func(i,j,h, N):
                    img1[i,j] = img2[i,j]
        a.append(img1)
    return a

class tf:
    # transition functions
    def melt(i, j, h, N):
        r = 6
        return math.sin(i/r) + math.cos(j/r)< h/N * 4 - 2

    def melts(i, j, h, N):
        r = 7
        return math.sin(i/r)*math.cos(j/r) < h/N*2-1

    def meltc(i, j, h, N):
        return (i-200)**2 + (j-150)**2 < (250/N * h)**2

    # def meltcx(i, j, h, N):
    #     return any(any((i-200 * k1)**2 + (j-125*k2)**2 < (125/N * h)**2 for k1 in range(1, 5)) for k2 in range(1, 5))

    def shiftv(i, j, h, N):
        return i < 400/N*h

    def shifth(i, j, h, N):
        return j < 300/N*h

    def shiftvx(i, j, h, N):
        L = 50
        return i % L < L/N*h

    def shifthx(i, j, h, N):
        L = 50
        return j % L < L/N*h

    def shiftvhx(i, j, h, N):
        L = 50
        return i % L < L/N*h and j % L < L/N*h

    def windmill(i, j, h, N):
        if j==150:
            return True
        else:
            phi = math.pi/4
            theta = math.atan((i-200)/(j-150))
            return (theta + math.pi/2) % phi < phi/N*h


def jpg2video(images, path, fps, repeat=1):
    """integrate images in JPG into a video"""
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    vw = cv2.VideoWriter(path, apiPreference=0, fourcc=fourcc, fps=fps, frameSize=(images[0].shape[1], images[0].shape[0]))
    for _ in range(repeat):
        for image in images:
            vw.write(image)
    vw.release()


class Anime(object):
    """Integrate images to a video"""
    def __init__(self, size, duration, stop, fps):
        """
        Arguments:
            size {tuple} -- size of viedo
            duration {number} -- the time of transition
            stop {number} -- the time of stop
            fps {number} -- fps

        duration, stop, fps is recommended to be int
        """
        self.size = size
        self.duration = duration
        self.stop = stop
        self.fps = fps

    def make(self, images, outfile='out.avi', funcs=None, repeat=1):
        N = self.duration * self.fps
        M = self.stop * self.fps
        import random
        images = [cv2.resize(image, self.size) for image in images]
        a = []
        if funcs is None:
            funcs = [f for _, f in inspect.getmembers(tf, inspect.isfunction)]
        for im1, im2 in zip(images[:-1], images[1:]):
            func = random.choice(funcs)
            a1 = transition(im1, im2, func, N)
            a.extend(a1+[im2]* M)
        #jpg2video(a, outfile, self.fps, repeat)

        return a

if __name__ == '__main__':
    PATH = pathlib.Path('/Users/zhuowenjie/PycharmProjects/zju/')
    images = [f for f in PATH.iterdir() if f.suffix=='.jpg']
    images = sorted(images, key=lambda x: int(x.stem))
    images = [cv2.imread(str(f)) for f in images]
    an = Anime((300,400), 4, 3, 25)
    outfile = 'out.avi'
    an.make(images, outfile=outfile, repeat=1)