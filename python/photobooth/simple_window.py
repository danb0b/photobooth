# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 20:54:47 2019

@author: danaukes
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 13:01:43 2014

@author: danaukes
"""

import numpy
import cv2
#import math
from math import pi
#import matplotlib.pyplot as plt
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

def cv_to_qimage(img):
#        image[:,:,:] = img
    output = img[:,:,(2,1,0)]
#            img = img[::2,::2,(2,1,0)]
#            output = process2(img)
    h,w,d = output.shape
    output2= numpy.require(output,dtype = numpy.uint8,requirements='C')
    qimage = qg.QImage(output2.data,w,h,w*d,qg.QImage.Format_RGB888)
    return qimage
    
    
class ImageWindow(qw.QWidget):
    def __init__(self,*args, **kwargs):
        super(ImageWindow,self).__init__(*args, **kwargs)
        self.video_capture = cv2.VideoCapture(2)

        is_sucessfully_read, img = self.video_capture.read()
        is_sucessfully_read, img = self.video_capture.read()
        is_sucessfully_read, img = self.video_capture.read()
        cv2.waitKey(20)
        self.image_height, self.image_width,self.image_depth = img.shape
#        self.setMinimumSize(self.image_width,self.image_height)
        self.imagelabel = qw.QLabel()
        self.imagelabel.setMinimumSize(1, 1)
#        self.imagelabel.setGeometry(qc.QRect(0,0,self.image_width,self.image_height))
        layout = qw.QVBoxLayout()
        layout.addWidget(self.imagelabel)
        self.setLayout(layout)
#        self.ii = 0
#        self.template = numpy.zeros((480,640,3),dtype=numpy.uint8)
        self.image = numpy.zeros(img.shape)

        self.loadimage()
        self.startTimer(1/30)
        self.setSizePolicy(
            qw.QSizePolicy.MinimumExpanding,
            qw.QSizePolicy.MinimumExpanding)
##    
    def sizeHint(self):
        return qc.QSize(self.image_width, self.image_height)
#        self.imagelabel.sizeHint = sizeHint

    def timerEvent(self,event):
        self.loadimage()

    def loadimage(self):
        good_read, img = self.video_capture.read()
        self.image[:,:,:] = img
        qimage = cv_to_qimage(img)
        self.pm = qg.QPixmap(qimage)
        self.update_image(self.pm)
#    def resizeEvent(self,event):
#        pm= self.pm
#        pm = pm.scaledToWidth(10)
#        self.imagelabel.setPixmap(pm)
        
    def update_image(self,pm):
#        pm = pm.scaled(self.imagelabel.width()-100,self.imagelabel.height()-100)
        pm = pm.scaledToWidth(self.imagelabel.width()-0)
        self.imagelabel.setPixmap(pm)
    
    def closeEvent(self, event):
        self.video_capture.release()
        
if __name__ == '__main__':
    
    app = qw.QApplication(sys.argv)
#    timer = qc.QTimer()
    iw = ImageWindow()    
    iw.show()
#    for ii in range(100):
#        is_sucessfully_read, img = video_capture.read()
#        output = process2(img)
#        cv2.imshow("Camera Feed", output)#   
#        cv2.waitKey(10)
    sys.exit(app.exec_())
