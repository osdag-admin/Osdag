from app.utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column
from app.utils.common.load import Load
from app.utils.common.material import Material


class Input(object):
    pass


class ConnectionInput(Input):
    pass


class ShearConnectionInput(ConnectionInput):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load,
                 bolt_diameter, bolt_type, bolt_grade):
        self.connectivity = connectivity
        if connectivity == "column_flange_beam_web" or "column_web_beam_web":
            self.supporting_member = Column(supporting_member_section, self.material)
        elif connectivity == "beam_beam":
            self.supporting_member = Beam(supporting_member_section, self.material)
        self.supported_member = Beam(supported_member_section, self.material)
        self.material = Material(fy=fy, fu=fu)
        self.shear_load = Load(shear_force=shear_load)
        self.bolt = Bolt(diameter=bolt_diameter, grade=bolt_grade, bolt_type=bolt_type)
        self.bolt_diameter_list = []
        self.weld = Weld()
        self.weld_size_list = []


class FinPlateConnectionInput(ShearConnectionInput):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load,
                 bolt_diameter, bolt_type, bolt_grade):
        self.plate = Plate()
        super(FinPlateConnectionInput, self).__init__(connectivity, supporting_member_section, supported_member_section,
                                                      fu, fy, shear_load, bolt_diameter, bolt_type, bolt_grade)


class EndPlateConnectionInput(ShearConnectionInput):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load,
                 bolt_diameter, bolt_type, bolt_grade):
        self.plate = Plate()
        super(EndPlateConnectionInput, self).__init__(connectivity, supporting_member_section, supported_member_section,
                                                      fu, fy, shear_load, bolt_diameter, bolt_type, bolt_grade)


class CleatAngleConnectionInput(ShearConnectionInput):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load,
                 bolt_diameter, bolt_type, bolt_grade):
        self.cleat_angle = Angle()
        super(CleatAngleConnectionInput, self).__init__(connectivity, supporting_member_section,
                                                        supported_member_section, fu, fy, shear_load, bolt_diameter,
                                                        bolt_type, bolt_grade)


class SeatedAngleConnectionInput(ShearConnectionInput):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load,
                 bolt_diameter, bolt_type, bolt_grade):
        self.seated_angle = Angle()
        self.top_angle = Angle()
        super(SeatedAngleConnectionInput, self).__init__(connectivity, supporting_member_section,
                                                         supported_member_section, fu, fy, shear_load,
                                                         bolt_diameter, bolt_type, bolt_grade)
