#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 09:41:11 2018

@author: hogwild
"""
import numpy as np
import os
import sys



def get_blocks(region, gap):
    R_y, R_x = region.shape
    i = 1
    blocks = []
    while i*gap < R_x:
        start = (i-1) * gap
        end = i * gap
        block = region[:,start:end]
        blocks.append(block)
        i += 1
    return blocks