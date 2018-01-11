# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 20:48:59 2017

@author: Gu
"""

import numpy as np
import cv2
 
cap = cv2.VideoCapture('../samples/lishuangjiang.mkv')
 
fgbg = cv2.createBackgroundSubtractorKNN()
#fgbg = cv2.createBackgroundSubtractorMOG2()
ret, frame_old = cap.read()
frame_old = cv2.resize(frame_old, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
gray_old = cv2.cvtColor(frame_old, cv2.COLOR_BGR2GRAY)
gray_old = cv2.GaussianBlur(gray_old, (3, 3), 0)
fgmask_old = fgbg.apply(gray_old) 
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (np.size(frame_old, 1), np.size(frame_old, 0)))
while(cap.isOpened()):
    ret, frame = cap.read()
    try:
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        fgmask = fgbg.apply(gray) 
        mask = fgmask == 0
        f = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
#        f_new = fgmask > 0
#        diff = (fgmask - fgmask_old) > 0 
        gray[mask] = 0
        mask_top = gray > np.max(gray)*0.5
        
        mask_mid = gray > np.max(gray)*0.2
        f[:,:,0][mask_mid] = 50#gray[mask]
        f[:,:,1][mask_mid] = 255#gray[mask]
        f[:,:,2][mask_mid] = 255#gray[mask]
        
        f[:,:,0][mask_top] = 255#gray[mask]
        f[:,:,1][mask_top] = 100#gray[mask]
        f[:,:,2][mask_top] = 150#gray[mask]
#        frame[:,:,0][diff] = 255
#        frame[:,:,1][diff] = 0
#        frame[:,:,1][fgmask_old>0] = 0
#        frame[:,:,2][fgmask_old>0] = 255
#        f = (gray-gray_old) > 0
#        frame[:,:,0][diff] = (gray-gray_old)[diff] 
#        frame[:,:,1][diff] = (gray-gray_old)[diff] 
#        frame[:,:,2][diff] = (gray-gray_old)[diff] 
        
        cv2.imshow('frame', f)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        fgmask_old = fgmask
#        gray_old = gray
        
    except (Exception) as e:
        print(e)
        break               
cap.release()
#out.release()
cv2.waitKey(1)
cv2.destroyAllWindows()
cv2.waitKey(1)

