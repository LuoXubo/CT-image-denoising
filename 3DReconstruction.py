"""
@Description :   
@Author      :   Xubo Luo 
@Time        :   2023/03/13 17:04:45
"""
import vtk
import SimpleITK as sitk

renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

reader = vtk.vtkDICOMImageReader()
reader.SetDataByteOrderToLittleEndian()
reader.SetDirectoryName('./weiying')
#reader.SetDataSpacing(3.2, 3.2, 1.5)
reader.SetDataSpacing(0.47851601243, 0.47851601243, 47851601243)
# (0028,0030)	Pixel Spacing	0.47851601243\0.47851601243

# volume rendering
extractor = vtk.vtkContourFilter()
extractor.SetInputConnection(reader.GetOutputPort())
extractor.SetValue(0, -250)

skinNormals = vtk.vtkPolyDataNormals()
skinNormals.SetInputConnection(extractor.GetOutputPort())
skinNormals.SetFeatureAngle(60.0)

skinMapper = vtk.vtkPolyDataMapper()
skinMapper.SetInputConnection(skinNormals.GetOutputPort())
skinMapper.ScalarVisibilityOff()

skin = vtk.vtkActor()
skin.SetMapper(skinMapper)

outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(reader.GetOutputPort())

mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())

outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(0, 0, 0)

camera = vtk.vtkCamera()

renderer.AddActor(outline)
renderer.AddActor(skin)
renderer.SetActiveCamera(camera)
renderer.ResetCamera()
camera.Dolly(1.5)

renderer.SetBackground(1, 1, 1)
renWin.SetSize(600, 500)

renderer.ResetCameraClippingRange()

'''
writer = vtk.vtkSTLWriter()
# writer.SetInputData(reader.GetOutput())
writer.SetInputConnection(extractor.GetOutputPort())
writer.SetFileName('D:/VTK/vtkpython/jiati.stl'.encode('GBK'))
writer.Write()
'''

renWin.Render()
iren.Initialize()
iren.Start()
