
from OCC.Display.SimpleGui import init_display
from OCC.Display.OCCViewer import Viewer3d
from OCC.BRepPrimAPI import *
from OCC.BRepAlgoAPI import *

display, start_display, add_menu, add_function_to_menu = init_display()
my_cyl = BRepPrimAPI_MakeCylinder(50., .5).Shape()
my_cut = BRepPrimAPI_MakeCylinder(30., .5).Shape()
my_sphere = BRepPrimAPI_MakeSphere(25.).Shape()
# my_sphere.set_bg_gradient_color(45.,20.,21.,25.,54.,10.)

O = BRepAlgoAPI_Cut(my_cyl, my_cut).Shape()

my_sphere = BRepAlgoAPI_Fuse(O, my_sphere).Shape()

display.DisplayShape(my_sphere, update=True)
start_display()