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
frame_old = cv.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv.INTER_LINEAR)
gray_old = cv.cvtColor(frame_old, cv.COLOR_BGR2GRAY)
gray_old = cv.GaussianBlur(gray_old, (5, 5), 0)
canny_old = cv.Canny(gray_old, 50, 150)
mask_old = canny_old > 0
while(cap.isOpened()):
    ret, frame = cap.read()
    
    try:
        frame = cv.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv.INTER_LINEAR)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (5, 5), 0)
        canny = cv.Canny(gray, 50, 150)
        mask = canny > 0
        mask[mask_old] = False
        frame[:,:,0][mask] = 255
        frame[:,:,1][mask] = 0
        frame[:,:,2][mask] = 0
#        frame[:,:,0][mask_old] = 0
#        frame[:,:,1][mask_old] = 0
#        frame[:,:,2][mask_old] = 255
        mask_old = mask
#        mask_color = np.stack((mask, mask, mask), 2)
#        frame[mask_color] = 255
        cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    except (Exception) as e:
        print(e)
        break
    
cap.release()
cv.waitKey(1)
cv.destroyAllWindows()
cv.waitKey(1)
