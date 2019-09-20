
from OCC.Display.SimpleGui import init_display
from OCC.BRepPrimAPI import *
# from OCC.BRepFilletAPI import

display, start_display, add_menu, add_function_to_menu = init_display()
my_box = BRepPrimAPI_MakeTorus(60., 30.).Shape()
# my_cyl = BRepPrimAPI_MakeCylinder(70.,100.).Shape()

display.DisplayShape(my_box, update=True)
# display.DisplayShape(my_cyl, update=True)
start_display()