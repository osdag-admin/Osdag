from OCC.Core.AIS import AIS_Shape
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods, TopoDS_Shape
from OCC.Core.Quantity import Quantity_NOC_BLACK


def color_the_edges(shp, display, color, width):
    shapeList = []
    Ex = TopExp_Explorer(shp, TopAbs_EDGE)
    ctx = display.Context
    while Ex.More():
        aEdge = topods.Edge(Ex.Current())
        # ais_shape = AIS_Shape(aEdge)
        # ctx.SetColor(ais_shape, color, True)
        # ctx.SetWidth(ais_shape, width, False)
        # ctx.Display(ais_shape, False)
        Ex.Next()


def set_default_edge_style(shp, display):
    color_the_edges(shp, display, Quantity_NOC_BLACK, 0.5)
    # return shps
    
    
def osdag_display_shape(display, shapes, material=None, texture=None, color=None, transparency=None, update=False):
    set_default_edge_style(shapes, display)
    display.DisplayShape(shapes, material, texture, color, transparency, update=update)
