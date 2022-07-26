from ifcexporter.IfcItems.IfcInitializer import *

class ISection(IfcObject):
    def __init__(self, ifcfile, name, placement = None, storey = None, type = "column", **kwgs):
        super().__init__(ifcfile)
        self.name = name
        self.product_rep = self.get_rep(name)
        if placement == None:
            self.placement = self.ifcfile.ground_storey_placement
        self.type = type
        self.process_kwgs(kwgs)
        ifcobj = self.create_ifcobj()
        self.assign_Pset(ifcobj, "Pset_ProfileData", self.Pset_ProfileData)
        self.assign_storey(ifcobj, storey)
    
    def process_kwgs(self, kwgs):
        self.Pset_ProfileData = kwgs.get("Pset_ProfileData")

    def create_ifcobj(self):
        params = {
            "GlobalId": self.guid(),
            "Name": self.name,
            "OwnerHistory": self.owner_history,
            "ObjectPlacement": self.placement,
            "Representation": self.product_rep
        }
        if self.type == "column":
            ifcobj = self.ifcfile.createIfcColumn(**params)
        else:
            ifcobj = self.ifcfile.createIfcBeam(**params)
        return ifcobj