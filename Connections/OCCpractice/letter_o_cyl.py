
from OCC.Display.SimpleGui import init_display
from OCC.BRepPrimAPI import *
from OCC.BRepAlgoAPI import *

display, start_display, add_menu, add_function_to_menu = init_display()
my_cyl = BRepPrimAPI_MakeCylinder(60., 2.).Shape()
my_cut = BRepPrimAPI_MakeCylinder(30., 2.).Shape()

O = BRepAlgoAPI_Cut(my_cyl, my_cut).Shape()

display.DisplayShape(O, update=True)
start_display()