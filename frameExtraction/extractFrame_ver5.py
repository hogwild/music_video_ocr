# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 20:48:59 2017

@author: Gu
"""


import numpy as np
import cv2
#==============================================================================
# To install opencv3.x with anaconda:
# $conda config --add channels conda-forge
# $conda install opencv
#==============================================================================

## Color scheme 1: BLUE
B = (100, 250)
G = (65, 50)
R = (50, 50)

## Color scheme 2: RED
#B = (50, 50)
#G = (65, 50)
#R = (100, 250)

## Threshold
T = (0.2, 0.5)

## switch for saving the new video
SAVE = True

## switch for color or gray 
COLOUR = False



## load the video
cap = cv2.VideoCapture('../samples/011clip2.mov')
 
## build the background subtractor instance
fgbg = cv2.createBackgroundSubtractorKNN()
#fgbg = cv2.createBackgroundSubtractorMOG2()

## prepare for saving the generated video 
if SAVE:
    ret, frame = cap.read()
#    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (np.size(frame, 1), np.size(frame, 0)))

## processing the video
while(cap.isOpened()):
    ret, frame = cap.read()
    try:
#        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) ## convert to gray image
        gray_2 = cv2.GaussianBlur(gray, (3, 3), 0) ## smooth 
        fgmask = fgbg.apply(gray_2)
        bgmask = fgmask == 0 ## get the mask of backgroud
        if COLOUR:
            f = frame
        else:
            f = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
        gray[bgmask] = 0 ## remove the background on the gray image
        
        ## The masks for the degenerating process
        mask_mid = gray > np.max(gray)*T[0]
        mask_top = gray > np.max(gray)*T[1]
        
        ## replace the colors
        f[:,:,0][mask_mid] = B[0]
        f[:,:,1][mask_mid] = G[0]
        f[:,:,2][mask_mid] = R[0]
        
        f[:,:,0][mask_top] = B[1]
        f[:,:,1][mask_top] = G[1]
        f[:,:,2][mask_top] = R[1]
        
        if SAVE:
            out.write(f)
        cv2.imshow('frame', f)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
    except (Exception) as e:
        print(e)
        break               
cap.release()
if SAVE:
    out.release()
cv2.waitKey(1)
cv2.destroyAllWindows()
cv2.waitKey(1)

