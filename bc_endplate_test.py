import yaml
from design_type.connection.beam_column_end_plate import BeamColumnEndPlate
from utils.common.component import *
from utils.common.load import Load



# Load osi file
# Get input objects
# '''
input_file_path = 'bcinput1.osi'
with open(input_file_path, 'r') as input_file:
        design_dictionary  = yaml.load(input_file, Loader=yaml.FullLoader)

# print(design_dictionary)

bcinput = BeamColumnEndPlate()
bcinput.set_input_values(design_dictionary)


'''
# Hardcoded inputs
bcinput = BeamColumnEndPlate()

bcinput.mainmodule = "Moment Connection"
bcinput.connectivity = 'Column flange-Beam web'
bcinput.material = Material(material_grade='E 250 (Fe 410 W)A')

bcinput.supporting_section = Column(designation='HB 400',
                                     material_grade='E 250 (Fe 410 W)A')

bcinput.supported_section = Beam(designation='MB 350',
                              material_grade='E 250 (Fe 410 W)A')
bcinput.bolt = Bolt(grade=[4.6, 8.8], diameter=[12, 20],
                 bolt_type='Friction Grip Bolt',
                 bolt_hole_type='Standard',
                 edge_type='a - Sheared or hand flame cut',
                 mu_f=0.3,
                 corrosive_influences='No',
                 bolt_tensioning='Pretensioned')

bcinput.load = Load(shear_force=40,
                 axial_force=10, moment=50)

bcinput.plate = Plate(thickness=[12, 220],
                   material_grade='E 250 (Fe 410 W)A',
                   gap=10)
bcinput.plate.design_status_capacity = False
bcinput.weld = Weld(material_g_o=410,
                 fabrication='Shop Weld')

'''
print("input values are set. Doing preliminary member checks")
bcinput.warn_text()
# bcinput.member_capacity()
print(bcinput.endplate_type)
bcinput.trial_design()

