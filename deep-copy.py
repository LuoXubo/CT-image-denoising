"""
@Description :   
@Author      :   Xubo Luo 
@Time        :   2023/03/13 17:04:45
"""
import os

import numpy as np
import pydicom
from matplotlib import pyplot as plt

ppath = './processedData/'
wpath = './weiying/'

savepath = './copypixel/'

pnames = os.listdir(ppath)
wnames = os.listdir(wpath)

cnt = 0
for wname in wnames:
    print('Processing dicom: ', cnt)

    pdcm = pydicom.read_file(ppath + str(cnt) + '.dcm')
    wdcm = pydicom.read_file(wpath + str(wname))

    img = pdcm.pixel_array
    (rows, cols) = wdcm.pixel_array.shape

    pixeldata = np.zeros((rows,cols))
    for i in range(rows):
        for j in range(cols):
            pixeldata[i][j] = img[i][j] + 950
    wdcm.image = pixeldata
    img = np.int16(pixeldata)
    img = img.tobytes()
    wdcm.PixelData = img
    wdcm.save_as(savepath + wname + '.dcm')
    cnt += 1