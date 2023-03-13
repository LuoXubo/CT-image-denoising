"""
@Description :   
@Author      :   Xubo Luo 
@Time        :   2023/03/13 17:04:45
"""
import SimpleITK as sitk

dcmpath = './weiying'
savepath = './Desktop/'

reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(dcmpath)
reader.SetFileNames(dicom_names)
image2 = reader.Execute()
image_array = sitk.GetArrayFromImage(image2)  # z, y, x
origin = image2.GetOrigin()  # x, y, z
spacing = image2.GetSpacing()  # x, y, z
image3 = sitk.GetImageFromArray(image_array)  ##其他三维数据修改原本的数据，
sitk.WriteImage(image3, savepath + 'weiying.nii')  # 这里可以直接换成image2 这样就保存了原来的数据成了nii格式了。




