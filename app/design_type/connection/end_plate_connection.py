from app.utils.common.material import Material
from app.design_type.connection.shear_connection import ShearConnection
from app.utils.common.component import Bolt, Plate, Weld, Angle
from app.utils.common.load import Load
import yaml


class EndPlateConnectionInput(ShearConnection):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load,
                 bolt_diameter, bolt_type, bolt_grade, weld_size, plate_thickness, plate_height=0.0, plate_width=0.0):
        self.plate = Plate(thickness=plate_thickness, height=plate_height, width=plate_width, material=self.material)
        self.weld = Weld(weld_size)
        self.weld_size_list = []
        super(EndPlateConnectionInput, self).__init__(connectivity, supporting_member_section, supported_member_section,
                                                      fu, fy, shear_load, bolt_diameter, bolt_type, bolt_grade)
