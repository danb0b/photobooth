# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 19:23:49 2014

@author: danb0b
"""

import cv2
import numpy
import numpy.random as nr
filename = 'test.avi'
fps = 1
frame_size = (400,300)
#load your frames
frames = numpy.uint8(nr.randint(0,255,(100,300,400)))
#create a video writer
writer = cv2.VideoWriter(filename, -1, 25, frame_size )
#and write your frames in a loop if you want
for frame in frames:
    print(frame.shape)
    writer.write(frame)
writer.release()