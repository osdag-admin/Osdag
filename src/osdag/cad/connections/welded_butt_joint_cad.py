"""
Module: welded_butt_joint_cad.py
Description:
    WeldedButtJointCad is a CAD module that creates 3D models for welded butt joints.
    It follows the same structure and design logic as other CAD modules in Osdag.
"""

import numpy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from ...cad.items.plate import Plate
from ...cad.items.filletweld import FilletWeld
from ...cad.items.groove_weld import GrooveWeld
import copy

class WeldedButtJointCad(object):
    """
    Creates CAD models of Welded Butt Joint components
    """
    def __init__(self, connection_type, plate1, plate2, weld, 
                 cover_plates=None, packing_plate=None):
        """
        Initialize the parameters required for creating 3D models
        
        Args:
            connection_type: Type of the butt joint (complete/partial penetration or with cover plates)
            plate1: First plate being connected
            plate2: Second plate being connected
            weld: Weld joining the plates
            cover_plates: Cover plates for the joint (if applicable)
            packing_plate: Packing plate if plates have different thickness
        """
        self.connection_type = connection_type
        self.plate1 = plate1
        self.plate2 = plate2
        self.weld = weld
        self.cover_plates = cover_plates or []
        self.packing_plate = packing_plate
        
        self.plate1_model = None
        self.plate2_model = None
        self.weld_models = []
        self.cover_plate_models = []
        self.packing_plate_model = None
        
    def create_3DModel(self):
        """
        Create 3D model of the welded butt joint connection
        """
        # Create plate models
        self.create_plate_geometry()
        
        # Create weld geometry based on connection type
        if self.connection_type in ["Complete Penetration Butt Weld", "Partial Penetration Butt Weld"]:
            self.create_butt_weld_geometry()
        elif self.cover_plates:
            self.create_cover_plate_geometry()
            self.create_fillet_weld_geometry()
    
    def create_plate_geometry(self):
        """
        Create geometry for the connected plates
        """
        # Position plate1
        plate1_origin = numpy.array([0, 0, 0])
        plate1_uDir = numpy.array([1, 0, 0])
        plate1_wDir = numpy.array([0, 0, 1])
        self.plate1.place(plate1_origin, plate1_uDir, plate1_wDir)
        self.plate1_model = self.plate1.create_model()
        
        # Position plate2
        plate2_origin = numpy.array([self.plate1.L, 0, 0])
        plate2_uDir = numpy.array([1, 0, 0])
        plate2_wDir = numpy.array([0, 0, 1])
        self.plate2.place(plate2_origin, plate2_uDir, plate2_wDir)
        self.plate2_model = self.plate2.create_model()
    
    def create_butt_weld_geometry(self):
        """
        Create geometry for butt welds (complete/partial penetration)
        """
        # Position the weld at the joint of the two plates
        weld_origin = numpy.array([self.plate1.L/2, 0, 0])
        weld_uDir = numpy.array([0, 1, 0])
        weld_wDir = numpy.array([0, 0, 1])
        self.weld.place(weld_origin, weld_uDir, weld_wDir)
        
        # Create weld model
        weld_model = self.weld.create_model()
        self.weld_models.append(weld_model)
    
    def create_cover_plate_geometry(self):
        """
        Create geometry for cover plates in a cover plate butt joint
        """
        if not self.cover_plates:
            return
            
        for i, cover_plate in enumerate(self.cover_plates):
            # Position cover plates
            if i == 0:  # Top cover plate
                cp_origin = numpy.array([0, 0, self.plate1.T])
                cp_uDir = numpy.array([1, 0, 0])
                cp_wDir = numpy.array([0, 0, 1])
            else:  # Bottom cover plate
                cp_origin = numpy.array([0, 0, -self.cover_plates[i].T])
                cp_uDir = numpy.array([1, 0, 0])
                cp_wDir = numpy.array([0, 0, -1])
                
            cover_plate.place(cp_origin, cp_uDir, cp_wDir)
            cp_model = cover_plate.create_model()
            self.cover_plate_models.append(cp_model)
            
        # Position packing plate if needed
        if self.packing_plate:
            if float(self.plate1.T) < float(self.plate2.T):
                pack_origin = numpy.array([self.plate1.L, 0, 0])
            else:
                pack_origin = numpy.array([0, 0, 0])
                
            pack_uDir = numpy.array([1, 0, 0])
            pack_wDir = numpy.array([0, 0, 1])
            self.packing_plate.place(pack_origin, pack_uDir, pack_wDir)
            self.packing_plate_model = self.packing_plate.create_model()
    
    def create_fillet_weld_geometry(self):
        """
        Create geometry for fillet welds connecting cover plates
        """
        if not self.cover_plates:
            return
            
        # Create welds for each cover plate
        for i, cover_plate in enumerate(self.cover_plates):
            # Create welds at both ends of the cover plate
            weld_locations = [0, self.plate1.L + self.plate2.L]
            
            for loc in weld_locations:
                if i == 0:  # Top cover plate welds
                    weld_origin = numpy.array([loc, 0, self.plate1.T])
                    weld_uDir = numpy.array([0, 1, 0])
                    weld_wDir = numpy.array([0, 0, 1])
                else:  # Bottom cover plate welds
                    weld_origin = numpy.array([loc, 0, 0])
                    weld_uDir = numpy.array([0, 1, 0])
                    weld_wDir = numpy.array([0, 0, -1])
                
                # Create a copy of the weld for this location
                weld_copy = FilletWeld(b=self.weld.b, h=self.weld.h, L=self.plate1.W)
                weld_copy.place(weld_origin, weld_uDir, weld_wDir)
                weld_model = weld_copy.create_model()
                self.weld_models.append(weld_model)
    
    # Model accessor functions
    def get_plate_models(self):
        """Get models of the connected plates"""
        return [self.plate1_model, self.plate2_model]
        
    def get_weld_models(self):
        """Get models of all welds in the connection"""
        return self.weld_models
        
    def get_cover_plate_models(self):
        """Get models of cover plates if present"""
        return self.cover_plate_models
        
    def get_packing_plate_model(self):
        """Get model of the packing plate if present"""
        return [self.packing_plate_model] if self.packing_plate_model else []
        
    def get_models(self):
        """Get all models combined for the complete connection"""
        # Combine all models
        models = []
        models.extend(self.get_plate_models())
        models.extend(self.get_weld_models())
        models.extend(self.get_cover_plate_models())
        models.extend(self.get_packing_plate_model())
        
        # Fuse all models into a single CAD model
        if not models:
            return None
            
        result_model = models[0]
        for model in models[1:]:
            result_model = BRepAlgoAPI_Fuse(result_model, model).Shape()
            
        return result_model
