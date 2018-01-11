#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 00:00:25 2018

@author: hogwild
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 20:48:59 2017

@author: Gu
"""
#from PIL import Image
#import pytesseract
import numpy as np
import cv2
from PIL import Image
import pytesseract


 
'''Region selection'''
def onmouse1(event,x,y,flags,param):
    global drag_start,sel
    workimg = np.copy(frame)
    if event == cv2.EVENT_LBUTTONDOWN:
        drag_start = x, y
        sel = 0,0,0,0
    elif drag_start:
        if flags and cv2.EVENT_FLAG_LBUTTON:           
            minpos = min(drag_start[0],x),min(drag_start[1],y)
            maxpos = max(drag_start[0],x),max(drag_start[1],y)
            sel = minpos[0],minpos[1],maxpos[0],maxpos[1]           
            cv2.rectangle(workimg,(sel[0],sel[1]),(sel[2],sel[3]),(0,0,255),2)
            cv2.imshow("frame",workimg)
        else:            
            print("Selection is completed.")
            drag_start = None
    
## load the music video
cap = cv2.VideoCapture('../samples/lishuangjiang.mkv')
sel = (0,0,0,0)
drag_start = None
count = 0
c1 = cv2.getStructuringElement(cv2.MORPH_RECT,(10, 8))
c2 = cv2.getStructuringElement(cv2.MORPH_RECT,(6, 6))
while(cap.isOpened()):
    ret, frame = cap.read() 
    try: ## avoid the bad ending of .mkv files
        cv2.imshow('frame', frame)
    except:
           break 
    if cv2.waitKey(1) & 0xFF == ord('q'): ## quit  
        break
    #### select the region of the subtitles:
    if cv2.waitKey(1) & 0xFF == ord('s'): ## select the region of the subtitles
        k = cv2.waitKey(1) & 0xFF
        cv2.setMouseCallback('frame', onmouse1, frame)
        while k != ord('d'):           ## when the region selection is done, press "d" to go on.
            k = cv2.waitKey(5) & 0xFF
        print("The region selected is: ", sel)
    if sel[0] != 0 and sel[3]!= 0:
        count += 1
        img_title = np.copy(frame[sel[1]:sel[3],sel[0]:sel[2],:])
        gray = cv2.cvtColor(img_title, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0) 
        ret, img = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        dilation = cv2.dilate(img, c2, iterations=1)
        img, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        new_contours = []
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if area > 500:
                new_contours.append(cnt)
        cv2.drawContours(img_title, new_contours, -1, (255, 255, 255), 1)
        gray = cv2.cvtColor(img_title, cv2.COLOR_BGR2GRAY)
        ret, img = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
#        img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 5)
#        canny = cv2.Canny(img, 10, 200)
#        sobel = cv2.Sobel(img, cv2.CV_8U, 1, 0, ksize=3)
        print("NO.:{} has {} words.".format(count, len(new_contours)))
        cv2.imshow('title', img)
        cv2.imwrite("./titles/{}.png".format(count), img)
cap.release()
cv2.waitKey(1)
cv2.destroyAllWindows()
cv2.waitKey(1)
        
    #### detect the rhythm:
for i in range(1, 5456):    
    text = pytesseract.image_to_string(Image.open('./titles/{}.png'.format(i)), lang='chi_sim')
    print(text.split())
    s = ''.join(text.split())
    print(s)
    
    
    

        

 


       


