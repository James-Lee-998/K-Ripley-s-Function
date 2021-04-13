import pandas as pd
import numpy
from scipy.spatial import KDTree
from scipy import spatial
from PIL import Image
import PIL as PIL
import os
import sys
from progressbar import ProgressBar

RED = 0
GREEN = 1
BLUE = 2
HEATMAP_CHANNEL = RED
HEATMAP_SENS_CHANNEL = RED
HM_LOW_VAL = 0
HM_HIGH_VAL_SENS = 1000
HM_HIGH_VAL = 1000
HEATMAP_SENS_CHANNEL_CYT = GREEN
LIST_of_LISTS = {'DIR_HOME':[],'THRESHOLD': [], 'SEARCH_RADIUS': [],'KNN':[],'KNN_SELF':[],'PIXEL_LOSS':[]}


PATH, THRESH, RADI = sys.argv[1], sys.argv[2], sys.argv[3]

THRESHOLD = int(THRESH)
THRESHOLD_CYT = 700
SEARCH_RADIUS = int(RADI)

def setColour(row):
# Determine the pixel colour for the heatmap based on the KNN value
    x, y, n = int(row['X']),int(row['Y']), int(row['Neighbours'])
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
    pixels[x, y] = (r, 0, 0)

def setColour_SENS(row):
# Same as above but base Red Channel on Pixel value not KNN
    x, y, n = int(row['X']),int(row['Y']), int(row['Value'])
    colour = min(max(0, n - HM_LOW_VAL),HM_HIGH_VAL_SENS - HM_LOW_VAL)
    colour = int (255 * colour / (HM_HIGH_VAL_SENS - HM_LOW_VAL))
    r = pixels[x, y][0]
    g = pixels[x, y][1]
    b = pixels[x, y][2]
    if HEATMAP_SENS_CHANNEL == RED: r = colour
    elif HEATMAP_SENS_CHANNEL == GREEN: g = colour
    elif HEATMAP_SENS_CHANNEL == BLUE: b = colour
    pixels[x, y] = (r, g, b)

def setColour_SENS_CYT(row):
# Same as above but base Red Channel on Pixel value not KNN
    x, y, n = int(row['X']),int(row['Y']), int(row['Value'])
    colour = min(max(0, n - HM_LOW_VAL),HM_HIGH_VAL_SENS - HM_LOW_VAL)
    colour = int (255 * colour / (HM_HIGH_VAL_SENS - HM_LOW_VAL))
    r = pixels[x, y][0]
    g = pixels[x, y][1]
    b = pixels[x, y][2]
    if HEATMAP_SENS_CHANNEL_CYT == RED: r = colour
    elif HEATMAP_SENS_CHANNEL_CYT == GREEN: g = colour
    elif HEATMAP_SENS_CHANNEL_CYT == BLUE: b = colour
    pixels[x, y] = (r, g, b)

def setColour_RATIO(row):
# Determine the pixel colour for the heatmap based on the KNN value
    x, y, n, s = int(row['X']),int(row['Y']), int(row['Neighbours']), int(row['Self-neighbours'])
# Values can't be lower than the value that makes it black or higher than the full 255
    if n>s: # red
        colour = (n-s)/(n+s)
        val = round(int(255 * colour))
        pixels[x,y] = (0,val,0)
    elif n<s:
        colour = (n-s)/(n+s)
        val = abs(round(int(255 * colour)))
        pixels[x,y] = (val,0,0)
    elif n==s:
        if n+s == 0:
            pixels[x,y] = (255,255,255)
        else:
            pixels[x,y] = (0,0,0)

def countNeighbours(row):
    # Method to count number of KNN per pixel value of PROTEIN
    if row['ValuePROT'] <= int(THRESHOLD): # only calculates this metric if the pixel value at row is above the agreed threshold
            return 0
    else:
            return len(kdCYT.query_ball_point([row['X'],row['Y']],int(SEARCH_RADIUS)))

def countNeighbours_self(row):
    # Method to count number of KNN per pixel value of PROTEIN
    if row['ValuePROT'] <= int(THRESHOLD): # only calculates this metric if the pixel value at row is above the agreed threshold
            return 0
    else:
            return len(kdPROT.query_ball_point([row['X'],row['Y']],int(SEARCH_RADIUS)))

minX, maxX = int(0), int(1940)
minY, maxY = int(0), int(1460)

dir = os.listdir(PATH)

pbar = ProgressBar()

for file in pbar(dir):
    try:
        DIR_HOME = str(file)
        PROTEIN_DF = pd.DataFrame(pd.read_csv(PATH + "/" + DIR_HOME + '/TAX.txt' , sep = "\t", header = None, names = ['X','Y','Value']), columns = ['X','Y','Value'])
        PROTEIN_DF = PROTEIN_DF[PROTEIN_DF['Value'] > int(THRESHOLD)]
        CYT_DF = pd.DataFrame(pd.read_csv(PATH + "/" + DIR_HOME + '/CYT.txt' , sep = "\t", header = None, names = ['X','Y','Value']), columns = ['X','Y','Value'])
        CYT_DF = CYT_DF[CYT_DF['Value'] > int(THRESHOLD_CYT)]

        img_CYT = Image.new(mode='RGB',size=(maxX, maxY))
        pixels = img_CYT.load()
        CYT_DF.apply(setColour_SENS_CYT, axis=1)
        img_CYT_1 = img_CYT.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        img_CYT_1.save(PATH + "/" + DIR_HOME + "/HEATMAP_CYT_" + str(THRESHOLD) + ".png")

        dfCombined = PROTEIN_DF.merge(CYT_DF, how = 'outer', on = ['X', 'Y'], suffixes= ('PROT', 'CYT'))
        dfCombined['ValuePROT'] = dfCombined.ValuePROT.fillna(0)
        dfCombined['ValueCYT'] = dfCombined.ValueCYT.fillna(0)
        CYT_DF.drop('Value', axis='columns', inplace=True)
        dfPROT_for_tree = PROTEIN_DF[['X','Y']]

        kdCYT = spatial.KDTree(CYT_DF)
        kdPROT = spatial.KDTree(dfPROT_for_tree)

        dfCombined['Neighbours'] = dfCombined.apply(countNeighbours, axis=1)
        dfCombined['Self-neighbours'] = dfCombined.apply(countNeighbours_self, axis = 1)

        img_TAX = Image.new(mode='RGB',size=(maxX, maxY))
        pixels = img_TAX.load()
        PROTEIN_DF.apply(setColour_SENS, axis=1)
        img_TAX_1 = img_TAX.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        img_TAX_1.save(PATH + "/" + DIR_HOME + "/HEATMAP_PROT_" + str(THRESHOLD) + ".png")

        img_KNN = Image.new(mode='RGB',size=(maxX, maxY), color = (255,255,255))
        pixels = img_KNN.load()
        dfCombined.apply(setColour, axis=1)
        img_KNN_1 = img_KNN.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        img_KNN_1.save(PATH + "/" + DIR_HOME + "/KNN_HEATMAP_" + str(THRESHOLD) + "_" + str(SEARCH_RADIUS) + ".png")

        img_RATIO = Image.new(mode='RGB',size=(maxX, maxY), color = (255,255,255))
        pixels = img_RATIO.load()
        dfCombined.apply(setColour_RATIO, axis=1)
        img_RATIO_1 = img_RATIO.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        img_RATIO_1.save(PATH + "/" + DIR_HOME + "/KNN_RATIO_HEATMAP_" + str(THRESHOLD) + "_" + str(SEARCH_RADIUS) + ".png")

        dfCombined.to_csv(PATH + "/" + DIR_HOME + '/TOTALS_' + str(THRESHOLD) + '_' + str(SEARCH_RADIUS) + '.csv', index = False)

        LIST_of_LISTS['DIR_HOME'].append(file)
        LIST_of_LISTS['THRESHOLD'].append(THRESHOLD)
        LIST_of_LISTS['SEARCH_RADIUS'].append(SEARCH_RADIUS)
        LIST_of_LISTS['KNN'].append((dfCombined['Neighbours']).sum())
        LIST_of_LISTS['KNN_SELF'].append((dfCombined['Self-neighbours']).sum())
        LIST_of_LISTS['PIXEL_LOSS'].append(len(PROTEIN_DF))

    except:
        continue


df_final = pd.DataFrame(LIST_of_LISTS, columns = ["REPEAT","THRESHOLD","SEARCH_RADIUS","KNN","KNN_SELF","PIXEL_LOSS"])

df_final.to_csv(PATH + "/TOTAL/" + str(THRESHOLD) + "_" + str(SEARCH_RADIUS) + ".csv", index = False)
