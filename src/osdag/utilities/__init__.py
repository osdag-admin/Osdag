from OCC.Core.AIS import AIS_Shape
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods, TopoDS_Shape
from OCC.Core.AIS import AIS_Point
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Prs3d import Prs3d_PointAspect
from OCC.Core.Aspect import Aspect_TOM_BALL
from OCC.Core.Geom import Geom_Point
from OCC.Core.TopoDS import TopoDS_Vertex
from OCC.Core.BRep import BRep_Tool
from OCC.Core.gp import gp_Pnt
from OCC.Core.AIS import AIS_Point
from OCC.Core.Geom import Geom_CartesianPoint
from OCC.Core.gp import gp_Pnt, gp_Pnt2d
from OCC.Core.Geom import Geom_CartesianPoint
from OCC.Core.AIS import AIS_TextLabel, AIS_Point
from OCC.Core.Quantity import Quantity_TOC_RGB, Quantity_Color


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
                                Graphic3d_RenderingParams,
                                Graphic3d_AspectLine3d)
from OCC.Core.Aspect import Aspect_TOTP_RIGHT_LOWER, Aspect_FM_STRETCH, Aspect_FM_NONE
import traceback
from OCC.Core.AIS import AIS_TextLabel


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
    # shapeList = []
    try:
        # Initialize the edge explorer for the given shape
        Ex = TopExp_Explorer(shp, TopAbs_EDGE)
        # Get the display context
        ctx = display.Context
        # Iterate over the edges in the shape
        while Ex.More():
            # Extract the current edge
            aEdge = topods.Edge(Ex.Current())

            # Create an AIS_Shape for the edge
            ais_shape = AIS_Shape(aEdge)
            # Set the color
            ais_shape.SetColor(color)
            # Display the edge
            ctx.Display(ais_shape, False)

            # Store the edge for tracking
            # shapeList.append(aEdge)

            # Move to the next edge
            Ex.Next()

    except Exception as e:
        # Print the error and traceback for more detail
        print(f"An error occurred: {e}")
        traceback.print_exc()  # This will print the full traceback

        raise RuntimeError(f"Error while coloring edges: {e}")
        
    # return shapeList


def set_default_edge_style(shp, display):
    color_the_edges(shp, display, Quantity_Color(Quantity_NOC_BLACK), 0.5)
    # return shps


def osdag_display_shape(display, shapes, material=None, texture=None, color=None, transparency=None, update=False):
    set_default_edge_style(shapes, display)
    display.DisplayShape(shapes, material, texture, color, transparency, update=update)

def rgb_color(r, g, b):
    return Quantity_Color(r, g, b, Quantity_NOC_BLACK)

def to_string(_string):
    return TCollection_ExtendedString(_string)

def DisplayMsg(display, point, text_to_write, height=15, message_color=None, update=False):
    if isinstance(point, gp_Pnt):
        pnt = point
    elif isinstance(point, gp_Pnt2d):
        pnt = gp_Pnt(point.X(), point.Y(), 0.0)
    else:
        raise TypeError("point must be gp_Pnt or gp_Pnt2d")

    if hasattr(display, 'Context'):
        ais_context = display.Context
    else:
        raise AttributeError("Display does not have a valid AIS context.")

    # Use yellow color by default (or provided)
    if message_color is not None:
        if len(message_color) != 3:
            raise ValueError("message_color must be a tuple of 3 floats between 0 and 1")
        r, g, b = message_color
        if not (0 <= r <= 1 and 0 <= g <= 1 and 0 <= b <= 1):
            raise ValueError("message_color values must be in range 0–1")
        color = Quantity_Color(r, g, b, Quantity_TOC_RGB)
    else:
        color = Quantity_Color(1.0, 1.0, 0.0, Quantity_TOC_RGB)  # Yellow

    # Create a text label with "+" sign as the marker
    plus_label = AIS_TextLabel()
    plus_label.SetText("+")
    plus_label.SetPosition(pnt)
    plus_label.SetColor(color)
    plus_label.SetHeight(height)

    ais_context.Display(plus_label, True)

    # Register tooltip for hover
    if not hasattr(display, "_hover_tooltips"):
        display._hover_tooltips = []
    display._hover_tooltips.append((plus_label, text_to_write))

    if update:
        display.Repaint()

    return plus_label



# def DisplayMsg(display, point, text_to_write, height=None, message_color=None, update=False):
#     """
#     :point: a gp_Pnt or gp_Pnt2d instance
#     :text_to_write: a string
#     :message_color: triple with the range 0-1, e.g., (1.0, 0.0, 0.0) for red
#     :height: float, text height
#     :update: bool, whether to repaint the display
#     """
#     # Handle point
#     if isinstance(point, gp_Pnt):
#         pnt = point
#     elif isinstance(point, gp_Pnt2d):
#         pnt = gp_Pnt(point.X(), point.Y(), 0.0)
#     else:
#         raise TypeError("point must be gp_Pnt or gp_Pnt2d")

#     # Get the AIS_InteractiveContext from the display
#     # Try different ways to access the context
#     if hasattr(display, 'Context'):
#         ais_context = display.Context  # Access as attribute
#     elif hasattr(display, '_context'):
#         ais_context = display._context
#     elif hasattr(display, 'GetContext'):
#         ais_context = display.GetContext()  # Some implementations use methods
#     else:
#         # Fallback: try to create a text directly with the display object
#         return display.DisplayMessage(pnt, text_to_write, message_color or (0,0,0), height or 10)

#     # Set color
#     if message_color is not None:
#         if len(message_color) != 3:
#             raise ValueError("message_color must be a tuple of three floats between 0 and 1")
#         r, g, b = message_color
#         if not (0 <= r <= 1 and 0 <= g <= 1 and 0 <= b <= 1):
#             raise ValueError("message_color values must be between 0 and 1")
#         color = Quantity_Color(r, g, b, Quantity_TOC_RGB)
#     else:
#         # Default color: black
#         color = Quantity_Color(0.0, 0.0, 0.0, Quantity_TOC_RGB)

#     # Create AIS_Text label
#     text_label = AIS_TextLabel()
#     text_label.SetText(text_to_write)
#     text_label.SetPosition(pnt)
#     text_label.SetColor(color)
    
#     # Set height
#     if height is not None:
#         text_label.SetHeight(height)
#     else:
#         # Default height: 10
#         text_label.SetHeight(20)
    
#     # Display the text
#     ais_context.Display(text_label, True)
    
#     # Update display if needed
#     if update:
#         display.Repaint()

#     return text_label

# def osdag_display_msg(display, shapes, material=None, texture=None, color=None, transparency=None, update=False):
#     set_default_edge_style(shapes, display)
#     display.DisplayShape(shapes, material, texture, color, transparency, update=update)