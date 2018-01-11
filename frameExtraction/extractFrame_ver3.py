# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 20:48:59 2017

@author: Gu
"""

import numpy as np
import cv2
 
cap = cv2.VideoCapture('../samples/011clip2.mov')
 
fgbg = cv2.createBackgroundSubtractorKNN()
#fgbg = cv2.createBackgroundSubtractorMOG2()
ret, frame = cap.read()
frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (np.size(frame, 1), np.size(frame, 0)))
while(cap.isOpened()):
    ret, frame = cap.read()
    try:
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
        fgmask = fgbg.apply(frame)
#        mask_1 = fgmask > 0
#        mask_2 = fgmask >200
#        mask_3 = fgmask == 255
##        print(fgmask)
##        input('wait:')
##        mask = fgmask > 0
#        frame[:,:,0][mask_1] = 0
#        frame[:,:,1][mask_1] = 255
#        frame[:,:,2][mask_1] = 0
#        frame[:,:,0][mask_2] = 255
#        frame[:,:,1][mask_2] = 0
#        frame[:,:,2][mask_2] = 0
#        frame[:,:,0][mask_3] = 0
#        frame[:,:,1][mask_3] = 0
#        frame[:,:,2][mask_3] = 255
        
#        out.write(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except (Exception) as e:
        print(e)
        break               
cap.release()
out.release()
cv2.waitKey(1)
cv2.destroyAllWindows()
cv2.waitKey(1)

