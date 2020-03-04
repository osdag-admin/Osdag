from app.utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column
from app.utils.common.load import Load
from app.utils.common.material import Material


class Main(object):
    pass


class ConnectionInput(Main):
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


class FinPlateConnectionInput(ShearConnectionInput):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load,
                 bolt_diameter, bolt_type, bolt_grade, weld_size, plate_thickness, plate_height=0.0, plate_width=0.0):
        self.plate = Plate(thickness=plate_thickness, height=plate_height, width=plate_width, material=self.material)
        self.weld = Weld(weld_size)
        self.weld_size_list = []
        super(FinPlateConnectionInput, self).__init__(connectivity, supporting_member_section, supported_member_section,
                                                      fu, fy, shear_load, bolt_diameter, bolt_type, bolt_grade)


class EndPlateConnectionInput(ShearConnectionInput):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load,
                 bolt_diameter, bolt_type, bolt_grade, weld_size, plate_thickness, plate_height=0.0, plate_width=0.0):
        self.plate = Plate(thickness=plate_thickness, height=plate_height, width=plate_width, material=self.material)
        self.weld = Weld(weld_size)
        self.weld_size_list = []
        super(EndPlateConnectionInput, self).__init__(connectivity, supporting_member_section, supported_member_section,
                                                      fu, fy, shear_load, bolt_diameter, bolt_type, bolt_grade)


class CleatAngleConnectionInput(ShearConnectionInput):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load,
                 bolt_diameter, bolt_type, bolt_grade, cleat_angle_section):
        self.cleat_angle = Angle(designation=cleat_angle_section, material=self.material)
        super(CleatAngleConnectionInput, self).__init__(connectivity, supporting_member_section,
                                                        supported_member_section, fu, fy, shear_load, bolt_diameter,
                                                        bolt_type, bolt_grade)


class SeatedAngleConnectionInput(ShearConnectionInput):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load,
                 bolt_diameter, bolt_type, bolt_grade, seated_angle_section, top_angle_section):
        self.seated_angle = Angle(designation=seated_angle_section, material=self.material)
        self.top_angle = Angle(designation=top_angle_section, material=self.material)
        super(SeatedAngleConnectionInput, self).__init__(connectivity, supporting_member_section,
                                                         supported_member_section, fu, fy, shear_load,
                                                         bolt_diameter, bolt_type, bolt_grade)
