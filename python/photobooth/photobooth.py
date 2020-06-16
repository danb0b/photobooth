# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 13:01:43 2014

@author: danaukes
"""

import numpy
import cv2
#import math
#from math import pi
#import matplotlib.pyplot as plt
video_capture = cv2.VideoCapture(2)
#video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
#video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 360);
import PyQt5.QtGui as qg
import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import sys
import time

from PyQt5 import QtCore, QtGui
from cv2 import *

def process1(img):
    img3 = cv2.blur(img,(2,2))
    edges = cv2.Canny(img,100,200,1)
#    lines = cv2.HoughLinesP(edges, 1, pi/180, 80,30,10)     
    kernel = numpy.ones((2,2),numpy.uint8)
    dilation = cv2.dilate(edges,kernel,iterations = 1)
    a,b= numpy.nonzero(dilation)
    final = img.copy()
#    for x1,y1,x2,y2 in lines.squeeze():
#        cv2.line(final,(x1,y1),(x2,y2),(0,0,255),2)
    final[a,b,:]=0

    return final


def process2(img):
    gray = numpy.uint8(img.sum(2)/3)
    blur1 = numpy.int32(cv2.blur(gray,(10,10)))
    blur2 = numpy.int32(cv2.blur(gray,(50,50)))
    a = blur1 - blur2+127
#    a-=a.min()
#    a = a*1.*255/a.max()
    a = numpy.uint8(a)

    b = a.copy()
#    b[b>=127]=255
#    b[b<1]
#    MAX = 2**8-1
#    MID = 2**7-1
#    MIN = 0
    top = 125.
    bottom = 124.
    
    b = (((b*1.)-bottom)*255.)/(top-bottom)
    b[b>255]=255
    b[b<0]=0
    b = numpy.uint8(b)

#    f = 1
    return b
#while True:
    
class ImageWindow(qw.QWidget):
    state_location = {1:(0,480*1-1),2:(0,480*2-1),3:(0,480*3-1),4:(0,480*4-1)}
    def __init__(self):
        super(ImageWindow,self).__init__()
        is_sucessfully_read, img = video_capture.read()
        cv2.waitKey(10)
        self.image_height, self.image_width,self.image_depth = img.shape
#        self.setMinimumSize(self.image_width,self.image_height)
        self.imagelabel = qw.QLabel()
#        self.imagelabel.setGeometry(qc.QRect(0,0,self.image_width,self.image_height))
        layout = qw.QVBoxLayout()
        layout.addWidget(self.imagelabel)
        self.setLayout(layout)
        self.ii = 0
        self.template = cv2.imread('template2.png',cv2.IMREAD_COLOR)
        self.loadimage()
        
    def keyPressEvent(self,event):
        print('hello')
        if event.key()==qc.Qt.Key_Space:
            self.loadimage()

    def loadimage(self):
#            cv2.waitKey(10)
        good_read, img = video_capture.read()
        good_read, img = video_capture.read()
#        img = process1(img)
        state = self.ii%5
        print(state)
        if state==0:
            self.image = self.template.copy()
        else:
            x,y = self.state_location[state]
            self.image[y:y+self.image_height,x:x+self.image_width,:] = img
        output = self.image[::2,::2,(2,1,0)]
#            img = img[::2,::2,(2,1,0)]
#            output = process2(img)
        h,w,d = output.shape
        output2= numpy.require(output,dtype = numpy.uint8,requirements='C')
        qimage = qg.QImage(output2.data,w,h,w*d,qg.QImage.Format_RGB888)
        self.imagelabel.setPixmap(qg.QPixmap(qimage))
        if state==4:
            cv2.imwrite(str(time.time()).replace('.','_')+'.jpg',self.image)
        self.ii+=1
#            self.imagelabel.setGeometry(qc.QRect(0,0,self.image_height,self.image_width))
#            cv2.imshow("Camera Feed", img)#   
        
if __name__ == '__main__':
    
    app = qw.QApplication(sys.argv)
    iw = ImageWindow()    
    iw.show()
#    for ii in range(100):
#        is_sucessfully_read, img = video_capture.read()
#        output = process2(img)
#        cv2.imshow("Camera Feed", output)#   
#        cv2.waitKey(10)
#    sys.exit(app.exec_())
