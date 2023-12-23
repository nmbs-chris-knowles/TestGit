import ezdxf as ez
import aspose.cad as cad
dwg = 'P:\\0622-0215\\DWG\\CMK TESTING.dwg'
dwf = 'P:\\0622-0215\\DWG\\CMK TESTING.dwf'
image = cad.Image.load(dwg)
options = cad.imageoptions.DxfOptions()
image.save(dwf,options)

file = ez.readfile(dwf)
modelspace = file.modelspace()
print(len(modelspace))
