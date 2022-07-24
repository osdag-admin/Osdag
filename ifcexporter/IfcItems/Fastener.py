from ifcexporter.IfcItems.IfcInitializer import *

class Fastener(IfcObject):
    def __init__(self, ifcfile, name, placement = None, storey = None, **kwgs):
        super().__init__(ifcfile)
        self.ifcfile = ifcfile
        self.name = name
        self.product_rep = self.get_rep(name)
        if placement == None:
            self.placement = self.ifcfile.ground_storey_placement
        self.process_kwgs(kwgs)
        ifcobj = self.create_ifcobj()
        self.assign_storey(ifcobj, storey)
    
    def process_kwgs(self, kwgs):
        pass

    def create_ifcobj(self):
        params = {
            "GlobalId": self.guid(),
            "Name": self.name,
            "OwnerHistory": self.owner_history,
            "ObjectPlacement": self.placement,
            "Representation": self.product_rep
        }
        ifcobj = self.ifcfile.createIfcMechanicalFastener(**params)
        return ifcobj