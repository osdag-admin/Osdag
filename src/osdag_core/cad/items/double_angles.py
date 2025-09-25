from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from .angle import Angle
from .Gasset_plate import GassetPlate
import numpy

class BackToBackAnglesWithGussetsSameSide:
    def __init__(self, L, A, B, T, R1, R2, gusset_L, gusset_H, gusset_T, gusset_degree, spacing=2):
        """
        Creates back-to-back angles with gusset plates automatically positioned at the ends
        Args:
            L: Length of the angle
            A: Vertical leg length
            B: Horizontal leg length
            T: Thickness
            R1, R2: Corner radii
            gusset_L: Length of gusset plate
            gusset_H: Height of gusset plate
            gusset_T: Thickness of gusset plate
            gusset_degree: Angle of gusset plate
            spacing: Gap between angles
        """
        self.angle1 = Angle(L, A, B, T, R1, R2)
        self.angle2 = Angle(L, B, A, T, R1, R2)
        self.gusset1 = GassetPlate(gusset_L, gusset_H, gusset_T, gusset_degree)
        self.gusset2 = GassetPlate(gusset_L, gusset_H, gusset_T, gusset_degree)
        self.spacing = spacing
        
        # Store dimensions for later use
        self.L = L
        self.A = A  # Vertical leg length
        self.B = B  # Horizontal leg length
        self.T = T  # Angle thickness
        self.gusset_L = gusset_L
        self.gusset_H = gusset_H
        self.gusset_T = gusset_T
        
        # Calculate Z-offsets based on angle length
        # Position plates at the ends with a small margin
        margin = gusset_L/2  # Adjust this value to fine-tune the end position
        self.gusset1_offsets = numpy.array([0, 0, margin])  # At the start
        self.gusset2_offsets = numpy.array([0, 0, L - margin])  # At the end
        
        # Base origin and directions
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.vDir = numpy.cross(self.wDir, self.uDir)

    def place(self, sec_origin, uDir, wDir):
        """Places the angles and gusset plates with automatic end positioning"""
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.vDir = numpy.cross(self.wDir, self.uDir)
        
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.vDir = numpy.cross(self.wDir, self.uDir)

        # Place first angle with offset to center on gusset
        angle1_origin = self.sec_origin
        rotated_uDir_angle1 = -self.vDir  # Point the horizontal leg towards negative y
        rotated_vDir_angle1 = -self.uDir  # Adjust vertical direction accordingly
        self.angle1.place(angle1_origin, rotated_uDir_angle1, self.wDir)
        
        # Place second angle with spacing
        angle2_origin = angle1_origin + self.spacing * self.vDir
        rotated_uDir = self.uDir
        rotated_vDir = -self.vDir
        self.angle2.place(angle2_origin, rotated_uDir, self.wDir)
        
        # Calculate center point between angles
        center_point = self.sec_origin + (self.spacing / 2) * self.vDir
        
        # Place first gusset plate at the start
        gusset1_origin = (
            center_point 
            + self.gusset1_offsets[0] * self.uDir  # X offset (0)
            + self.gusset1_offsets[1] * self.vDir  # Y offset (0)
            + self.gusset1_offsets[2] * self.wDir  # Z offset (start position)
        )
        gusset1_uDir = numpy.array([0, 0, 1.0])
        gusset1_wDir = numpy.array([0, -1.0, 0])
        self.gusset1.place(gusset1_origin, gusset1_uDir, gusset1_wDir)
        
        # Place second gusset plate at the end
        gusset2_origin = (
            center_point 
            + self.gusset2_offsets[0] * self.uDir  # X offset (0)
            + self.gusset2_offsets[1] * self.vDir  # Y offset (0)
            + self.gusset2_offsets[2] * self.wDir  # Z offset (end position)
        )
        gusset2_uDir = numpy.array([0, 0, -1.0])
        gusset2_wDir = numpy.array([0, 1.0, 0])
        self.gusset2.place(gusset2_origin, gusset2_uDir, gusset2_wDir)



    def create_model(self):
        """Creates the 3D model of back-to-back angles with gusset plates"""
        # Create models
        angle1_prism = self.angle1.create_model()
        angle2_prism = self.angle2.create_model()
        gusset1_prism = self.gusset1.create_model()
        gusset2_prism = self.gusset2.create_model()
        
        # Combine all shapes
        combined_angles = BRepAlgoAPI_Fuse(angle1_prism, angle2_prism).Shape()
        combined_with_gusset1 = BRepAlgoAPI_Fuse(combined_angles, gusset1_prism).Shape()
        final_shape = BRepAlgoAPI_Fuse(combined_with_gusset1, gusset2_prism).Shape()
        
        return final_shape

class BackToBackAnglesWithGussetsOppSide:
    def __init__(self, L, A, B, T, R1, R2, gusset_L, gusset_H, gusset_T, gusset_degree, spacing=2):
        """
        Creates back-to-back angles with gusset plates automatically positioned at the ends and perfectly centered
        Args:
            L: Length of the angle
            A: Vertical leg length
            B: Horizontal leg length
            T: Thickness
            R1, R2: Corner radii
            gusset_L: Length of gusset plate
            gusset_H: Height of gusset plate (width of the shorter end)
            gusset_T: Thickness of gusset plate
            gusset_degree: Angle of gusset plate
            spacing: Gap between angles (including both angle thicknesses)
        """
        self.angle1 = Angle(L, A, B, T, R1, R2)
        self.angle2 = Angle(L, B, A, T, R1, R2)
        self.gusset1 = GassetPlate(gusset_L, gusset_H, gusset_T, gusset_degree)
        self.gusset2 = GassetPlate(gusset_L, gusset_H, gusset_T, gusset_degree)
        self.spacing = spacing
        
        # Store dimensions for later use
        self.L = L
        self.A = A  # Vertical leg length
        self.B = B  # Horizontal leg length
        self.T = T  # Angle thickness
        self.gusset_L = gusset_L
        self.gusset_H = gusset_H
        self.gusset_T = gusset_T
        
        # Calculate Z-offsets based on angle length
        margin = gusset_L/2
        
        # Calculate X offset to center the double angle on gusset plate width
        x_offset = gusset_H/2  # Center of gusset plate width
        
        # Calculate Y offset for gusset plates
        # For gusset1, we need to account for its forward growth by adding half its thickness
        gusset1_y_offset = spacing/2 + gusset_T/2.0
        # For gusset2, we can use the center point since it grows backwards
        gusset2_y_offset = spacing/2 - gusset_T/2.0
        
        self.gusset1_offsets = numpy.array([x_offset, gusset1_y_offset, margin])  
        self.gusset2_offsets = numpy.array([x_offset, gusset2_y_offset, L - margin])
        
        # Base origin and directions
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.vDir = numpy.cross(self.wDir, self.uDir)

    def place(self, sec_origin, uDir, wDir):
        """Places the angles and gusset plates with perfect centering on both axes"""
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.vDir = numpy.cross(self.wDir, self.uDir)
        
        # Calculate the offset needed to center angles on gusset plate
        x_center_offset = (self.gusset_H - self.A)/2
        
        # Place first angle with offset to center on gusset
        angle1_origin = self.sec_origin + x_center_offset * self.uDir
        rotated_uDir_angle1 = -self.vDir  # Point the horizontal leg towards negative y
        rotated_vDir_angle1 = -self.uDir  # Adjust vertical direction accordingly
        self.angle1.place(angle1_origin, rotated_uDir_angle1, self.wDir)
        
        # Place second angle with spacing
        angle2_origin = angle1_origin + self.spacing * self.vDir
        rotated_uDir = self.uDir
        rotated_vDir = -self.vDir
        self.angle2.place(angle2_origin, rotated_uDir, self.wDir)
        
        # Place first gusset plate
        gusset1_origin = (
            self.sec_origin 
            + self.gusset1_offsets[0] * self.uDir  # X offset (centered)
            + self.gusset1_offsets[1] * self.vDir  # Y offset (adjusted for forward growth)
            + self.gusset1_offsets[2] * self.wDir  # Z offset (start position)
        )
        gusset1_uDir = numpy.array([0, 0, 1.0])
        gusset1_wDir = numpy.array([1.0, 0, 0])
        self.gusset1.place(gusset1_origin, gusset1_uDir, gusset1_wDir)
        
        # Place second gusset plate
        gusset2_origin = (
            self.sec_origin 
            + self.gusset2_offsets[0] * self.uDir  # X offset (centered)
            + self.gusset2_offsets[1] * self.vDir  # Y offset (at center point)
            + self.gusset2_offsets[2] * self.wDir  # Z offset (end position)
        )
        gusset2_uDir = numpy.array([0, 0, -1.0])
        gusset2_wDir = numpy.array([1.0, 0, 0])
        self.gusset2.place(gusset2_origin, gusset2_uDir, gusset2_wDir)

    def create_model(self):
        """Creates the 3D model of back-to-back angles with gusset plates"""
        # Create models
        angle1_prism = self.angle1.create_model()
        angle2_prism = self.angle2.create_model()
        gusset1_prism = self.gusset1.create_model()
        gusset2_prism = self.gusset2.create_model()
        
        # Combine all shapes
        angle1_with_gusset = BRepAlgoAPI_Fuse(angle1_prism, gusset1_prism).Shape()
        angle2_with_gusset = BRepAlgoAPI_Fuse(angle2_prism, gusset2_prism).Shape()
        final_shape = BRepAlgoAPI_Fuse(angle1_with_gusset, angle2_with_gusset).Shape()
        
        return final_shape
    


if __name__ == '__main__':
    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    # Example dimensions for angles
    L = 2000   # Length
    A = 200   # Vertical leg length
    B = 300   # Horizontal leg length
    T = 18    # Thickness
    R1 = 15   # Inner corner radius
    R2 = 4.8  # Outer corner radius
    spacing = 8  # Gap between angles

    # Example dimensions for gusset plates
    gusset_L = 200  # Length
    gusset_H = 200  # Height
    gusset_T =8   # Thickness
    gusset_degree = 30  # Angle in degrees

    # Create and display the assembly
    origin = numpy.array([0., 0., 0.])
    uDir = numpy.array([1., 0., 0.])
    wDir = numpy.array([0., 0., 1.])

    print("Creating back-to-back angles with symmetric gusset plates...")
    assembly = BackToBackAnglesWithGussetsOppSide(L, A, B, T, R1, R2, gusset_L, gusset_H, gusset_T, gusset_degree, spacing)
    assembly.place(origin, uDir, wDir)
    shape = assembly.create_model()
    display.DisplayShape(shape, update=True)
    
    display.DisableAntiAliasing()
    start_display()
