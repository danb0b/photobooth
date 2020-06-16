# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 19:58:29 2019

@author: danaukes
"""

import numpy
import cv2
#import math
#from math import pi
#import matplotlib.pyplot as plt
#video_capture = cv2.VideoCapture(0)
#import PyQt5.QtGui as qg
#import PyQt5.QtWidgets as qw
#import PyQt5.QtCore as qc
#import sys
#import time


cams_test = 10
for i in range(-1, cams_test):
    cap = cv2.VideoCapture(i)
    test, frame = cap.read()
    print("i : "+str(i)+" /// result: "+str(test))