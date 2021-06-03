import pandas as pd
import numpy
from scipy.spatial import KDTree
from scipy import spatial
import itertools
from PIL import Image
import os
from scipy.stats import skew
output = []

def removeNestings(l):
    for i in l:
        if type(i) == list:
            removeNestings(i)
        else:
            output.append(i)

P = list(range(0,1001,1))
Q = list(range(0,201,1))
Z = list(range(0,1001,5))

X_CORD = [Q for n in P]
removeNestings(X_CORD)
Y_CORD = [i for i in P for n in Q]
R_VALUE = [i for i in Z for n in range(0,1001,1)]

TOTAL = pd.DataFrame(list(zip(output,Y_CORD,R_VALUE)), columns = ["X","Y","Value"])
print(TOTAL)

RED = 0
GREEN = 1              # Presets for colour values in img with PIL
BLUE = 2
HEATMAP_CHANNEL = RED
HEATMAP_SENS_CHANNEL = RED # Colour of choice to display heatmaps
HM_LOW_VAL = 0         # Lowest value for showing on the heatmap
HM_HIGH_VAL = 1000
HM_HIGH_VAL_SENS = 2000

minX, maxX = int(TOTAL['X'].min()), int(TOTAL['X'].max())
minY, maxY = int(TOTAL['Y'].min()), int(TOTAL['Y'].max())
minN, maxN = TOTAL['Value'].min(), TOTAL['Value'].max()

def setColour(row):
# Determine the pixel colour for the heatmap based on the KNN value
    x, y, n = int(row['X']),int(row['Y']), int(row['Value'])
# Values can't be lower than the value that makes it black or higher than the full 255
    colour = min(max(0, n - HM_LOW_VAL),HM_HIGH_VAL - HM_LOW_VAL)
# Apply the colour as a proportion of 255
    colour = int (255 * colour / (HM_HIGH_VAL - HM_LOW_VAL))
    r = pixels[x, y][0]
    g = pixels[x, y][1]
    b = pixels[x, y][2]
# Update the selected channel
    if HEATMAP_CHANNEL == RED: r = colour
    elif HEATMAP_CHANNEL == GREEN: g = colour
    elif HEATMAP_CHANNEL == BLUE: b = colour
    pixels[x, y] = (r, g, b)

img = Image.new(mode='RGB',size=(maxX + 1, maxY + 1))
pixels = img.load()
TOTAL.apply(setColour, axis=1)
rotate_img = img.rotate(180)
# Save the image
rotate_img.save("Your directory.png")
