import pydicom
import numpy as np
import os
from skimage.transform import radon
from skimage.transform import iradon
from matplotlib import pyplot as plt


file_path = 'I7000001'
dcm = pydicom.read_file(file_path)

(srcImg_width, srcImg_height) = (dcm.Columns, dcm.Rows)
metalImg = np.zeros((srcImg_height,srcImg_width))
notMetalImg = np.zeros((srcImg_height,srcImg_width))

dcm.image = dcm.pixel_array
DcmImage = dcm.pixel_array

slices = [dcm]
img = slices[int(len(slices)/2)].image.copy()

thrshldVal = 220
for h in range(srcImg_height):
    for w in range(srcImg_width):
        if(img[h,w] < thrshldVal):
            metalImg[h,w] = 0
            notMetalImg[h,w] = img[h,w]
        else:
            metalImg[h,w] = 255
            notMetalImg[h,w] = 0

xmax = metalImg.max()
xmin = metalImg.min()

imageB = (metalImg - xmin)/(xmax-xmin)
xmax = notMetalImg.max()
xmin = notMetalImg.min()
radon_theta = range(180)
# 原始图像Radon变换
r_src = radon(img, radon_theta, circle=True)

# 金属Radon变换
r_metal = radon(metalImg, radon_theta)

# 非金属Radon变换
r_notMetal = radon(notMetalImg, radon_theta)

# 对金属图像的Radon变换结果进行插值校正
(radon_height, radon_width) = r_metal.shape

# Radon变换的结果横向坐标是距离，纵坐标是角度
# metalPQBeta矩阵，储存金属的Radon变换的边界
metalPQBeta = np.zeros((radon_height, radon_width))

# 获取金属的Radon变换边界
for h in range(radon_height):
    for w in range(1, radon_width-1):
        preIndex = w-1
        nextIndex = w+1
        currPix = r_metal[h,w]
        if currPix > 0:
            if ((r_metal[h,nextIndex] > 0 and r_metal[h,preIndex] == 0) or (r_metal[h,nextIndex] == 0 and r_metal[h,preIndex] > 0)):
            #if((r_metal[h][nextIndex]>0 and r_metal[h][preIndex]==0 )or(r_metal[h][nextIndex]==0 and r_metal[h][preIndex]>0)):
                metalPQBeta[h][w] = 100

# 开始插值，非金属的Radon变换线性插值替换金属的Radon变换
for h in range(radon_height):
    upIndex = 0
    for w in range(radon_width):
        if(metalPQBeta[h][w]==100 and upIndex==0):
            upIndex = w
        elif(metalPQBeta[h][w]==100 and upIndex!=0):
            g_pBeta = r_notMetal[h][upIndex]
            g_qBeta = r_notMetal[h][w]
            midPixValue = r_metal[h][round((upIndex + w) * 0.5)]
            if(midPixValue > 0):
                for k in range(upIndex, w-1):
                    left_val = g_pBeta*(w-k)/(w-upIndex)
                    right_val = g_qBeta*(k-upIndex)/(w-upIndex)
                    r_notMetal[h][k] = left_val + right_val
                upIndex = 0
            else:
                upIndex = w

# 对非金属的Radon变换的插值校正结果进行反变换
irdnImg = iradon(r_notMetal, radon_theta, interpolation='linear')

xmin = irdnImg.min()
xmax = irdnImg.max()
resImg = (irdnImg-xmin)/(xmax-xmin) #归一化

data16 = np.int16(resImg)
# plt.figure(figsize=(6,6))
# plt.imshow(resImg, 'gray')
# plt.show()
dcm.PixelData = data16.tobytes()
dcm.save_as('C:/Users/Administrator/Desktop/test.dcm')
