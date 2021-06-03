import pandas as pd
import numpy as np
from scipy.spatial import KDTree
from scipy import spatial
from PIL import Image
import PIL as PIL
import os
import matplotlib.pyplot as plt
from scipy.stats import skew

output = []

def removeNestings(l):
    for i in l:
        if type(i) == list:
            removeNestings(i)
        else:
            output.append(i)

Q = list(range(0,1001,1))
P = list(range(0,521,1))
Z = list(range(-255,256,1))

X_CORD = [Q for n in P]
removeNestings(X_CORD)
Y_CORD = [i for i in P for n in Q]
R_VALUE = [i for i in Z for n in range(0,1001,1)]

print(len(X_CORD))
print(len(Y_CORD))
print(len(R_VALUE))

TOTAL = pd.DataFrame(list(zip(output,Y_CORD,R_VALUE)), columns = ["X","Y","Value"])

TOTAL['Value'] = TOTAL.Value.fillna(0)

minX, maxX = int(TOTAL['X'].min()), int(TOTAL['X'].max())
minY, maxY = int(TOTAL['Y'].min()), int(TOTAL['Y'].max())

def setColour(row):
# Determine the pixel colour for the heatmap based on the KNN value
    x, y, n = int(row['X']),int(row['Y']), int(row['Value'])
# Values can't be lower than the value that makes it black or higher than the full 255
    if n>0: # red
        val = abs(n)
        pixels[x,y] = (val,0,0)
    elif n<0:
        val = abs(n)
        pixels[x,y] = (0,val,0)
    else:
        pixels[x,y] = (0,0,0)

img = Image.new(mode='RGB',size=(maxX +1 , maxY+1 ))
pixels = img.load()
TOTAL.apply(setColour, axis=1)
img.show()
img.save("Your directory.png")
