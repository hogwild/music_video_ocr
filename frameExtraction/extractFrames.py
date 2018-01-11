#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 10:57:27 2017

@author: xg7
"""
import numpy as np
import cv2 as cv


cap = cv.VideoCapture('../samples/011clip2.mov')
ret, frame = cap.read()
frame_old = cv.resize(frame, None, fx=0.25, fy=0.25, interpolation=cv.INTER_LINEAR)
gray_old = cv.cvtColor(frame_old, cv.COLOR_BGR2GRAY)

while(cap.isOpened()):
    ret, frame = cap.read()
    try:
        frame_new = cv.resize(frame, None, fx=0.25, fy=0.25, interpolation=cv.INTER_LINEAR)
        gray_new = cv.cvtColor(frame_new, cv.COLOR_BGR2GRAY)
        frame = gray_new - gray_old
#        print('type of frame:', type(frame))
#        input()
        gray_old = gray_new
        cv.imshow('frame', gray_new)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        break
    
cap.release()
cv.waitKey(1)
cv.destroyAllWindows()
cv.waitKey(1)
