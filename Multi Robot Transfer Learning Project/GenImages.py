# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 23:09:13 2017

@author: AdityaPMishra
"""

import numpy as np  
import matplotlib.pyplot as plt
from PIL import Image

dFile = np.loadtxt(fname="imagesloop1.txt",dtype=np.uint8,delimiter=',')
for i in range(len(dFile)):
    inp = dFile[i]
    inp.resize([128,128,3])
    im = Image.fromarray(inp)
    if(i%8 == 0):
        im=im.rotate(45)
    elif(i%6 == 0):
        im=im.rotate(90)
    elif(i%4 == 0):
        im=im.rotate(135)
    elif(i%2 == 0):
        im=im.rotate(180)
    im.save("‪track1_"+str(i)+".jpeg")

dFile = np.loadtxt(fname="imagesloop2.txt",dtype=np.uint8,delimiter=',')
for i in range(len(dFile)):
    inp = dFile[i]
    inp.resize([128,128,3])
    im = Image.fromarray(inp)
    if(i%8 == 0):
        im=im.rotate(45)
    elif(i%6 == 0):
        im=im.rotate(90)
    elif(i%4 == 0):
        im=im.rotate(135)
    elif(i%2 == 0):
        im=im.rotate(180)
    im.save("‪track2_"+str(i)+".jpeg")