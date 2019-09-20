
from OCC.Display.SimpleGui import init_display
from OCC.BRepPrimAPI import *

display, start_display, add_menu, add_function_to_menu = init_display()
my_box = BRepPrimAPI_MakeBox(60., 30., 3.).Shape()

display.DisplayShape(my_box, update=True)
start_display()