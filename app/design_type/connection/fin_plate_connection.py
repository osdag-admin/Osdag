from app.utils.common.material import Material
from app.design_type.connection.shear_connection import ShearConnection
from app.utils.common.component import Bolt, Plate, Weld
from app.utils.common.load import Load
import yaml
import pickle

connectivity = "column_flange_beam_web"
supporting_member_section = "HB 400"
supported_member_section = "MB 300"
fy = 250.0
fu = 410.0
shear_force = 100.0
bolt_diameter = 24.0
bolt_type = "friction_grip"
bolt_grade = 8.8
plate_thickness = 10.0
weld_size = 6
material = Material(fy=fy, fu=fu)


class FinPlateConnection(ShearConnection):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load,
                 bolt_diameter, bolt_type, bolt_grade, weld_size, plate_thickness, plate_height=0.0, plate_width=0.0):
        super(FinPlateConnection, self).__init__(connectivity, supporting_member_section, supported_member_section,
                                                      fu, fy, shear_load, bolt_diameter, bolt_type, bolt_grade)

        self.weld = Weld(weld_size)
        self.weld_size_list = []
        self.plate = Plate(thickness=plate_thickness, height=plate_height, width=plate_width, material=self.material)

# fin_plate_input = FinPlateConnectionInput(connectivity, supporting_member_section, supported_member_section, material)


fin_plate_input = FinPlateConnection(connectivity, supporting_member_section, supported_member_section, fu, fy, shear_force,
                 bolt_diameter, bolt_type, bolt_grade, weld_size, plate_thickness)
bolt = Bolt(grade=bolt_grade, diameter=bolt_diameter, bolt_type=bolt_type, material=material)
load = Load(shear_force=shear_force)
plate = Plate(thickness=plate_thickness, material=material)
weld = Weld(size=weld_size, material=material)

fin_plate_input.bolt = bolt
fin_plate_input.load = load
fin_plate_input.plate = plate
fin_plate_input.weld = weld

print(fin_plate_input.bolt)

with open("filename", 'w') as out_file:
    yaml.dump(fin_plate_input, out_file)
