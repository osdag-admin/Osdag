
import sys
import os
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from OCC.Display.SimpleGui import init_display
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB

# Import CAD items
from osdag_core.cad.items.ISection import ISection
from osdag_core.cad.items.plate import Plate
from osdag_core.cad.items.stiffener_plate import StiffenerPlate
from osdag_core.cad.items.bolt import Bolt
from osdag_core.cad.items.nut import Nut
from osdag_core.cad.items.groove_weld import GrooveWeld
from osdag_core.cad.MomentConnections.CCEndPlateCAD.CAD import CCEndPlateCAD
from osdag_core.cad.MomentConnections.CCEndPlateCAD.nutBoltPlacement import NutBoltArray

# ==============================================================================
# PARAMETERS
# ==============================================================================

# Column (ISLB 350 - User Request "Beam's dimension LB 350")
COL_D = 250.0
COL_B = 250.0
COL_T = 9.7
COL_t = 6.9
COL_R1 = 13.0
COL_R2 = 6.5
COL_ALPHA = 94.0
COL_ALPHA = 94.0
COL_LENGTH = 541.5 # Standardized Length

# End Plate
# User: Height 570, Length 250, Thickness 50.
# In Code: L=Height (Vertical), W=Width (Horizontal).
EP_HEIGHT = 570.0 # L
EP_WIDTH = 250.0 # W
EP_THICKNESS = 50.0

# Stiffener
# User: Height 100, Width 110, Thickness 6.
# In Code: L=Vertical Dimension (Extension coverage), W=Horizontal (Along Col Length).
STIFF_L = 100.0
STIFF_W = 110.0
STIFF_T = 6.0

# Bolts
# 27mm, Grade 4.8.
BOLT_DIA = 27.0
BOLT_GRADE = 4.8
BOLT_NUM = 12

PITCH = 67.5
END_DIST = 55.0

# Mock Config
class MockConfig:
    def __init__(self):
        # Logic derivation:
        # Extended Both Ways.
        # Want 12 bolts total. 2 columns.
        # So 6 rows.
        # Extended Both Ways logic: row = n_bw + 2.
        # So Set n_bw = 4. (Gives 6 rows).
        # Set n_bf = 1. (Gives col = n_bf * 2 = 2).
        self.n_bw = 4
        self.n_bf = 1
        self.no_bolts = 12
        
        self.end_dist = END_DIST
        self.pitch = PITCH
        self.p_2_web = PITCH # Uniform spacing
        self.p_2_flange = 0.0 # Not used for col=2 (Calculated by edge logic)
        
        self.connection = "Extended Both Ways"
        self.weld_type = "Groove Weld"

def generate_cad():
    # 1. Column
    column = ISection(B=COL_B, T=COL_T, D=COL_D, t=COL_t,
                      R1=COL_R1, R2=COL_R2, alpha=COL_ALPHA,
                      length=COL_LENGTH, notchObj=None)
    
    # 2. End Plate
    endPlate = Plate(L=EP_HEIGHT, W=EP_WIDTH, T=EP_THICKNESS)
    
    
    # 3. Weld
    # Groove Weld
    flangeWeld = GrooveWeld(b=COL_T, h=20, L=COL_B)
    webWeld = GrooveWeld(b=COL_t, h=20, L=COL_D - 2*COL_T)
    
    # 4. Bolts
    bolt = Bolt(R=BOLT_DIA*1.5/2, T=BOLT_DIA*0.6, H=50, r=BOLT_DIA/2)
    nut = Nut(R=BOLT_DIA*1.5/2, T=BOLT_DIA, H=BOLT_DIA, innerR1=BOLT_DIA/2)
    
    # Grip: 2 Plates.
    nut_space = 2 * EP_THICKNESS
    
    config = MockConfig()
    
    # FIX for Bolt Offset:
    # NutBoltArray calculates edge distance based on 'column.B'.
    # But CAD.py places the array origin at 'endPlate.W/2'.
    # If Plate Width (250) != Column Width (165), the bolts are offset by (W-B)/2.
    # To center them, we pass a Proxy Column to NutBoltArray with B = Plate Width.
    import copy
    proxy_column = copy.copy(column)
    proxy_column.B = EP_WIDTH # Force calc to reference Plate Width
    
    nut_bolt_array = NutBoltArray(config, proxy_column, nut, bolt, nut_space)
    
    # 5. Stiffener
    # User Request: 
    # 1. "Red lines": Remove Top-Outer corner -> Increase L11/L12.
    # 2. "Blue lines": Add Bottom-Inner cutout -> Add R21/R22.
    # 3. "Touch till the end of end plate": Restore Projection Length (L) to 110.
    #    (570/2 - 350/2 = 110).
    
    STIFF_L_NEW = 100.0
    STIFF_W_NEW = 100.0
    
    # Outer-Top (L11/L12): Large Chamfer. 50x50.
    # Inner-Top (R11/R12): Sharp (0.01).
    # Inner-Bottom (R21/R22): Cutout (Snipe). 15x15.
    # Outer-Bottom (L21/L22): Sharp (0.01).
    
    stiffener = StiffenerPlate(L=STIFF_L_NEW, W=STIFF_W_NEW, T=STIFF_T, 
                               L11=50, L12=50, 
                               R11=0.01, R12=0.01, 
                               R21=15, R22=15, 
                               L21=0.01, L22=0.01)
    
    # Welds for Stiffener
    # Horizontal (Along Projection L): Length 110. Cut 15 at start (Inner).
    weld_stiff_h = GrooveWeld(b=STIFF_T, h=10, L=STIFF_L_NEW - 15)
    
    # Vertical (Along Height W against Flange): Length 100. Cut 15 at start (Bottom).
    weld_stiff_v = GrooveWeld(b=STIFF_T, h=10, L=STIFF_W_NEW - 15)
    
    # 6. Assemble
    CCEndPlate = CCEndPlateCAD(config, column, endPlate, flangeWeld, webWeld, 
                               nut_bolt_array, stiffener, weld_stiff_h, weld_stiff_v)
                               
    CCEndPlate.create_3DModel()
    return CCEndPlate

if __name__ == '__main__':
    display, start_display, add_menu, add_function_to_menu = init_display()
    
    try:
        model = generate_cad()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        start_display() # Keep window open
        sys.exit(1)
        
    # Colors
    from OCC.Core.Quantity import Quantity_NOC_BLACK, Quantity_NOC_SADDLEBROWN
    from osdag_core.utilities import color_the_edges
    
    column_color = Quantity_Color(0.28, 0.28, 0.21, Quantity_TOC_RGB) 
    # Colors from common_logic.py (lines 2564-2568)
    plate_color = Quantity_Color(47/255.0, 47/255.0, 35/255.0, Quantity_TOC_RGB) # Dark Olive
    weld_color = Quantity_Color(Quantity_NOC_SADDLEBROWN)
    bolt_color = Quantity_Color(Quantity_NOC_SADDLEBROWN)
    black_color = Quantity_Color(Quantity_NOC_BLACK)
    
    def display_with_edges(shape, color):
        if shape is None: return
        display.DisplayShape(shape, color=color, update=False)
        try:
            color_the_edges(shape, display, black_color, 0.5)
        except Exception as e:
            pass

    # Get Separate Models
    cols = model.get_column_models()
    plates = model.get_plate_models()
    bolts = model.get_nut_bolt_models()
    welds = model.get_weld_models()
    
    display_with_edges(cols, column_color)
    display_with_edges(plates, plate_color)
    display_with_edges(bolts, bolt_color)
    display_with_edges(welds, weld_color)
    
    # View
    try:
        display.View_Iso()
        display.FitAll()
        display.View.SetEye(1600, 1000, 500) 
        display.FitAll()
        display.ZoomFactor(0.9)
    except:
        display.View_Iso()
        
    filename = "col_end_plate_cad.png"
    print(f"Saving image to {filename}...")
    display.View.Dump(filename)
    start_display()
