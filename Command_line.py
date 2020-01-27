from design_type.connection.shear_connection import ShearConnection
from design_type_command_prompt.connection.fin_plate_connection import FinPlateConnection
from design_type_command_prompt.connection.column_cover_plate import ColumnCoverPlate
from design_type_command_prompt.connection.end_plate_connection import EndPlateConnectionInput
from design_type.connection.cleat_angle_connection import CleatAngleConnectionInput
import yaml
from utils.common.component import Bolt, Plate, Weld
from Common import *
import os

path = r'./ResourceFiles/Osi_Files'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.osi' in file:
            files.append(os.path.join(r, file))

for f in files:
    print(f)
    with open(f, 'r') as f:
        d = yaml.load(f, Loader=yaml.FullLoader)

    module = d['Module']
    if module == 'Fin Plate':
        self = FinPlateConnection
        self.set_osdaglogger()
        self.set_input_values(self, d)
    elif module == 'Column Coverplate Connection':
        self = ColumnCoverPlate
        self.set_osdaglogger()
        self.set_input_values(self, d)




