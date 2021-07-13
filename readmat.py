import os
import scipy.io as scio
import pydicom
import numpy as np

matpath = 'C:/Users/Administrator/Desktop/radonmethod/'
dcmpath = 'C:/Users/Administrator/Desktop/weiying/'
savepath = 'C:/Users/Administrator/Desktop/radon/'

dcmnames = os.listdir(dcmpath)
matnames = os.listdir(matpath)

cnt = 0
for (matname, dcmname) in zip(matnames, dcmnames):
    print('Processing : ', cnt)
    cnt += 1
    dcm = pydicom.read_file(dcmpath + str(dcmname))
    mat = scio.loadmat(matpath + str(matname))
    data = mat['data']

    # data[data>=3000] = 1024
    pixel = data[0:512, 0:512] + 500

    if dcm[0x0028, 0x0100].value == 16:
        pixel = pixel.astype(np.uint16)

    else:
        pixel = pixel.astype(np.uint8)

    # dcm.image = pixel

    img = np.int16(pixel)
    img = img.tobytes()
    dcm.PixelData = img
    dcm.save_as(savepath + str(dcmname) + '.dcm')

