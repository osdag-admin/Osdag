from OCC.Core.gp import gp_Vec, gp_Trsf, gp_Pnt, gp_Dir, gp_Ax1
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Display.SimpleGui import init_display
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_RED
import math
import numpy


def make_edge(*args):
    edge = BRepBuilderAPI_MakeEdge(*args)
    result = edge.Edge()
    return result

def make_wire(*args):
    if isinstance(args[0], list) or isinstance(args[0], tuple):
        wire = BRepBuilderAPI_MakeWire()
        for i in args[0]:
            wire.Add(i)
        wire.Build()
        return wire.Wire()
    wire = BRepBuilderAPI_MakeWire(*args)
    return wire.Wire()

def makeWireFromEdges(edges):
    wire = None
    for edge in edges:
        if wire:
            wire = make_wire(wire, edge)
        else:
            wire = make_wire(edge)
    return wire

def makeFaceFromWire(wire):
    return BRepBuilderAPI_MakeFace(wire).Face()

def getGpPt(point):
    return gp_Pnt(point[0], point[1], point[2])

def makeEdgesFromPoints(points):
    edges = []
    num = len(points)
    for i in range(num - 1):
        edge = make_edge(getGpPt(points[i]), getGpPt(points[i + 1]))
        edges.append(edge)
    # Close the loop
    cycleEdge = make_edge(getGpPt(points[num - 1]), getGpPt(points[0]))
    edges.append(cycleEdge)
    return edges

def makePrismFromFace(aFace, eDir):
    return BRepPrimAPI_MakePrism(aFace, gp_Vec(gp_Pnt(0., 0., 0.), gp_Pnt(eDir[0], eDir[1], eDir[2]))).Shape()

def create_corner_triangular_weld(corner_point, size, length, orientation='xy',flag='positive',end=False):
    """Create a triangular fillet weld at corner intersection"""
    x, y, z = corner_point
    
    if orientation == 'xy':  # Horizontal corner weld
        # Right triangle in XY plane
        p1 = gp_Pnt(x, y, z)              # Corner point
        p2 = gp_Pnt(x + size, y, z)       # Along X axis
        p3 = gp_Pnt(x, y + size, z)       # Along Y axis
        
        # Create triangular face
        edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
        edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
        edge3 = BRepBuilderAPI_MakeEdge(p3, p1).Edge()
        
        wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3).Wire()
        face = BRepBuilderAPI_MakeFace(wire).Face()
        
        # Extrude along Z axis
        vec = gp_Vec(0, 0, length)
        
    elif orientation == 'xz':  # Vertical corner weld in XZ plane
        if end==True:
            p1 = gp_Pnt(x, y, z)              # Corner point
            p2 = gp_Pnt(x, y-20, z)       # Along X axis
            p3 = gp_Pnt(x, y, z + size)       # Along Z axis
        if flag=='negative':
            p1 = gp_Pnt(x, y, z)              # Corner point
            p2 = gp_Pnt(x + 12, y, z)       # Along X axis
            p3 = gp_Pnt(x, y, z - size)       # Along Z axis
        else:    
        # Right triangle in XZ plane
            p1 = gp_Pnt(x, y, z)              # Corner point
            p2 = gp_Pnt(x + 12, y, z)       # Along X axis
            p3 = gp_Pnt(x, y, z + size)       # Along Z axis
        
        # Create triangular face
        edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
        edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
        edge3 = BRepBuilderAPI_MakeEdge(p3, p1).Edge()
        
        wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3).Wire()
        face = BRepBuilderAPI_MakeFace(wire).Face()
        
        # Extrude along Y axis
        vec = gp_Vec(0, length, 0)
        
    elif orientation == 'yz':  # Vertical corner weld in YZ plane
        # Right triangle in YZ plane
        if flag=="negative":
                
            p1 = gp_Pnt(x, y, z)              # Corner point
            p2 = gp_Pnt(x, y - 20, z)       # Along Y axis
            p3 = gp_Pnt(x, y, z - size)       # Along Z axis
        else:

            p1 = gp_Pnt(x, y, z)              # Corner point
            p2 = gp_Pnt(x, y - 20, z)       # Along Y axis
            p3 = gp_Pnt(x, y, z + size)       # Along Z axis
        
        # Create triangular face
        edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
        edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
        edge3 = BRepBuilderAPI_MakeEdge(p3, p1).Edge()
        
        wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3).Wire()
        face = BRepBuilderAPI_MakeFace(wire).Face()
        
        # Extrude along X axis
        vec = gp_Vec(length, 0, 0)
    
    prism = BRepPrimAPI_MakePrism(face, vec).Shape()
    return prism


def create_corner_triangular_weldo(corner_point, size, length, orientation='xy',flag="positive"):
    """Create a triangular fillet weld at corner intersection"""
    x, y, z = corner_point
    
    if orientation == 'xy':  # Horizontal corner weld
        # Right triangle in XY plane
        p1 = gp_Pnt(x, y, z)              # Corner point
        p2 = gp_Pnt(x + size, y, z)       # Along X axis
        p3 = gp_Pnt(x, y + size, z)       # Along Y axis
        
        # Create triangular face
        edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
        edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
        edge3 = BRepBuilderAPI_MakeEdge(p3, p1).Edge()
        
        wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3).Wire()
        face = BRepBuilderAPI_MakeFace(wire).Face()
        
        
        # Extrude along Z axis
        vec = gp_Vec(0, 0, length)
        
    elif orientation == 'xz':  # Vertical corner weld in XZ plane
        # if flag==False:
        #     p1 = gp_Pnt(x, y, z)              # Corner point
        #     p2 = gp_Pnt(x - size-10, y, z)       # Along X axis
        #     p3 = gp_Pnt(x, y, z + size)  
        # elif flag2==False:
        #     p1 = gp_Pnt(x, y, z)              # Corner point
        #     p2 = gp_Pnt(x - size, y, z)       # Along X axis
        #     p3 = gp_Pnt(x, y, z - size)  
        # else:
        # Right triangle in XZ plane
        if flag=="negative":
            p1 = gp_Pnt(x, y, z)              # Corner point
            p2 = gp_Pnt(x - 8, y, z)       # Along X axis    
            p3 = gp_Pnt(x, y, z - size)       # Along Z axis
        else:   
            p1 = gp_Pnt(x, y, z)              # Corner point
            p2 = gp_Pnt(x - 8, y, z)       # Along X axis    
            p3 = gp_Pnt(x, y, z + size)       # Along Z axis
        
        # Create triangular face
        edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
        edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
        edge3 = BRepBuilderAPI_MakeEdge(p3, p1).Edge()
        
        wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3).Wire()
        face = BRepBuilderAPI_MakeFace(wire).Face()
        
        # Extrude along Y axis
        vec = gp_Vec(0, length, 0)
        
    elif orientation == 'yz':  # Vertical corner weld in YZ plane
        # Right triangle in YZ plane
        if flag=="negative":
            p1 = gp_Pnt(x, y, z)              # Corner point
            p2 = gp_Pnt(x, y + 20, z)       # Along Y axis
            p3 = gp_Pnt(x, y, z - size)       # Along Z axis
        else:
            p1 = gp_Pnt(x, y, z)              # Corner point
            p2 = gp_Pnt(x, y + 20, z)       # Along Y axis
            p3 = gp_Pnt(x, y, z + size)       # Along Z axis
        
        # Create triangular face
        edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
        edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
        edge3 = BRepBuilderAPI_MakeEdge(p3, p1).Edge()
        
        wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3).Wire()
        face = BRepBuilderAPI_MakeFace(wire).Face()
        
        # Extrude along X axis
        vec = gp_Vec(length, 0, 0)
    
    prism = BRepPrimAPI_MakePrism(face, vec).Shape()
    return prism

def create_edge_weld(start_point, end_point, weld_size, thickness_direction='z',weld_size_x=0,theta=0,flag="positive"):
    """Create fillet weld along an edge"""
    x1, y1, z1 = start_point
    x2, y2, z2 = end_point
    
    if thickness_direction == 'z':
        if weld_size_x!=0:
                if flag=="negative":
                    p1 = gp_Pnt(x1, y1, z1)
                    p2 = gp_Pnt(x1 + weld_size_x*math.cos(theta), y1-weld_size_x*math.sin(theta), z1)
                    p3 = gp_Pnt(x1, y1, z1 - weld_size)
                else:
                    p1 = gp_Pnt(x1, y1, z1)
                    p2 = gp_Pnt(x1 + weld_size_x*math.cos(theta), y1+weld_size_x*math.sin(theta), z1)
                    p3 = gp_Pnt(x1, y1, z1 + weld_size)
        # Create triangular cross-section weld along Z direction
        # Base points for triangle
        else:
            if flag=="negative":
                p1 = gp_Pnt(x1, y1, z1)
                p2 = gp_Pnt(x1 + weld_size, y1, z1)
                p3 = gp_Pnt(x1, y1, z1 - weld_size)
            else:
                p1 = gp_Pnt(x1, y1, z1)
                p2 = gp_Pnt(x1 + weld_size, y1, z1)
                p3 = gp_Pnt(x1, y1, z1 + weld_size)
        
        # Create triangular face
        edge1 = BRepBuilderAPI_MakeEdge(p2, p1).Edge()
        edge2 = BRepBuilderAPI_MakeEdge(p3, p2).Edge()
        edge3 = BRepBuilderAPI_MakeEdge(p3, p1).Edge()
        
        wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3).Wire()
        face = BRepBuilderAPI_MakeFace(wire).Face()
        
        # Extrude along the edge direction
        edge_length = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
        direction = gp_Vec(x2-x1, y2-y1, z2-z1)
        direction.Normalize()
        direction.Scale(edge_length)
        
    elif thickness_direction == 'y':
        # Create triangular cross-section weld along Y direction
        p1 = gp_Pnt(x1, y1, z1)
        p2 = gp_Pnt(x1 + weld_size, y1, z1)
        p3 = gp_Pnt(x1, y1 + weld_size, z1)
        
        edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
        edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
        edge3 = BRepBuilderAPI_MakeEdge(p3, p1).Edge()
        
        wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3).Wire()
        face = BRepBuilderAPI_MakeFace(wire).Face()
        
        edge_length = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
        direction = gp_Vec(x2-x1, y2-y1, z2-z1)
        direction.Normalize()
        direction.Scale(edge_length)
    
    prism = BRepPrimAPI_MakePrism(face, direction).Shape()
    return prism


def create_edge_weldo(start_point, end_point, weld_size, thickness_direction='z',weld_size_x=0,theta=0,flag="positive"):
    """Create fillet weld along an edge"""
    x1, y1, z1 = start_point
    x2, y2, z2 = end_point
    
    if thickness_direction == 'z':
        if weld_size_x!=0:
                if flag=="negative":
                    p1 = gp_Pnt(x1, y1, z1)
                    p2 = gp_Pnt(x1 - weld_size_x*math.cos(theta), y1+weld_size_x*math.sin(theta), z1)
                    p3 = gp_Pnt(x1, y1, z1 - weld_size)
                else:
                    p1 = gp_Pnt(x1, y1, z1)
                    p2 = gp_Pnt(x1 - weld_size_x*math.cos(theta), y1-weld_size_x*math.sin(theta), z1)
                    p3 = gp_Pnt(x1, y1, z1 + weld_size)
        # Create triangular cross-section weld along Z direction
        # Base points for triangle
        else:
            if flag=="negative":
                p1 = gp_Pnt(x1, y1, z1)
                p2 = gp_Pnt(x1 - weld_size, y1, z1)
                p3 = gp_Pnt(x1, y1, z1 - weld_size)
            else:
                p1 = gp_Pnt(x1, y1, z1)
                p2 = gp_Pnt(x1 - weld_size, y1, z1)
                p3 = gp_Pnt(x1, y1, z1 + weld_size)
        
        # Create triangular face
        edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
        edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
        edge3 = BRepBuilderAPI_MakeEdge(p3, p1).Edge()
        
        wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3).Wire()
        face = BRepBuilderAPI_MakeFace(wire).Face()
        
        # Extrude along the edge direction
        edge_length = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
        direction = gp_Vec(x2-x1, y2-y1, z2-z1)
        direction.Normalize()
        direction.Scale(edge_length)
        
    elif thickness_direction == 'y':
        # Create triangular cross-section weld along Y direction
        p1 = gp_Pnt(x1, y1, z1)
        p2 = gp_Pnt(x1 + weld_size, y1, z1)
        p3 = gp_Pnt(x1, y1 +weld_size, z1)
        
        edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
        edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
        edge3 = BRepBuilderAPI_MakeEdge(p3, p1).Edge()
        
        wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3).Wire()
        face = BRepBuilderAPI_MakeFace(wire).Face()
        
        edge_length = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
        direction = gp_Vec(x2-x1, y2-y1, z2-z1)
        direction.Normalize()
        direction.Scale(edge_length)
    
    prism = BRepPrimAPI_MakePrism(face, direction).Shape()
    return prism




def create_i_section(length, width, depth, flange_thickness, web_thickness):
    web_height = depth - 2 * flange_thickness

    bottom_flange = BRepPrimAPI_MakeBox(length, width, flange_thickness).Shape()
    top_flange = BRepPrimAPI_MakeBox(length, width, flange_thickness).Shape()
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(0, 0, depth - flange_thickness))
    top_flange_transform = BRepBuilderAPI_Transform(top_flange, trsf, True).Shape()

    web = BRepPrimAPI_MakeBox(length, web_thickness, web_height).Shape()
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(0, (width - web_thickness) / 2, flange_thickness))
    web_transform = BRepBuilderAPI_Transform(web, trsf, True).Shape()

    i_section_solid = BRepAlgoAPI_Fuse(bottom_flange, top_flange_transform).Shape()
    i_section_solid = BRepAlgoAPI_Fuse(i_section_solid, web_transform).Shape()

    return i_section_solid

def create_end_batten(length, width, depth, column_distance):
    batten = BRepPrimAPI_MakeBox(length, column_distance + width, depth).Shape()
    return batten

def create_straight_lace(width, thickness, length):
    # Create a horizontal lace plate
    lace = BRepPrimAPI_MakeBox(length, width, thickness).Shape()
    return lace

def create_parallelogram_face(p1, p2, p3, thickness):
    # Calculate the fourth point (Top-right)
    vec1 = gp_Vec(p1, p2)  # Base vector
    p4 = gp_Pnt(p3.XYZ() + vec1.XYZ())  # Top-right = Top-left + base vector

    # Create edges
    edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(p2, p4).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(p4, p3).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(p3, p1).Edge()

    # Make wire
    wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()

    # Make face
    face = BRepBuilderAPI_MakeFace(wire).Face()
    
    # Extrude the face into a solid
    vec = gp_Vec(0, 0, thickness)
    prism = BRepPrimAPI_MakePrism(face, vec).Shape()
    
    return prism

if __name__ == "__main__":
    column_length = 6100.0  # Total column length
    i_section_width = 100.0  # Width of I-section
    i_section_height = 200.0  # Height of I-section
    flange_thickness = 10.0
    web_thickness = 5.0
    column_distance = 450.0  # Distance between I-sections (center to center)
    
    # End batten parameters
    batten_depth = 300.0
    batten_thickness = 10.0
    
    # Lace parameters
    lace_width = 100.0
    lace_thickness = 8.0
    start_laces = batten_depth + column_distance
    step_size = column_distance + lace_width
    end_lace = column_length - column_distance - lace_width - batten_depth
    num_laces = int((end_lace - start_laces) / step_size) + 1
    num_laces=int((column_length-batten_depth)/column_distance)
    print(num_laces)
    triangular_weld_shapes = []
    # Create the two I-sections
    i_section1 = create_i_section(column_length, i_section_width, i_section_height, flange_thickness, web_thickness)
    #top left end batten
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(0, column_distance, 0))
    i_section2 = BRepBuilderAPI_Transform(i_section1, trsf, True).Shape()
    p1 = gp_Pnt(batten_depth,0+20, i_section_height)
    p2 = gp_Pnt(batten_depth,column_distance-100+2*lace_width-20, i_section_height)
    p3 = gp_Pnt(20, +20,i_section_height)
    diagonal_platet = create_parallelogram_face(p1, p2, p3, batten_thickness)
    batten_corner1=(20,20,i_section_height)
    tri_weld1b = create_corner_triangular_weld(batten_corner1,batten_thickness, batten_depth-20, 'yz',)

    batten_corner2=(20,column_distance-100+2*lace_width-20,i_section_height)
    tri_weld2b = create_corner_triangular_weldo(batten_corner2,batten_thickness, batten_depth-20, 'yz')

    corner1o = (20, 
                      20, 
                      i_section_height)
    tri_weld1o = create_corner_triangular_weldo(corner1o, batten_thickness, lace_width-20, 'xz')

    corner2o = (20, 
                      column_distance-100+lace_width, 
                      i_section_height)
    tri_weld2o = create_corner_triangular_weldo(corner2o,batten_thickness, lace_width-20, 'xz')
    triangular_weld_shapes.append([tri_weld1b,tri_weld2b,tri_weld1o,tri_weld2o])


    # Position the right bottom batten
    trsf_bottom_right = gp_Trsf()
    trsf_bottom_right.SetTranslation(gp_Vec(column_length - batten_thickness, 0, 0))

# bottom left end batten
    p1 = gp_Pnt(batten_depth,0+20, -lace_thickness)
    p2 = gp_Pnt(batten_depth,column_distance-100+2*lace_width-20, -lace_thickness)
    p3 = gp_Pnt(20, +20,-lace_thickness)
    diagonal_platetb = create_parallelogram_face(p1, p2, p3, batten_thickness)

    batten_corner1=(20,20,0)
    tri_weld1b = create_corner_triangular_weld(batten_corner1,batten_thickness, batten_depth-20, 'yz',"negative")

    batten_corner2=(20,column_distance-100+2*lace_width-20,0)
    tri_weld2b = create_corner_triangular_weldo(batten_corner2,batten_thickness, batten_depth-20, 'yz',"negative")

    corner1o = (20, 
                      20, 
                      0)
    tri_weld1o = create_corner_triangular_weldo(corner1o, batten_thickness, lace_width-20, 'xz',"negative")

    corner2o = (20, 
                      column_distance-100+lace_width, 
                      0)
    tri_weld2o = create_corner_triangular_weldo(corner2o,batten_thickness, lace_width-20, 'xz',"negative")
    triangular_weld_shapes.append([tri_weld1b,tri_weld2b,tri_weld1o,tri_weld2o])
     # top right end batten
    p1 = gp_Pnt(column_length-20,20, i_section_height)
    p2 = gp_Pnt(column_length-20,column_distance-100+2*lace_width-20, i_section_height)
    p3 = gp_Pnt(column_length-20-batten_depth, 20,i_section_height)
    diagonal_plate = create_parallelogram_face(p1, p2, p3, batten_thickness)
    corner1 = (batten_depth+num_laces*column_distance, 
                      0, 
                      i_section_height)
    tri_weld1 = create_corner_triangular_weld(corner1, 2*lace_thickness, lace_width, 'xz')
    corner1o = (column_length-20-batten_depth, 
                      20, 
                      i_section_height)
    tri_weld1o = create_corner_triangular_weldo(corner1o, batten_thickness, lace_width-20, 'xz')
    corner2=(batten_depth+num_laces*column_distance, 
                      column_distance-100+lace_width, 
                      i_section_height)
    tri_weld2 = create_corner_triangular_weld(corner2, lace_thickness, lace_width, 'xz')
    corner2o = (column_length-20-batten_depth, 
                      column_distance-100+lace_width, 
                      i_section_height)
    tri_weld2o = create_corner_triangular_weldo(corner2o,batten_thickness, lace_width-20, 'xz')
    triangular_weld_shapes.extend([ tri_weld1,tri_weld1o,tri_weld2,tri_weld2o])

    batten_corner1=(column_length-20-batten_depth,20,i_section_height)
    tri_weld1b = create_corner_triangular_weld(batten_corner1,batten_thickness, batten_depth, 'yz')
    corner1b = (column_length-20, 
                      20, 
                      i_section_height)
    tri_weld1 = create_corner_triangular_weld(corner1b, batten_thickness, lace_width-20, 'xz')
    triangular_weld_shapes.extend([ tri_weld1b,tri_weld1])

    batten_corner2=(column_length-20-batten_depth,column_distance-100+2*lace_width-20,i_section_height)
    tri_weld2b = create_corner_triangular_weldo(batten_corner2,batten_thickness, batten_depth, 'yz')
    corner1b = (column_length-20, 
                      column_distance-100+lace_width, 
                      i_section_height)
    tri_weld2bo = create_corner_triangular_weld(corner1b, batten_thickness, lace_width-20, 'xz')
    triangular_weld_shapes.extend([ tri_weld1b,tri_weld1,tri_weld2b, tri_weld2bo])
    
    

    # Position the left top batten
    # trsf_top_left = gp_Trsf()
    # trsf_top_left.SetTranslation(gp_Vec(0, 0, i_section_height))
    # top_batten_left = BRepBuilderAPI_Transform(temp_top_left, trsf_top_left, True).Shape()

    # Position the right top batten - need both horizontal and vertical translation
    trsf_top_right = gp_Trsf()
    trsf_top_right.SetTranslation(gp_Vec(column_length - batten_thickness, 0, i_section_height))
        # top_batten_right = BRepBuilderAPI_Transform(temp_top_right, trsf_top_right, True).Shape()
        
        # bottom right end batten
    p1 = gp_Pnt(column_length-20,column_distance-100+2*lace_width-20, -lace_thickness)
    p2 = gp_Pnt(column_length-20,20, -lace_thickness)
    p3 = gp_Pnt(column_length-20-batten_depth,column_distance-100+2*lace_width-20 ,-lace_thickness)
    diagonal_plateo = create_parallelogram_face(p1, p2, p3, batten_thickness)

    corner2o=(column_length-20-batten_depth,20,0)
    tri_weld2o=create_corner_triangular_weldo(corner2o, batten_thickness, lace_width-20, 'xz',"negative")

    corner1o=(column_length-20-batten_depth, 
                lace_width+column_distance-100, 
                0)
    tri_weld1o = create_corner_triangular_weldo(corner1o, batten_thickness, lace_width-20, 'xz',"negative")

    corner2ob=(column_length-20,20,0)
    tri_weld2ob=create_corner_triangular_weld(corner2ob, batten_thickness, lace_width-20, 'xz',"negative")

    corner1ob=(column_length-20, 
                lace_width+column_distance-100, 
                0)
    tri_weld1ob = create_corner_triangular_weld(corner1ob, batten_thickness, lace_width-20, 'xz',"negative")


    batten_corner1=(column_length-20-batten_depth,20,0)
    tri_weld1b = create_corner_triangular_weld(batten_corner1,batten_thickness, batten_depth, 'yz',"negative")
    batten_corner2=(column_length-20-batten_depth,column_distance-100+2*lace_width-20,0)
    tri_weld2b = create_corner_triangular_weldo(batten_corner2,batten_thickness, batten_depth, 'yz',"negative")
    
    triangular_weld_shapes.extend([ tri_weld1o,tri_weld2o,tri_weld1ob,tri_weld2ob,tri_weld1b,tri_weld2b])
    # Combine all elements
    combined_structure = BRepAlgoAPI_Fuse(i_section1, i_section2).Shape()
    # combined_structure = BRepAlgoAPI_Fuse(combined_structure, bottom_batten_left).Shape()
    # combined_structure = BRepAlgoAPI_Fuse(combined_structure, bottom_batten_right).Shape()
    # combined_structure = BRepAlgoAPI_Fuse(combined_structure, top_batten_left).Shape()
    combined_structure = BRepAlgoAPI_Fuse(combined_structure, diagonal_plate).Shape()
    combined_structure = BRepAlgoAPI_Fuse(combined_structure, diagonal_plateo).Shape()
    # combined_structure = BRepAlgoAPI_Fuse(combined_structure, top_batten_right).Shape()
    combined_structure = BRepAlgoAPI_Fuse(combined_structure, diagonal_platet).Shape()
    combined_structure = BRepAlgoAPI_Fuse(combined_structure, diagonal_platetb).Shape()
    
    # Calculate diagonal lace length and spacing
    lace_spacing = i_section_height  # Distance between laces
    
    # Create diagonal laces
    

    for i in range(num_laces):
        # Create parallelogram (diagonal plate) using the new function
        p1 = gp_Pnt(batten_depth+i*column_distance+20,0, i_section_height)
        p2 = gp_Pnt(batten_depth+column_distance + i*column_distance,column_distance-100+lace_width, i_section_height)
        p3 = gp_Pnt(batten_depth+i*column_distance+20, 0+lace_width,i_section_height)

        v1 = gp_Vec(p3, p1)
        v2 = gp_Vec(p2, p1)

        # Compute angle between v1 and v2
        angle_rad = v1.Angle(v2)
        angle_deg = math.degrees(angle_rad)

        # print("Angle between p3→p1 and p2→p1 is:", angle_deg, "degrees")

        if(i==0):
            corner1 = (batten_depth+i*column_distance, 
                      0+20, 
                      i_section_height)
            
            corner1o = (batten_depth+i*column_distance+20, 
                      0, 
                      i_section_height)
            tri_weld1o = create_corner_triangular_weldo(corner1o, lace_thickness, lace_width, 'xz')
            corner2=(batten_depth+i*column_distance,lace_width+column_distance-100,i_section_height)
            corner2o=(batten_depth+i*column_distance+20,lace_width+column_distance-100,i_section_height)
            tri_weld2o = create_corner_triangular_weldo(corner2o, 2*lace_thickness, lace_width, 'xz')
            tri_weld2 = create_corner_triangular_weld(corner2, batten_thickness, lace_width-20, 'xz')
            tri_weld1 = create_corner_triangular_weld(corner1, batten_thickness, lace_width-20, 'xz')
            triangular_weld_shapes.extend([ tri_weld1,tri_weld1o,tri_weld2o,tri_weld2])

        else:
            corner1 = (batten_depth+i*column_distance, 
                        0, 
                        i_section_height)
            
            corner2=(batten_depth+i*column_distance,lace_width+column_distance-100,i_section_height)
            tri_weld2 = create_corner_triangular_weld(corner2, lace_thickness, lace_width, 'xz')

            corner2o=(batten_depth+i*column_distance+20,lace_width+column_distance-100,i_section_height)
            tri_weld2o=create_corner_triangular_weldo(corner2o, 2*lace_thickness, lace_width, 'xz')

            corner1o=(batten_depth+i*column_distance+20, 
                      0, 
                      i_section_height)
            tri_weld1 = create_corner_triangular_weld(corner1, 2*lace_thickness, lace_width, 'xz')
            corner1o=(batten_depth+i*column_distance+20, 
                      0, 
                      i_section_height)
            tri_weld1o = create_corner_triangular_weldo(corner1o, lace_thickness, lace_width, 'xz')

            triangular_weld_shapes.extend([ tri_weld1,tri_weld1o,tri_weld2,tri_weld2o])


        left_edge_start = (batten_depth+i*column_distance+20, 0, i_section_height)
        left_edge_end = (batten_depth+i*column_distance+20+(lace_width*math.tan(angle_rad)), lace_width, i_section_height)
        left_thickness_weld = create_edge_weld(left_edge_start, left_edge_end, 8, 'z')
        triangular_weld_shapes.append(left_thickness_weld)

        left_edge_starto = (batten_depth+i*column_distance+20, column_distance-100+2*lace_width, i_section_height)
        left_edge_endo = (batten_depth+i*column_distance+20+(lace_width*math.tan(angle_rad)), column_distance-100+lace_width, i_section_height)
        left_thickness_weldo = create_edge_weld(left_edge_starto, left_edge_endo, 2*lace_thickness, 'z')
        triangular_weld_shapes.append(left_thickness_weldo)


         

        po1 = gp_Pnt(batten_depth+i*column_distance+column_distance,0+lace_width, i_section_height+lace_thickness)
        po2 = gp_Pnt(batten_depth+i*column_distance+20,column_distance-100+2*lace_width, i_section_height+lace_thickness)
        po3 = gp_Pnt(batten_depth+i*column_distance+column_distance, 0,i_section_height+lace_thickness)
        

        v1 = gp_Vec(po1, po3)
        po4 = gp_Pnt(po2.XYZ() + v1.XYZ())
        v2 = gp_Vec(po4, po3)
        # Compute angle between v1 and v2
        angle_rad = v1.Angle(v2)
        angle_deg = math.degrees(angle_rad)

        # print("Angle between p3→p1 and p2→p1 is:", angle_deg, "degrees")
        if(i!=0):
            right_edge_start = (batten_depth+ i*column_distance, 0, i_section_height)
            right_edge_end = (batten_depth+i*column_distance-(lace_width*math.tan(angle_rad)), lace_width, i_section_height)
            right_thickness_weld = create_edge_weldo(right_edge_start, right_edge_end, 2*lace_thickness, 'z')
            triangular_weld_shapes.append(right_thickness_weld)


            right_edge_starto = (batten_depth+ i*column_distance, column_distance-100+2*lace_width, i_section_height)
            right_edge_endo = (batten_depth+i*column_distance-(lace_width*math.tan(angle_rad)), column_distance-100+lace_width, i_section_height)
            right_thickness_weldo = create_edge_weldo(right_edge_starto, right_edge_endo, lace_thickness, 'z')
            triangular_weld_shapes.append(right_thickness_weldo)





        # Create solid from the face and add to structure
        diagonal_plate = create_parallelogram_face(p1, p2, p3, lace_thickness)
        combined_structure = BRepAlgoAPI_Fuse(combined_structure, diagonal_plate).Shape()
        diagonal_plateo = create_parallelogram_face(po1, po2, po3, lace_thickness)
        combined_structure = BRepAlgoAPI_Fuse(combined_structure, diagonal_plateo).Shape() 

        from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Section
        from OCC.Core.TopoDS import TopoDS_Shape
        from OCC.Core.BRep import BRep_Tool
        from OCC.Core.TopExp import TopExp_Explorer
        from OCC.Core.TopAbs import TopAbs_VERTEX

        # Compute section (even if it's just an edge or vertex)
        from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Section
        from OCC.Core.gp import gp_Pnt

        def point_key(pnt, tol=1e-2):
            # Round to eliminate precision errors; customize tolerance if needed
            return (round(pnt.X(), 2), round(pnt.Y(), 2), round(pnt.Z(), 2))

        # Build section
        section_algo = BRepAlgoAPI_Section(diagonal_plate, diagonal_plateo, False)
        section_algo.ComputePCurveOn1(True)
        section_algo.Approximation(True)
        section_algo.Build()

        if not section_algo.IsDone():
            print(f"Section at i={i} failed.")
        else:
            section_shape = section_algo.Shape()

            # Explore unique vertices
            explorer = TopExp_Explorer(section_shape, TopAbs_VERTEX)
            unique_points = dict()

            while explorer.More():
                vertex = explorer.Current()
                pnt = BRep_Tool.Pnt(vertex)
                key = point_key(pnt)

                if key not in unique_points and len(unique_points) < 4:
                    unique_points[key] = pnt
                    # print(f"Touching Point at i={i}: ({pnt.X():.2f}, {pnt.Y():.2f}, {pnt.Z():.2f})")

                    # right_edge_start = ()
                    # right_edge_end = (batten_depth+i*column_distance-2*(lace_width*math.tan(angle_rad))-430/2, 2*lace_width+430/2, i_section_height+lace_thickness)
                    # right_thickness_weld = create_edge_weldo(right_edge_start, right_edge_end, 2*lace_thickness, 'z')
                    # triangular_weld_shapes.append(right_thickness_weld)
            
                explorer.Next()
            keys = list(unique_points)
            # print(keys)
            right_edge_start = (keys[1][0],keys[1][1],keys[1][2])
            right_edge_end = (keys[0][0],keys[0][1],keys[0][2])
            v1 = gp_Vec(p3, p1)
            v2 = gp_Vec(p2, p1)

            # Compute angle between v1 and v2
            angle_rad = v1.Angle(v2)
            angle_deg = math.degrees(angle_rad)
            right_thickness_weld = create_edge_weldo(right_edge_start, right_edge_end, lace_thickness, 'z',lace_thickness,angle_rad)
            triangular_weld_shapes.append(right_thickness_weld)

            left_edge_start = (keys[2][0],keys[2][1],keys[2][2])
            left_edge_end = (keys[3][0],keys[3][1],keys[3][2])
            left_thickness_weld = create_edge_weld(left_edge_start, left_edge_end, lace_thickness, 'z',lace_thickness,angle_rad)
            triangular_weld_shapes.append(left_thickness_weld)

        
        # display.DisplayColoredShape(intersection, Quantity_Color(1, 0, 0, 1), update=True)  # Red
    
        # Create backward diagonal lace (\)

        
        b_p1 = gp_Pnt(batten_depth+column_distance+i*column_distance, column_distance, -2*lace_thickness)  # Bottom left
        b_p2 = gp_Pnt(batten_depth + i*column_distance+20, 0, -2*lace_thickness)  # Bottom right
        b_p3 = gp_Pnt(batten_depth+column_distance+i*column_distance, column_distance+lace_width, -2*lace_thickness)  # Top left


        b_p1o = gp_Pnt(batten_depth+i*column_distance+20, column_distance-100+2*lace_width, -lace_thickness)  # Bottom left
        b_p2o = gp_Pnt(batten_depth + i*column_distance+column_distance, lace_width, -lace_thickness)  # Bottom right
        b_p3o = gp_Pnt(batten_depth+i*column_distance+20, column_distance-100+lace_width, -lace_thickness)  # Top left


        if(i==0):
            corner1 = (batten_depth+i*column_distance, 
                        lace_width+column_distance-100, 
                        0)
            
            corner2=(batten_depth+i*column_distance,0+20,0)
            tri_weld2 = create_corner_triangular_weld(corner2, batten_thickness, lace_width-20, 'xz',"negative")

            corner2o=(batten_depth+i*column_distance+20,0,0)
            tri_weld2o=create_corner_triangular_weldo(corner2o, 2*lace_thickness, lace_width, 'xz',"negative")

            corner1o=(batten_depth+i*column_distance+20, 
                      lace_width+column_distance-100, 
                      0)
            tri_weld1 = create_corner_triangular_weld(corner1, batten_thickness, lace_width-20, 'xz',"negative")
            # corner1o=(batten_depth+i*column_distance+20, 
            #           0, 
            #           -lace_thickness)
            tri_weld1o = create_corner_triangular_weldo(corner1o, lace_thickness, lace_width, 'xz',"negative")

            triangular_weld_shapes.extend([ tri_weld1,tri_weld1o,tri_weld2,tri_weld2o])

        else:
            corner1 = (batten_depth+i*column_distance, 
                        lace_width+column_distance-100, 
                        0)
            
            corner2=(batten_depth+i*column_distance,0,0)
            tri_weld2 = create_corner_triangular_weld(corner2, lace_thickness, lace_width, 'xz',"negative")

            corner2o=(batten_depth+i*column_distance+20,0,0)
            tri_weld2o=create_corner_triangular_weldo(corner2o, 2*lace_thickness, lace_width, 'xz',"negative")

            corner1o=(batten_depth+i*column_distance+20, 
                      lace_width+column_distance-100, 
                      0)
            tri_weld1 = create_corner_triangular_weld(corner1, 2*lace_thickness, lace_width, 'xz',"negative")
            # corner1o=(batten_depth+i*column_distance+20, 
            #           0, 
            #           -lace_thickness)
            tri_weld1o = create_corner_triangular_weldo(corner1o, lace_thickness, lace_width, 'xz',"negative")

            triangular_weld_shapes.extend([ tri_weld1,tri_weld1o,tri_weld2,tri_weld2o])


        # if(i!=0):
        left_edge_start = (batten_depth+i*column_distance+20, column_distance-100+2*lace_width, 0)
        left_edge_end = (batten_depth+i*column_distance+20+(lace_width*math.tan(angle_rad)), column_distance-100+lace_width, 0)
        left_thickness_weld = create_edge_weld(left_edge_start, left_edge_end, 8, 'z',flag="negative")
        triangular_weld_shapes.append(left_thickness_weld)

        left_edge_starto = (batten_depth+i*column_distance+20, 0, 0)
        left_edge_endo = (batten_depth+i*column_distance+20+(lace_width*math.tan(angle_rad)), lace_width, 0)
        left_thickness_weldo = create_edge_weld(left_edge_starto, left_edge_endo, 2*lace_thickness, 'z',flag="negative")
        triangular_weld_shapes.append(left_thickness_weldo)
        
        if(i!=0):
            right_edge_start = (batten_depth+ i*column_distance, column_distance-100+2*lace_width, 0)
            right_edge_end = (batten_depth+i*column_distance-(lace_width*math.tan(angle_rad)), column_distance-100+lace_width, 0)
            right_thickness_weld = create_edge_weldo(right_edge_start, right_edge_end, 2*lace_thickness, 'z',flag="negative")
            triangular_weld_shapes.append(right_thickness_weld)


            right_edge_starto = (batten_depth+ i*column_distance, 0,0)
            right_edge_endo = (batten_depth+i*column_distance-(lace_width*math.tan(angle_rad)),lace_width, 0)
            right_thickness_weldo = create_edge_weldo(right_edge_starto, right_edge_endo, lace_thickness, 'z',flag="negative")
            triangular_weld_shapes.append(right_thickness_weldo)
    
    # Create backward diagonal plate
        backward_diagonal_plate = create_parallelogram_face(b_p1, b_p2, b_p3, lace_thickness)
        combined_structure = BRepAlgoAPI_Fuse(combined_structure, backward_diagonal_plate).Shape()
        backward_diagonal_plateo = create_parallelogram_face(b_p1o, b_p2o, b_p3o, lace_thickness)
        combined_structure = BRepAlgoAPI_Fuse(combined_structure, backward_diagonal_plateo).Shape()


        # Create horizontal connecting laces
        
        # Add horizontal laces to structure

        section_algo = BRepAlgoAPI_Section(backward_diagonal_plate, backward_diagonal_plateo, False)
        section_algo.ComputePCurveOn1(True)
        section_algo.Approximation(True)
        section_algo.Build()

        if not section_algo.IsDone():
            print(f"Section at i={i} failed.")
        else:
            section_shape = section_algo.Shape()

            # Explore unique vertices
            explorer = TopExp_Explorer(section_shape, TopAbs_VERTEX)
            unique_points = dict()

            while explorer.More():
                vertex = explorer.Current()
                pnt = BRep_Tool.Pnt(vertex)
                key = point_key(pnt)

                if key not in unique_points and len(unique_points) < 4:
                    unique_points[key] = pnt
                    # print(f"Touching Point at i={i}: ({pnt.X():.2f}, {pnt.Y():.2f}, {pnt.Z():.2f})")

                    # right_edge_start = ()
                    # right_edge_end = (batten_depth+i*column_distance-2*(lace_width*math.tan(angle_rad))-430/2, 2*lace_width+430/2, i_section_height+lace_thickness)
                    # right_thickness_weld = create_edge_weldo(right_edge_start, right_edge_end, 2*lace_thickness, 'z')
                    # triangular_weld_shapes.append(right_thickness_weld)
            
                explorer.Next()
            keys = list(unique_points)
            print(keys)
            right_edge_start = (keys[0][0],keys[0][1],keys[0][2])
            right_edge_end = (keys[2][0],keys[2][1],keys[2][2])
            right_thickness_weld = create_edge_weldo(right_edge_start, right_edge_end, lace_thickness, 'z',lace_thickness,angle_rad,"negative")
            triangular_weld_shapes.append(right_thickness_weld)

            left_edge_start = (keys[3][0],keys[3][1],keys[3][2])
            left_edge_end = (keys[1][0],keys[1][1],keys[1][2])
            left_thickness_weld = create_edge_weld(left_edge_start, left_edge_end, lace_thickness, 'z',lace_thickness,angle_rad,"negative")
            triangular_weld_shapes.append(left_thickness_weld)
    
    # Add final diagonal lace at the end

    right_edge_start = (batten_depth+ num_laces*column_distance, 0, i_section_height)
    right_edge_end = (batten_depth+num_laces*column_distance-(lace_width*math.tan(angle_rad)), lace_width, i_section_height)
    right_thickness_weld = create_edge_weldo(right_edge_start, right_edge_end, 2*lace_thickness, 'z')
    triangular_weld_shapes.append(right_thickness_weld)

    right_edge_starto = (batten_depth+ num_laces*column_distance, column_distance-100+2*lace_width, i_section_height)
    right_edge_endo = (batten_depth+num_laces*column_distance-(lace_width*math.tan(angle_rad)), column_distance-100+lace_width, i_section_height)
    right_thickness_weldo = create_edge_weldo(right_edge_starto, right_edge_endo, lace_thickness, 'z')
    triangular_weld_shapes.append(right_thickness_weldo)

    right_edge_start = (batten_depth+ num_laces*column_distance, column_distance-100+2*lace_width, 0)
    right_edge_end = (batten_depth+num_laces*column_distance-(lace_width*math.tan(angle_rad)), column_distance-100+lace_width, 0)
    right_thickness_weld = create_edge_weldo(right_edge_start, right_edge_end, 2*lace_thickness, 'z',flag="negative")
    triangular_weld_shapes.append(right_thickness_weld)


    right_edge_starto = (batten_depth+ num_laces*column_distance, 0,0)
    right_edge_endo = (batten_depth+num_laces*column_distance-(lace_width*math.tan(angle_rad)),lace_width, 0)
    right_thickness_weldo = create_edge_weldo(right_edge_starto, right_edge_endo, lace_thickness, 'z',flag="negative")
    triangular_weld_shapes.append(right_thickness_weldo)

    corner1 = (batten_depth+num_laces*column_distance, 
            lace_width+column_distance-100, 
            0)

    corner2=(batten_depth+num_laces*column_distance,0,0)
    tri_weld2 = create_corner_triangular_weld(corner2, lace_thickness, lace_width, 'xz',"negative")
    tri_weld1 = create_corner_triangular_weld(corner1, 2*lace_thickness, lace_width, 'xz',"negative")
    triangular_weld_shapes.append([tri_weld1,tri_weld2])
    # Display the structure
    display, start_display, add_menu, add_function_to_menu = init_display()
    
    # Display main structure in default color
    display.DisplayShape(combined_structure, update=False)
    
    # Display triangular fillet welds in red color

    # display.DisplayColoredShape(intersection, Quantity_Color(1, 0, 0, 1), update=True)  # Red
    red_color = Quantity_Color(Quantity_NOC_RED)
    for tri_weld in triangular_weld_shapes:
        display.DisplayColoredShape(tri_weld, red_color, update=False)
    
    display.FitAll()
    start_display()