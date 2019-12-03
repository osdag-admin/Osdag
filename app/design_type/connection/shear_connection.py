from app.design_type.connection.connection import Connection
from app.utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column
from app.utils.common.load import Load
from app.utils.common.material import Material

class ShearConnection(Connection):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load, axial_load,
                 bolt_diameter, bolt_type, bolt_grade):
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
