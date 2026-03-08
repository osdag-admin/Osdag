from ISection import ISection
from notch import Notch
from plate import Plate
from filletweld import FilletWeld
import sys
import math
import numpy
import time

# OCC Imports
# from OCC.Display.backend import load_backend
# load_backend("pyside6")
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf, gp_Ax1, gp_Dir, gp_Ax3
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import Graphic3d_NOM_ALUMINIUM
from OCC.Display.SimpleGui import init_display
from OCC.Core.StlAPI import StlAPI_Writer

def translation_movement(x,y,z, model):
    """
    This function is used to translate the model by a given vector
    Args:
        x: float
        y: float
        z: float
        model: TopoDS_Shape
    Returns:
        model: TopoDS_Shape
    """
    trsf = gp_Trsf()
    translation_vector = gp_Vec(x, y, z)
    trsf.SetTranslation(translation_vector)
    model = BRepBuilderAPI_Transform(model, trsf).Shape()
    return model

def translation_rotation(angle, axis, model):
    """
    This function is used to rotate the model by a given angle around a given axis
    Args:
        angle: float
        axis: numpy array
        model: TopoDS_Shape
    Returns:
        model: TopoDS_Shape
    """
    trsf = gp_Trsf()
    ax1 = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(float(axis[0]), float(axis[1]), float(axis[2])))
    trsf.SetRotation(ax1, math.radians(angle))
    model = BRepBuilderAPI_Transform(model, trsf).Shape()
    return model

def plate_model(origin, l, b, h):
    """
    This function is used to create a plate model
    Args:
        origin: numpy array
        l: float
        b: float
        h: float
    Returns:
        plate_shape: TopoDS_Shape
    """
    plate_origin = origin
    plate_uDir = numpy.array([0.,0.,1.])
    plate_wDir = numpy.array([0.,1.,0.])
    plate = Plate(l, b, h)
    _place = plate.place(plate_origin, plate_uDir, plate_wDir)
    plate_point = plate.compute_params()
    plate_shape = plate.create_model()
    return plate_shape

def filletWeld_model(b, h, l):
    """
    This function is used to create a fillet weld model
    Args:
        b: float
        h: float
        l: float
    Returns:
        prism: TopoDS_Shape
    """
    origin = numpy.array([0., 0., 0.])
    uDir = numpy.array([0., 0., 1.])
    shaftDir = numpy.array([0., 1., 0.])
    FWeld = FilletWeld(b, h, l)
    _place = FWeld.place(origin, uDir, shaftDir)
    point = FWeld.compute_params()
    prism = FWeld.create_model(0)
    return prism

#initialisation of the display method to display the 3D model
display, start_display, add_menu, add_function_to_menu = init_display()
display.set_bg_gradient_color([51, 51, 102], [150, 150, 170]) 

#input parameters
l=50
b=40
h=0.5

#calculation of the horizontal distance between the two plates
horizontal_distance = l/3

weld_height = h
weld_breadth = h

print("-----------------------------------------------------------------------")
print("generating the model")
print("-----------------------------------------------------------------------")

#creation of the plates
top_plate = plate_model(numpy.array([0, 0, 0]) , l, b, h)
bottom_plate = plate_model(numpy.array([-horizontal_distance, 0, -h]) , l, b, h)

#fusion of the plates
lap_plate_model = BRepAlgoAPI_Fuse(bottom_plate, top_plate).Shape()

#creation of the fillet weld model
fillet_weld_model1 = filletWeld_model(weld_height, weld_height, b)
fillet_weld_model1 = translation_rotation(90, numpy.array([0, 1, 0]), fillet_weld_model1)
fillet_weld_model1 = translation_movement((l/2)-horizontal_distance, 0, -weld_height/2, fillet_weld_model1)

#creation of the second fillet weld model
fillet_weld_model2 = filletWeld_model(weld_height, weld_height, b)
fillet_weld_model2 = translation_rotation(-90, numpy.array([0, 1, 0]), fillet_weld_model2)
fillet_weld_model2 = translation_movement(-l/2, 0, -h/2, fillet_weld_model2)

#fusion of the fillet weld models
weld_model = BRepAlgoAPI_Fuse(fillet_weld_model1, fillet_weld_model2).Shape()

#displaying the model
display.DisplayShape(lap_plate_model,material=Graphic3d_NOM_ALUMINIUM, update=True)
display.DisplayShape(weld_model,color="red", update=True)

start_display()