from app.utils.common.material import Material
from app.utils.common.input import FinPlateConnectionInput
from app.utils.common.component import Bolt, Plate, Weld
from app.utils.common.load import Load


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
fin_plate_input = FinPlateConnectionInput(connectivity, supporting_member_section, supported_member_section, material)

bolt = Bolt(grade=bolt_grade, diameter=bolt_diameter, bolt_type=bolt_type, material=material)
load = Load(shear_force=shear_force)
plate = Plate(thickness=plate_thickness, material=material)
weld = Weld(size=weld_size, material=material)

fin_plate_input.bolt = bolt
fin_plate_input.load = load
fin_plate_input.plate = plate
fin_plate_input.weld = weld

print(fin_plate_input.load)

