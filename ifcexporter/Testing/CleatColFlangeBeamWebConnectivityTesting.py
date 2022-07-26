from ifcexporter.IfcItems.IfcInitializer import *
from ifcexporter.IfcItems.RawDesign.ISection import ISection
from ifcexporter.IfcItems.RawDesign.Angle import Angle
from ifcexporter.IfcItems.Fastener import Fastener
import numpy as np
import json

class CleatColFlangeBeamWebConnectivity(IfcObject):
    def __init__(self, design_data, location_data, **kwgs):
        super().__init__(**kwgs)
        self.dd = design_data
        self.ld = location_data
        self.init_design_data()
        self.init_location_data()
        self.create_and_assemble()
        self.create_heirarchy()
    
    def init_design_data(self):
        self.column_dd = self.dd["supporting"]
        self.beam_dd = self.dd["supported"]
        self.angle_dd = self.dd["angle"]
        self.gap = self.dd["gap"]
    
    def init_location_data(self):
        self.column_ld = self.ld["column"]
        self.beam_ld = self.ld["beam"]
        self.angle_ld = self.ld["angle"]
        self.angleLeft_ld = self.ld["angleLeft"]
        self.bolts_and_nuts_ld = self.ld["bolts_and_nuts"]
    
    def create_and_assemble(self):
        self.create_column()
        self.create_beam()
        self.create_angle()
        self.create_angleLeft()
        self.create_nutBoltArray()
    
    def create_heirarchy(self):
        self.place_ifcelement_in_storey(self.ifccolumn, self.ground_storey)
        self.place_ifcelement_in_storey(self.ifcbeam, self.ground_storey)
        self.place_ifcelement_in_storey(self.ifcplate_angle, self.ground_storey)
        self.place_ifcelement_in_storey(self.ifcplate_angleLeft, self.ground_storey)

    def create_column(self):
        self.column = ISection(self.ifcfile, **self.column_dd)
        self.column_placement = self.place(location = self.column_ld)
        self.ifccolumn = self.column.create_ifccolumn("Column", self.column_placement)
    
    def create_beam(self):
        self.beam = ISection(self.ifcfile, **self.beam_dd)
        self.beam_placement = self.place(location = self.beam_ld)
        self.ifcbeam = self.beam.create_ifcbeam("Beam", self.beam_placement)

    def create_angle(self):
        self.angle = Angle(self.ifcfile, **self.angle_dd)
        self.angle_placement = self.place(location = self.angle_ld)
        self.ifcplate_angle = self.angle.create_angle_as_ifcplate("Angle", self.angle_placement)
    
    def create_angleLeft(self):
        self.angleLeft_placement = self.place(location = self.angleLeft_ld)
        self.ifcplate_angleLeft = self.angle.create_angle_as_ifcplate("Angle Left", self.angleLeft_placement)
    
    def create_nutBoltArray(self):
        for name, location in self.bolts_and_nuts_ld.items():
            fname = "DesignData/" + name + ".brep"
            shape = self.read_brep(fname)
            representation = ifcgeom.tesselate(self.ifcfile.schema, shape, 1.)
            self.ifcfile.add(representation)
            fastener = Fastener(self.ifcfile, representation)
            fastener_placement = self.place(location = location)
            self.ifcmechanicalfastener = fastener.create_ifcmechanicalfastener(name, fastener_placement)
            self.place_ifcelement_in_storey(self.ifcmechanicalfastener, self.ground_storey)

if __name__ == "__main__":
    CONFIG = {
        "filename": "CleatTestFinal.ifc",
    }
    design_data = json.load(open("DesignData/CleatColFlangeBeamWebConnectivity.json"))
    location_data = json.load(open("LocationData/CleatColFlangeBeamWebConnectivity.json"))
    CleatTest = CleatColFlangeBeamWebConnectivity(design_data, location_data, **CONFIG)
    CleatTest.write_ifcfile()