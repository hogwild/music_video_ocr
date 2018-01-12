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
    global drag_start, sel
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
cap = cv2.VideoCapture('../samples/liudehua.mkv')
sel = (0,0,0,0)
drag_start = None
count = 0
c1 = cv2.getStructuringElement(cv2.MORPH_RECT,(10, 8))
c2 = cv2.getStructuringElement(cv2.MORPH_RECT,(16, 14))
ret, frame = cap.read()
Y, X, Z = frame.shape
LINE_GAP = 10
region = (0, 0, 0, 0)
one_char = (0, 0, 0, 0)
char_with_gap = (0, 0, 0, 0)
blocks = []
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
        while k != ord('d'):          ## when the region selection is done, press "d" to go on.
            k = cv2.waitKey(5) & 0xFF
        region = sel[:]
        print("The region is: ", region)
        while k != ord('f'):
            k = cv2.waitKey(5) & 0xFF
            one_char = sel[:]
        print("The size of one character is: {}".format(one_char))
        while k != ord('g'):
            k = cv2.waitKey(5) & 0xFF
            char_with_gap = sel[:]
        print("The size of gap is: {}".format(char_with_gap))
   
    if sum(region) > 0:    
        count += 1
        GAP = char_with_gap[2] - one_char[2]
        LEFT_BOUND = region[0] - int(GAP/2)
        RIGHT_BOUND = region[2] + int(GAP/2)
        UP_BOUND = region[1]
        LOW_BOUND = region[3]
        CHAR_WIDTH = one_char[2] - one_char[0] + GAP
        MID = int((LOW_BOUND - UP_BOUND)/2)
        img_title = np.copy(frame[UP_BOUND:LOW_BOUND, LEFT_BOUND:RIGHT_BOUND, :])
        gray = cv2.cvtColor(img_title, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
#        half = gray[:MID, :]
    ### draw the white lines
        i = 1
        while i*CHAR_WIDTH < RIGHT_BOUND - LEFT_BOUND:
            start = (i-1) * CHAR_WIDTH
            end = i * CHAR_WIDTH
            blocks.append(gray[:MID, start:end])
            cv2.imwrite("./titles/{}_{}.png".format(count, i), gray[:MID, start:end])
            cv2.imshow('chinese-char', gray[:MID, start:end])
#            gray[:, i*CHAR_WIDTH] = 255
            i += 1
   

        
#        cv2.imwrite("./titles/{}.png".format(count), gray)
        
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


