from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform, BRepBuilderAPI_MakeEdge
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf, gp_Dir, gp_Ax1, gp_Pnt
from OCC.Core.TopoDS import TopoDS_Edge
from OCC.Display.SimpleGui import init_display
import math

def create_c_section(length=1000, depth=200, flange_width=80, web_thickness=10, flange_thickness=10):
    # Create points for the C-section profile (in Y-Z plane)
    points = [
        gp_Pnt(0, 0, 0),                        # Bottom-left corner
        gp_Pnt(0, 0, depth),                    # Top-left corner
        gp_Pnt(0, -flange_width, depth),        # Top-right of upper flange
        gp_Pnt(0, -flange_width, depth-flange_thickness),  # Bottom-right of upper flange
        gp_Pnt(0, -web_thickness, depth-flange_thickness), # Top-right of web
        gp_Pnt(0, -web_thickness, flange_thickness),       # Bottom-right of web
        gp_Pnt(0, -flange_width, flange_thickness),        # Top-right of lower flange
        gp_Pnt(0, -flange_width, 0),            # Bottom-right of lower flange
    ]
    
    # Create edges
    edges = []
    for i in range(len(points)-1):
        edge = BRepBuilderAPI_MakeEdge(points[i], points[i+1]).Edge()
        edges.append(edge)
    
    # Close the profile
    edge = BRepBuilderAPI_MakeEdge(points[-1], points[0]).Edge()
    edges.append(edge)
    
    # Create wire from edges
    wire_builder = BRepBuilderAPI_MakeWire()
    for edge in edges:
        wire_builder.Add(edge)
    wire = wire_builder.Wire()
    
    # Create face from wire
    face = BRepBuilderAPI_MakeFace(wire).Face()
    
    # Extrude along X-axis to create the beam
    vec = gp_Vec(length, 0, 0)
    beam = BRepPrimAPI_MakePrism(face, vec).Shape()
    
    # Create and apply the rotation transformation
    trsf = gp_Trsf()
    rotation_axis_z = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
    trsf.SetRotation(rotation_axis_z, math.pi/2)
    beam_transformed = BRepBuilderAPI_Transform(beam, trsf).Shape()
    
    return beam_transformed

def main():
    # Initialize display
    display, start_display, add_menu, add_function_to_menu = init_display()
    
    # Create the C-section beam
    beam = create_c_section()
    
    # Display the beam
    display.DisplayShape(beam, update=True)
    
    # Set view
    display.View_Iso()
    display.FitAll()
    
    # Start the display
    start_display()

if __name__ == "__main__":
    main()