
from OCC.Display.SimpleGui import init_display
from OCC.BRepPrimAPI import *

display, start_display, add_menu, add_function_to_menu = init_display()
my_cyl = BRepPrimAPI_MakeCylinder(60., 600.).Shape()

display.DisplayShape(my_cyl, update=True)
start_display()