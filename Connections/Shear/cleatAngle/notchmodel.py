'''
Created on 15-Mar-2016

@author: deepa
'''
from OCC.Display.SimpleGui import init_display
from notch import Notch
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
from ModelUtils import *

display, start_display, add_menu, add_function_to_menu = init_display()
notchObject = Notch(B=140, t=8.9, R1=14, height=50, length=55.55)
notch3dModel = notchObject.create_model()
display.set_bg_gradient_color(51, 51, 102, 150, 150, 170)

sbeamOrigin = notchObject.sec_origin + notchObject.length / 2 * notchObject.uDir + notchObject.B / 2 * notchObject.wDir
gpNotchOrigin = get_gp_pt(sbeamOrigin)
my_sphere1 = BRepPrimAPI_MakeSphere(gpNotchOrigin, 5).Shape()
display.DisplayShape(notch3dModel, material=Graphic3d_NOT_2D_ALUMINUM, update=True)
# display.DisplayShape(my_sphere1,color ='blue', update = True)
display.View_Iso()
display.FitAll()
start_display()
