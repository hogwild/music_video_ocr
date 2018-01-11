# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 20:48:59 2017

@author: Gu
"""
#from PIL import Image
#import pytesseract
import numpy as np
import cv2



 
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
cap = cv2.VideoCapture('../samples/jasmine.mkv')
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
            if area > 2000:
                new_contours.append(cnt)
        cv2.drawContours(img_title, contours, -1, (0, 0, 255), 3)
#        img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 5)
#        canny = cv2.Canny(img, 10, 200)
#        sobel = cv2.Sobel(img, cv2.CV_8U, 1, 0, ksize=3)
        print("NO.:{} has {} words.".format(count, len(contours)))
        cv2.imshow('title', img_title)
#        cv2.imwrite("./titles/{}.png".format(count), img_title)
        
    #### detect the rhythm:
    
    
    

        
cap.release()
cv2.waitKey(1)
cv2.destroyAllWindows()
cv2.waitKey(1)
 
#cv2.namedWindow('img', 1)
#cv2.setMouseCallback('img', onmouse1, frame) 
#sel = (0,0,0,0)
#drag_start = None
#cv2.imshow("img",frame)
#k = cv2.waitKey(20)&0xFF


#while True:
#    cv2.imshow("img",frame)
#    k = cv2.waitKey(20)&0xFF
#    if k == ord('b'):
#        break
#    else:#if k == ord('a'):
#        cv2.rectangle(frame,(sel[0],sel[1]),(sel[2],sel[3]),(0,0,255),1)
#        cv2.imshow("img",frame)    
#        cv2.destroyAllWindows()        
#print("The region selected is: ",sel)
#for imgName in filename_list:
#    image = path+imgName
#    if j==0:
#        img = cv.imread(image)
#        img = cv.resize(img,(1200,900))
#        set_region = raw_input('Would you like to set the region by hand, yes or no ?  ')
#        if set_re gion.lower() in ['y','Y','yes','Yes','YES']:
#            sel = range(4)
#            sel[0] = int(input('Please input x1:   '))
#            sel[1] = int(input('Please input y1:   '))
#            sel[2] = int(input('Please input x2:   '))
#            sel[3] = int(input('Please input y2:   '))            
#        else:
#            print("Press 'b' when the region selection is completed.")
#            cv2.namedWindow("img",1)
#            cv2.setMouseCallback("img", onmouse1,img)
#            sel = (0,0,0,0)
#            drag_start = None
#            is_img = True
#            while (1):
#                if is_img:
#                    cv2.imshow("img",img)
#                else:
#                    cv2.imshow("img",img2)
#                k = cv2.waitKey(20)&0xFF
#                if k == ord('b'):
#                    break
#                else:#if k == ord('a'):
#                    is_img = False
#                    img2 = np.copy(img)
#                    cv2.rectangle(img2,(sel[0],sel[1]),(sel[2],sel[3]),(0,0,255),2)
#                    cv2.imshow("img",img2)                
#            cv2.destroyAllWindows()        
#        print("The region selected is: ",sel)
##        patch = img[sel[1]:sel[3],sel[0]:sel[2]]
##        centroid = np.array(((sel[3]-sel[1])/2.0,(sel[2]-sel[0])/2.0))
##        print "The centroid is: ",centroid
#        '''take the color velue of the region center'''
#        b[j]=img[sel[1]+(sel[3]-sel[1])/2,sel[0]+(sel[2]-sel[0])/2,0]
#        g[j]=img[sel[1]+(sel[3]-sel[1])/2,sel[0]+(sel[2]-sel[0])/2,1]
#        r[j]=img[sel[1]+(sel[3]-sel[1])/2,sel[0]+(sel[2]-sel[0])/2,2]
#    else:
#        img = cv2.imread(image)
#        img = cv2.resize(img,(1200,900))
#        b[j]=img[sel[1]+(sel[3]-sel[1])/2,sel[0]+(sel[2]-sel[0])/2,0]
#        g[j]=img[sel[1]+(sel[3]-sel[1])/2,sel[0]+(sel[2]-sel[0])/2,1]
#        r[j]=img[sel[1]+(sel[3]-sel[1])/2,sel[0]+(sel[2]-sel[0])/2,2]
#    j+=1


 

#while(cap.isOpened()):
#    ret, frame = cap.read()     
#    cv2.imshow('frame', frame)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
#        


