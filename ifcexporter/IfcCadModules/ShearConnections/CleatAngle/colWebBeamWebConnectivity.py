from ifcexporter.IfcItems.IfcInitializer import *
from ifcexporter.IfcItems.ISection import ISection
from ifcexporter.IfcItems.Plate import Plate
from ifcexporter.IfcItems.Fastener import Fastener

class CleatAngle_colWebBeamWebConnectivity(IfcObject):
    def __init__(self, **kwgs):
        super().__init__(**kwgs)
        ifc_class_name = self.__class__.__name__
        self.aux_data = json.load(open("ifcexporter/Temp/" + ifc_class_name + ".json"))
        self.create_models()
        self.clear_Temp()
    
    def create_models(self):
        self.create_column()
        self.create_beam()
        self.create_angle()
        self.create_angleLeft()
        self.create_fasteners()

    def create_column(self):
        ISection(self.ifcfile, 
            name = "column", 
            type = "column", 
            Pset_ProfileData = self.aux_data["Psets"]["ColumnProfileData"]
        )
    
    def create_beam(self):
        ISection(self.ifcfile, 
            name = "beam", 
            type = "beam", 
            Pset_ProfileData = self.aux_data["Psets"]["BeamProfileData"]
        )
    
    def create_angle(self):
        Plate(self.ifcfile, "angle")
    
    def create_angleLeft(self):
        Plate(self.ifcfile, "angleLeft")
    
    def create_fasteners(self):
        self.no_of_fasteners = self.aux_data.get("no_of_fasteners")
        for i in range(self.no_of_fasteners):
            Fastener(self.ifcfile, "fastener" + str(i))