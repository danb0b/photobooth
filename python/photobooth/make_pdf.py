# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 20:15:07 2019

@author: danaukes
"""


import numpy
import cairo
import math
import time
import os

def make_pdf(image):
    height, width, channels = image.shape
    imagesurface = cairo.ImageSurface.create_for_data(image, cairo.FORMAT_RGB24, width, height)
    
    paper_width = 8.5
    paper_height = 11
    margin = .25
    
    point_to_inches= 72
    image_scaling = 300
    
    pdfname = "out.pdf" 
    pdf = cairo.PDFSurface( pdfname, 
                            paper_width*point_to_inches, 
                            paper_height*point_to_inches
                            )
    
    cr = cairo.Context(pdf)
    
    scaling = point_to_inches/image_scaling
    
    cr.save()
    cr.scale(scaling , scaling)
    cr.set_source_surface(imagesurface, margin*point_to_inches/scaling, margin*point_to_inches/scaling)
    cr.paint()
    cr.restore()
    
    pdf.show_page()
    pdf.finish()

def reshape(image):
    image = image.transpose(1,0,2)
    image = image[:,-1::-1,:]
    image = image.copy()
    return image

def reshape_images(images):
    images = images.transpose(0,2,1,3)
    images = images[:,:,-1::-1,:]
    images = images.copy()
    return images

def make_pdf2(images):
    num, height, width, channels = images.shape
    surfaces = []
    for image in images:
        surfaces.append(cairo.ImageSurface.create_for_data(image, cairo.FORMAT_RGB24, width, height))
    
    paper_width = 8.5
    paper_height = 11
    margin = .25
    
    point_to_inches= 72
    image_scaling = 300
    
    
    path1 = os.path.expanduser('~')
    path2 = 'Desktop'
    path3 = 'pdf'
    path4 = str(time.time()).replace('.','_')+'.pdf'
    path = os.path.join(path1,path2,path3,path4)
    
    pdfname = path
    pdf = cairo.PDFSurface( pdfname, paper_width*point_to_inches, paper_height*point_to_inches)
    
    cr = cairo.Context(pdf)
    
    scaling = point_to_inches/image_scaling
    
    for ii,imagesurface in enumerate(surfaces):
        cr.save()
        cr.scale(scaling , scaling)
        cr.set_source_surface(imagesurface, margin*point_to_inches/scaling, (margin+ii*(2.75))*point_to_inches/scaling)
        cr.paint()
        cr.restore()
    
    pdf.show_page()
    pdf.finish()
    
if __name__=='__main__':
    width = 640
    height = 2400

    image = numpy.zeros((height,width,4),dtype = numpy.uint8)
    image[:,:,0]   = 0
    image[:,:,1]   = 0
    image[:,:,2]   = 255
    image[:,:,3]   = 255
    #image[:,:,(3)]   =1
    make_pdf(reshape(image))
    
#    height, width, channels = image.shape
#    imagesurface = cairo.ImageSurface.create_for_data(image, cairo.FORMAT_RGB24, width, height)
