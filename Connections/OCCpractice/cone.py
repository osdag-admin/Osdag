
from OCC.Display.SimpleGui import init_display
from OCC.BRepPrimAPI import *

display, start_display, add_menu, add_function_to_menu = init_display()
my_cone = BRepPrimAPI_MakeCone(60., 1., 100).Shape()

display.DisplayShape(my_cone, update=True)
start_display()