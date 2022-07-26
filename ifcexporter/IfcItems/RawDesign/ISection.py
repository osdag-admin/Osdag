from IfcInitializer import IfcObject

class ISection(IfcObject):
    def __init__(self, ifcfile, **kwgs):
        super().__init__(ifcfile)
        self.process_kwgs(kwgs)
        self.construct_profile()
        self.extrude_body()
        self.product_rep = self.create_product_representation(self.extruded_body)

    def process_kwgs(self, kwgs):
        self.length = kwgs.pop("length")
        self.profile_data = dict(
            OverallWidth = kwgs.get("B"),
            OverallDepth = kwgs.get("D"),
            WebThickness = kwgs.get("t"),
            FlangeThickness = kwgs.get("T"), 
            FilletRadius = None
        )

    def construct_profile(self):
        self.profile_placement = self.ifcfile.createIfcAxis2Placement2D(self.ori, self.Xdir)
        self.profile = self.ifcfile.createIfcIShapeProfileDef("AREA", "IShapedProfile", self.profile_placement, **self.profile_data)
    
    def extrude_body(self):
        self.extruded_body = self.ifcfile.createIfcExtrudedAreaSolid(self.profile, self.g_placement, self.Zdir, self.length)
    
    def create_ifccolumn(self, name, placement):
        params = {
            "GlobalId": self.guid(),
            "Name": name,
            "OwnerHistory": self.owner_history,
            "ObjectPlacement": placement,
            "Representation": self.product_rep
        }
        ifccolumn = self.ifcfile.createIfcColumn(**params)
        return ifccolumn
    
    def create_ifcbeam(self, name, placement):
        params = {
            "GlobalId": self.guid(),
            "Name": name,
            "OwnerHistory": self.owner_history,
            "ObjectPlacement": placement,
            "Representation": self.product_rep
        }
        ifcbeam = self.ifcfile.createIfcBeam(**params)
        return ifcbeam