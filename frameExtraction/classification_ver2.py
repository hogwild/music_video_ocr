#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 19:00:39 2018

@author: hogwild
"""

import os
import shutil
import numpy as np
from sklearn.cluster import KMeans
#import matplotlib.pyplot as plt
#from pywt import WaveletPacket2D
from skimage.feature import local_binary_pattern
import cv2

Num_Img = 1000
DIR = './titles/'
pos = './pos_examples'
neg = './neg_examples'
file_list = os.listdir(DIR)
samples = np.zeros((Num_Img, 256))
radius = 1
n_points = 8 * radius



for i in range(Num_Img): 
    print(file_list[i])
    img_title = cv2.imread(DIR+file_list[i])
    gray = cv2.cvtColor(img_title, cv2.COLOR_BGR2GRAY)
    lbp = local_binary_pattern(gray, n_points, radius)
    max_bins = int(lbp.max() + 1)
    samples[i], _ = np.histogram(lbp, normed=True, bins=max_bins, range=(0, max_bins))
#    plt.subplot(131)
#    plt.imshow(img_title)
#    plt.subplot(132)
#    plt.imshow(gray)
#    plt.subplot(133)
#    plt.imshow(lbp, cmap='gray')
#    plt.show
    


#samples = np.array(samples)
kmeans = KMeans(n_clusters=2, random_state=0).fit(samples)
l = kmeans.labels_
for i in range(Num_Img):
    if l[i] == 1:
        shutil.copy(DIR+file_list[i], pos)
    else:
        shutil.copy(DIR+file_list[i], neg)

# Show level 1 nodes
#    fig = plt.figure()
#    for i, p2 in enumerate(path):
#        ax = fig.add_subplot(2, 2, i + 1)
#        ax.imshow(np.sqrt(np.abs(wp2[p2].data)), origin='upper',
#              interpolation="nearest", cmap=plt.cm.gray)
#        ax.set_title(p2)
#
#    for p1 in path:
#        fig = plt.figure()
#        for i, p2 in enumerate(path):
#            ax = fig.add_subplot(2, 2, i + 1)
#            p1p2 = p1 + p2
#            ax.imshow(np.sqrt(np.abs(wp2[p1p2].data)), origin='image',
#                  interpolation="nearest", cmap=plt.cm.gray)
#            ax.set_title(p1p2)
#
#    fig = plt.figure()
#    i = 1
#    for row in wp2.get_level(2, 'freq'):
#        for node in row:
#            ax = fig.add_subplot(len(row), len(row), i)
#            ax.set_title("%s=(%s row, %s col)" % (
#                     (node.path,) + wp2.expand_2d_path(node.path)))
#            ax.imshow(np.sqrt(np.abs(node.data)), origin='image',
#                  interpolation="nearest", cmap=plt.cm.gray)
#            i += 1
#
#    plt.show()