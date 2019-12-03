from app.utils.common.material import Material
from app.design_type.connection.shear_connection import ShearConnection
from app.utils.common.component import Bolt, Plate, Weld, Angle
from app.utils.common.load import Load
import yaml

class SeatedAngleConnectionInput(ShearConnection):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load,
                 bolt_diameter, bolt_type, bolt_grade, seated_angle_section, top_angle_section):
        self.seated_angle = Angle(designation=seated_angle_section, material=self.material)
        self.top_angle = Angle(designation=top_angle_section, material=self.material)
        super(SeatedAngleConnectionInput, self).__init__(connectivity, supporting_member_section,
                                                         supported_member_section, fu, fy, shear_load,
                                                         bolt_diameter, bolt_type, bolt_grade)
