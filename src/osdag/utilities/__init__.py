from OCC.Core.AIS import AIS_Shape
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods, TopoDS_Shape
from OCC.Core.Quantity import Quantity_NOC_BLACK

import os
import os.path
import time
import sys
import math
import itertools

import OCC
from OCC.Core.Aspect import Aspect_GFM_VER
from OCC.Core.AIS import AIS_Shape, AIS_Shaded, AIS_TexturedShape, AIS_WireFrame
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.gp import gp_Dir, gp_Pnt, gp_Pnt2d, gp_Vec
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeVertex,
                                     BRepBuilderAPI_MakeEdge,
                                     BRepBuilderAPI_MakeEdge2d,
                                     BRepBuilderAPI_MakeFace)
from OCC.Core.TopAbs import (TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX,
                             TopAbs_SHELL, TopAbs_SOLID)
from OCC.Core.Geom import Geom_Curve, Geom_Surface
from OCC.Core.Geom2d import Geom2d_Curve
from OCC.Core.Visualization import Display3d
from OCC.Core.V3d import (V3d_ZBUFFER, V3d_Zpos, V3d_Zneg, V3d_Xpos,
                          V3d_Xneg, V3d_Ypos, V3d_Yneg, V3d_XposYnegZpos,)
from OCC.Core.TCollection import TCollection_ExtendedString, TCollection_AsciiString
from OCC.Core.Quantity import (Quantity_Color, Quantity_TOC_RGB, Quantity_NOC_WHITE,
                               Quantity_NOC_BLACK, Quantity_NOC_BLUE1,
                               Quantity_NOC_CYAN1, Quantity_NOC_RED,
                               Quantity_NOC_GREEN, Quantity_NOC_ORANGE, Quantity_NOC_YELLOW)
from OCC.Core.Prs3d import Prs3d_Arrow, Prs3d_Presentation, Prs3d_Text, Prs3d_TextAspect
from OCC.Core.Graphic3d import (Graphic3d_NOM_NEON_GNC, Graphic3d_NOT_ENV_CLOUDS,
                                Graphic3d_Camera, Graphic3d_RM_RAYTRACING,
                                Graphic3d_RM_RASTERIZATION,
                                Graphic3d_StereoMode_QuadBuffer,
                                Graphic3d_RenderingParams)
from OCC.Core.Aspect import Aspect_TOTP_RIGHT_LOWER, Aspect_FM_STRETCH, Aspect_FM_NONE
import traceback

def color_the_edges(shp, display, color, width):
    """
    Colors the edges of a given shape.

    :param shp: The shape to color (TopoDS_Shape).
    :param display: The display context for rendering the shape.
    :param color: The color to apply to the edges (Quantity_Color or predefined constant like Quantity_NOC_BLACK).
    :param width: The width of the edges.
    """
    if not isinstance(shp, TopoDS_Shape):
        raise TypeError("The 'shp' parameter must be a valid TopoDS_Shape.")

    shapeList = []
    try:
        # Initialize the edge explorer for the given shape
        Ex = TopExp_Explorer(shp, TopAbs_EDGE)

        # Get the display context
        ctx = display.Context

        # If the color is a predefined constant (like Quantity_NOC_BLACK), convert to Quantity_Color
        if isinstance(color, int):  # Quantity_NOC_BLACK is an int, so check if color is an int
            color = Quantity_Color(color)

        # If the color is already a Quantity_Color, do nothing
        elif isinstance(color, Quantity_Color):
            pass  
        elif isinstance(color, tuple):
            # If color is a tuple (r, g, b), convert to Quantity_Color
            color = Quantity_Color(color[0], color[1], color[2], Quantity_TOC_RGB)
        else:
            raise TypeError(f"Unsupported color type: {type(color)}")

        # Iterate over the edges in the shape
        while Ex.More():
            # Extract the current edge
            aEdge = topods.Edge(Ex.Current())

            # Create an AIS_Shape for the edge
            ais_shape = AIS_Shape(aEdge)

            # Set the color and width for the edge
            ctx.SetColor(ais_shape, color, True)
            ctx.SetWidth(ais_shape, width, False)

            # Display the edge
            ctx.Display(ais_shape, False)

            # Store the edge for tracking
            shapeList.append(aEdge)

            # Move to the next edge
            Ex.Next()

    except Exception as e:
        # Print the error and traceback for more detail
        print(f"An error occurred: {e}")
        traceback.print_exc()  # This will print the full traceback

        raise RuntimeError(f"Error while coloring edges: {e}")
        
    return shapeList


def set_default_edge_style(shp, display):
    color_the_edges(shp, display, Quantity_NOC_BLACK, 0.5)
    # return shps


def osdag_display_shape(display, shapes, material=None, texture=None, color=None, transparency=None, update=False):
    set_default_edge_style(shapes, display)
    display.DisplayShape(shapes, material, texture, color, transparency, update=update)

def rgb_color(r, g, b):
    return Quantity_Color(r, g, b, Quantity_NOC_BLACK)

def to_string(_string):
    return TCollection_ExtendedString(_string)


def DisplayMsg(display, point, text_to_write, height=None, message_color=None, update=False):
    """
    :point: a gp_Pnt or gp_Pnt2d instance
    :text_to_write: a string
    :message_color: triple with the range 0-1
    """
    aPresentation = Prs3d_Presentation(display._struc_mgr)
    text_aspect = Prs3d_TextAspect()

    if message_color is not None:
        text_aspect.SetColor(rgb_color("RED"))
    # if height is not None:
    text_aspect.Aspect()
    # if isinstance(point, None):
    point = gp_Pnt(point.X(), point.Y(), point.Z())
    Prs3d_Text.Draw(aPresentation,
                    text_aspect,
                    to_string(text_to_write),
                    point)
    aPresentation.Display()
    # @TODO: it would be more coherent if a AIS_InteractiveObject
    # is be returned
    if update:
        display.Repaint()
    return aPresentation

# def osdag_display_msg(display, shapes, material=None, texture=None, color=None, transparency=None, update=False):
#     set_default_edge_style(shapes, display)
#     display.DisplayShape(shapes, material, texture, color, transparency, update=update)
