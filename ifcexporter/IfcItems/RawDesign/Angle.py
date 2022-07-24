from IfcInitializer import IfcObject

class Angle(IfcObject):
    def __init__(self, ifcfile, **kwgs):
        super().__init__(ifcfile)
        self.process_kwgs(kwgs)
        self.construct_profile()
        self.extrude_body()
        self.product_rep = self.create_product_representation(self.extruded_body)

    def process_kwgs(self, kwgs):
        self.height = kwgs.get("L")
        pc = kwgs.get("profile_coords")
        pc.append(pc[0])
        self.profile_coords = pc

    def construct_profile(self):
        self.profile_placement = self.ifcfile.createIfcAxis2Placement2D(self.ori, self.Xdir)
        self.profile = self.create_ifcarbitraryclosedprofiledef(self.profile_coords)
    
    def extrude_body(self):
        self.extruded_body = self.ifcfile.createIfcExtrudedAreaSolid(self.profile, self.g_placement, self.Zdir, self.height)
    
    def create_angle_as_ifcplate(self, name, placement):
        params = {
            "GlobalId": self.guid(),
            "Name": name,
            "OwnerHistory": self.owner_history,
            "ObjectPlacement": placement,
            "Representation": self.product_rep
        }
        ifcplate = self.ifcfile.createIfcPlate(**params)
        return ifcplate