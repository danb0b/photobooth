# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:08:55 2019

@author: daukes
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 13:01:43 2014

@author: danaukes
"""

import cv2
import numpy
import PyQt5.QtGui as qg
import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.Qt as qt
import sys
import time
import math
import simple_window
import make_pdf
import cairo
import os

from PyQt5 import QtCore, QtGui

num_images_per_page=4
class CustomWidget(qw.QWidget):
    width = 100
    height = 100

    def __init__(self,*args, **kwargs):
        super(CustomWidget,self).__init__(*args, **kwargs)
    
        self.setSizePolicy(
            qw.QSizePolicy.MinimumExpanding,
            qw.QSizePolicy.MinimumExpanding)
    
    def sizeHint(self):
        return qc.QSize(self.width, self.height)

class ControlWidget(CustomWidget):
    timer_string = '<span style=" font-size:50pt; font-weight:600; ">{0:1.0f}</span>'
    tt_string = '<span style=" font-size:100pt; font-weight:600; ">{0:1.0f}</span>'
    text_string= '<span style=" font-size:50pt;">{0}</span>'
    delay =100
    timer_start = 10
    timer_fire = 5
    def __init__(self,*args, **kwargs):
        super(ControlWidget,self).__init__(*args, **kwargs)
        
        self.picture_ii = 0
        self.roll_ii= 0
        self.t = self.timer_start

        self.time_remaining=qw.QLabel(self.tt_string.format(self.t))
        self.picture_num=qw.QLabel(self.timer_string.format(math.ceil(self.picture_ii+1)))
        self.roll_num=qw.QLabel(self.timer_string.format(math.ceil(self.roll_ii+1)))
#        self.time_remaining.setSizePolicy(qw.QSizePolicy.MinimumExpanding,qw.QSizePolicy.MinimumExpanding)
#        self.tf = self.time_remaining.setTextFormat(1)
#        self.tf.FontPointSize=50
#        self.time_remaining.setTextFormat()
        self.start_button = qw.QPushButton()
        self.start_button.setStyleSheet('font-size: 50px; height: 60px;')
#        self.start_button.setMinimumSize(100,100)
        
        layout1 = qw.QVBoxLayout()

        lh = qw.QHBoxLayout()
        lh.addStretch()                                               
        lh.addWidget(qw.QLabel(self.text_string.format('Time')))
        lh.addStretch()                                               
        layout1.addLayout(lh)

        lh = qw.QHBoxLayout()
        lh.addStretch()                                               
        lh.addWidget(self.time_remaining)
        lh.addStretch()                                               
        layout1.addLayout(lh)

#        layout1.addLayout(lh)

        lh = qw.QHBoxLayout()
        lh.addWidget(qw.QLabel(self.text_string.format('Roll #')))
        lh.addStretch()                                               
        lh.addWidget(self.roll_num)
        layout1.addLayout(lh)

        lh = qw.QHBoxLayout()
        lh.addWidget(qw.QLabel(self.text_string.format('Picture #')))
        lh.addStretch()                                               
        lh.addWidget(self.picture_num)
        layout1.addLayout(lh)


        layout1.addWidget(self.start_button)
#        layout.addWidget(self.start_button)
        self.setLayout(layout1)

        self.startTimer(self.delay)
        
        self.started = False
        self.update_start()
        self.start_button.pressed.connect(self.start_timer)
        
    def timer_zero(self,x,y):
        pass
        
    def timerEvent(self,event):
        self.picture_num.setText(self.timer_string.format(math.ceil(self.picture_ii+1)))
        self.roll_num.setText(self.timer_string.format(math.ceil(self.roll_ii+1)))
        if self.started:
            self.t -= self.delay/1000
            self.time_remaining.setText(self.tt_string.format(math.ceil(self.t)))
            if self.t<0:
                self.timer_zero(self.picture_ii,self.roll_ii)
                self.picture_ii+=1
                self.t = self.timer_fire
                if self.picture_ii>=4:
                    self.picture_ii=0
                    self.roll_ii+=1
                    self.started=False
                if self.roll_ii>=num_images_per_page:
                    self.roll_ii=0
                    

    def update_start(self):
        if self.started:
            self.start_button.setText('Stop')
        else:
            self.start_button.setText('Start')

    def start_timer(self,*args,**kwargs):
        self.started = True
        self.t = self.timer_start

#class SnapshotWidget(CustomWidget):
#    pass

class Photostrip(CustomWidget):
    def __init__(self,*args, **kwargs):
        super(Photostrip,self).__init__(*args, **kwargs)
    
        self.template = cv2.imread('template4.png',cv2.IMREAD_COLOR)
        self.template_height, self.template_width,self.template_depth = self.template.shape

        self.imagelabel = qw.QLabel()
        self.imagelabel.setMinimumSize(1, 1)
        self.imagelabel2 = qw.QLabel()
        self.imagelabel2.setMinimumSize(1, 1)
        layout = qw.QHBoxLayout()
        layout.addWidget(self.imagelabel)
        layout.addWidget(self.imagelabel2)
        self.setLayout(layout)

        self.strip_height = self.template_height+480*4
        self.strip_width = 640
        self.strip_depth = 3
        
        self.image = numpy.zeros((self.strip_height,self.strip_width,self.strip_depth))
        self.images = numpy.zeros((num_images_per_page,self.strip_height,self.strip_width,4),dtype=numpy.uint8)
        self.images[:,:,:,3]=255
#        self.ii = 0
        self.load_template()
        self.loadimage()

    def add_image(self,image,ii):
        y = self.template_height+ii*480
        self.image[y:y+480,:,:] = image
        self.loadimage()

    def load_template(self):
        self.image = numpy.zeros((self.strip_height,self.strip_width,self.strip_depth))
        self.image[:self.template_height,:self.template_width,:]=self.template

    def wind(self,ii,jj):
#        self.ii+=1
        if ii>=3:
            self.images[jj,:,:,:3]=self.image.copy()
            self.load_prev_strip(jj)
            self.save_image()
            self.load_template()
            if jj>=num_images_per_page-1:
                make_pdf.make_pdf2(make_pdf.reshape_images(self.images))
                
#            self.ii=0
    def snap(self,image,ii,jj):
        self.add_image(image,ii)
        self.wind(ii,jj)

    def save_image(self):
        path1 = os.path.expanduser('~')
        path2 = 'Desktop'
        path3 = 'images'
        path4 = str(time.time()).replace('.','_')+'.jpg'
        path = os.path.join(path1,path2,path3,path4)
        cv2.imwrite(path,self.image)
        
        
    def loadimage(self):
        qimage = simple_window.cv_to_qimage(self.image)
        pm = qg.QPixmap(qimage)
        pm = pm.scaled(self.imagelabel.width(),self.imagelabel.height(),1)
        self.imagelabel.setPixmap(pm)

    def load_prev_strip(self,jj):
        qimage = simple_window.cv_to_qimage(self.images[jj,:,:,:3])
        pm = qg.QPixmap(qimage)
        pm = pm.scaled(self.imagelabel.width(),self.imagelabel.height(),1)
        self.imagelabel2.setPixmap(pm)

#    def resizeEvent(self,event):
#        self.loadimage()

class Gui(qw.QWidget):
    def __init__(self):
        super(Gui,self).__init__()
        layout = qw.QHBoxLayout()
        
        self.snapshot_widget = simple_window.ImageWindow(self)
        self.control_widget = ControlWidget(self)
        self.photostrip = Photostrip(self)
        
        layout.addWidget(self.snapshot_widget)
        layout.addWidget(self.control_widget)
        layout.addWidget(self.photostrip)
        
        self.control_widget.timer_zero=self.snap

        self.setLayout(layout)
    def snap(self,ii,jj):
        self.photostrip.snap(self.snapshot_widget.image,ii,jj)

if __name__ == '__main__':
    
    app = qw.QApplication(sys.argv)
    iw = Gui()    
    iw.show()
    sys.exit(app.exec_())
