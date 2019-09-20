
from OCC.Display.SimpleGui import init_display
from OCC.BRepPrimAPI import *

display, start_display, add_menu, add_function_to_menu = init_display()
my_sph = BRepPrimAPI_MakeSphere(60.).Shape()

display.DisplayShape(my_sph, update=True)
start_display()