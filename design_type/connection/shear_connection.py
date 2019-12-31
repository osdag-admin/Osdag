from design_type.connection.connection import Connection
from utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column
from utils.common.load import Load
from utils.common.material import Material

class ShearConnection(Connection):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load, axial_load,
                 bolt_diameter, bolt_type, bolt_grade):
        super(ShearConnection, self).__init__(fu, fy)
        self.connectivity = connectivity
        # self.material = Material(fy=fy, fu=fu)
        if connectivity == "column_flange_beam_web" or "column_web_beam_web":
            self.supporting_member = Column(supporting_member_section, self.material)
        elif connectivity == "beam_beam":
            self.supporting_member = Beam(supporting_member_section, self.material)
        self.supported_member = Beam(supported_member_section, self.material)
        self.load = Load(shear_force=shear_load, axial_force=axial_load)
        self.bolt = Bolt(diameter=bolt_diameter, grade=bolt_grade, bolt_type=bolt_type)
        self.bolt_diameter_list = []

    def get_connectivity(self):
        return self.connectivity

    def set_connectivity(self,connectivity):
        self.connectivity = connectivity

    def get_supporting_member_section(self):
        return self.supporting_member

    def set_supporting_member_section(self,connectivity,supporting_member_section):
        if self.connectivity == "column_flange_beam_web" or "column_web_beam_web":
            self.supporting_member = Column(supporting_member_section, self.material)
        elif connectivity == "beam_beam":
            self.supporting_member = Beam(supporting_member_section, self.material)
    # 
    # def get_supported_member_section(self):
    #     pass