#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 18:45:25 2018

@author: hogwild
"""
from PIL import Image
import pytesseract
#import numpy as np
import cv2

img1 = cv2.imread('./titles/100.png')
img2 = cv2.imread('./titles/301.png')


gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#ret, img = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
#img, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#new_contours = []
#for i in range(len(contours)):
#    cnt = contours[i]
#    area = cv2.contourArea(cnt)
#    if area > 500:
#        new_contours.append(cnt)
#cv2.drawContours(img2, new_contours, -1, (255, 255, 255), 1)
#cv2.imshow('img2',img2)
#cv2.waitKey()
#img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)
#img = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 5)
cv2.imshow('img2',img)
cv2.waitKey()
cv2.imwrite('test.png', img)

text = pytesseract.image_to_string(Image.open('test.png'), lang='chi_sim')
print(text.split())
s = ''.join(text.split())
print(s)
#cv2.imshow('img', img1)
cv2.imshow('img2', img)
cv2.waitKey()
cv2.destroyAllWindows()
