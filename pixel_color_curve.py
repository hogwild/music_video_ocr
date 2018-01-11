import os
import sys
from time import localtime as imgtime
import cv2 as cv
import numpy as np
import tkinter as Tk
import argparse
import matplotlib.pyplot as plt

'''pickout the images'''
def getImgAtClock(path,time_hour):
    files = os.listdir(path)
    year = 0
    month = 0
    day = 0
    imgAtclock =[];
    for imgName in files:
        if imgName[-3:]=='JPG':
           imginfo = os.stat(path+"/"+imgName)
           timeAttribution = imgtime(imginfo.st_mtime)
           clock = timeAttribution.tm_hour
           n_year = timeAttribution.tm_year
           n_month = timeAttribution.tm_mon
           n_day = timeAttribution.tm_mday
           if clock == time_hour and (year!=n_year or month!=n_month or day!=n_day):
               imgAtclock.append(imgName)
               year = n_year
               month = n_month
               day = n_day
    return imgAtclock

'''Directory checking'''
def make_dir(source,target):
    s_dir=source.get()
    t_dir=target.get()
    if os.path.isdir(s_dir):
        print("Source folder is OK.")
    else:
        print("The source directory doesn't exist. Please check the path.")
        sys.exit()
    if os.path.isdir(t_dir):
        print("Warning: Saving folder exist. Recorders in it may be covered.")
    else:
        os.makedirs(t_dir)
        print("New saving folder is created.")
       
'''Region selection'''
def onmouse1(event,x,y,flags,param):
    global drag_start,sel
    workimg=np.copy(img)
    if event == cv.EVENT_LBUTTONDOWN:
        drag_start = x, y
        sel = 0,0,0,0
    elif drag_start:
        if flags and cv.EVENT_FLAG_LBUTTON:           
            minpos = min(drag_start[0],x),min(drag_start[1],y)
            maxpos = max(drag_start[0],x),max(drag_start[1],y)
            sel = minpos[0],minpos[1],maxpos[0],maxpos[1]           
            cv.rectangle(workimg,(sel[0],sel[1]),(sel[2],sel[3]),(0,0,255),2)
            cv.imshow("img",workimg)
        else:            
            print("Selection is completed.")
            drag_start = None


'''Set the directory'''
folder=open("./folder.txt",'r')
line= folder.readline()
while line:
    f=line.split()
    if f[0]=='Source':
        image_folder = f[2]
    elif f[0]=='Saving':
        save_folder = f[2]
    line= folder.readline()
folder.close()
     
window = Tk.Tk()
win0 = Tk.Frame(window,border=4)
win0.pack(side='top',anchor='w')
win1 = Tk.Frame(window,border=4)
win1.pack(side='top',anchor='w')
win2 = Tk.Frame(window,border=4)
win2.pack(side='top',anchor='w')
 
Source = Tk.StringVar(window,image_folder)
Tk.Label(win0,text='Read from').pack(side='left')
Tk.Entry(win0,width=50,textvariable=Source).pack()
 
Target = Tk.StringVar(window,save_folder)
Tk.Label(win1,text='Save to      ').pack(side='left')
Tk.Entry(win1,width=50,textvariable=Target).pack()

Tk.Button(win2,text='Check Folder',padx=8,command=lambda source=Source, target=Target:make_dir(source,target)).pack(side='left') 
Tk.Button(win2,text='OK',padx=8,command= window.destroy).pack(side='right')
window.mainloop()

image_folder = Source.get()
if image_folder[-1]!='/':
    image_folder += '/'
save_folder = Target.get()
if save_folder[-1]!='/':
    save_folder+='/'
folder = open('./folder.txt','w')
folder.write('Source folder: '+image_folder+' \n')
folder.write('Saving folder: '+save_folder+' \n')
folder.close()

'''pick out the image at a given time, clock'''
filename_list = getImgAtClock(image_folder,10)
print("The images are from: "+image_folder+'\n')
print("The results will be saved to: "+save_folder+'\n')

'''Initialization of the parameters'''
col_range = 0.1 #control the upper and lower boundry of the color
region_range_x = 1 #control the size of the ellipse
region_range_y = 1 #control the size of the ellipse
centroid=[0,0] #initial value of the centroid of the ellipse
sample_color_pos=[]
last_sample_color_pos=[]
    
parser = argparse.ArgumentParser(description = "Tree images")
parser.add_argument("-i","--input",default = image_folder,help="Input directory.")
args = parser.parse_args()
path = args.input
j=0 ##counts the number of the images
b=np.zeros(len(filename_list))
g=np.zeros(len(filename_list))
r=np.zeros(len(filename_list))
for imgName in filename_list:
    image = path+imgName
    if j==0:
        img = cv.imread(image)
        img = cv.resize(img,(1200,900))
        set_region = input('Would you like to set the region by hand, yes or no ?  ')
        if set_region.lower() in ['y','Y','yes','Yes','YES']:
            sel = range(4)
            sel[0] = int(input('Please input x1:   '))
            sel[1] = int(input('Please input y1:   '))
            sel[2] = int(input('Please input x2:   '))
            sel[3] = int(input('Please input y2:   '))            
        else:
            print("Press 'b' when the region selection is completed.")
            cv.namedWindow("img",1)
            cv.setMouseCallback("img", onmouse1,img)
            sel = (0,0,0,0)
            drag_start = None
            is_img = True
            while (1):
                if is_img:
                    cv.imshow("img",img)
                else:
                    cv.imshow("img",img2)
                k = cv.waitKey(20)&0xFF
                if k == ord('b'):
                    break
                else:#if k == ord('a'):
                    is_img = False
                    img2 = np.copy(img)
                    cv.rectangle(img2,(sel[0],sel[1]),(sel[2],sel[3]),(0,0,255),2)
                    cv.imshow("img",img2)                
            cv.destroyAllWindows()        
        print("The region selected is: ",sel)
##        patch = img[sel[1]:sel[3],sel[0]:sel[2]]
##        centroid = np.array(((sel[3]-sel[1])/2.0,(sel[2]-sel[0])/2.0))
##        print "The centroid is: ",centroid
        '''take the color velue of the region center'''
        b[j]=img[sel[1]+(sel[3]-sel[1])/2,sel[0]+(sel[2]-sel[0])/2,0]
        g[j]=img[sel[1]+(sel[3]-sel[1])/2,sel[0]+(sel[2]-sel[0])/2,1]
        r[j]=img[sel[1]+(sel[3]-sel[1])/2,sel[0]+(sel[2]-sel[0])/2,2]
    else:
        img = cv.imread(image)
        img = cv.resize(img,(1200,900))
        b[j]=img[sel[1]+(sel[3]-sel[1])/2,sel[0]+(sel[2]-sel[0])/2,0]
        g[j]=img[sel[1]+(sel[3]-sel[1])/2,sel[0]+(sel[2]-sel[0])/2,1]
        r[j]=img[sel[1]+(sel[3]-sel[1])/2,sel[0]+(sel[2]-sel[0])/2,2]
    j+=1

'''display the RGB'''
x = np.arange(1,b.size+1,1)
##plt.plot(x,b,'bo',x,g,'g^',x,r,'rs')
plt.figure(1)
plt.subplot(311)
plt.ylabel('Channel B')
plt.xlabel('Days')
plt.plot(x,b,x,b,'bo')

plt.subplot(312)
plt.ylabel('Channel G')
plt.xlabel('Days')
plt.plot(x,g,x,g,'g^')

plt.subplot(313)
plt.ylabel('Channel R')
plt.xlabel('Days')
plt.plot(x,r,x,r,'rs')
plt.show()
