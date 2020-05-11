from design_type.connection.shear_connection import ShearConnection
from design_type.connection.fin_plate_connection import FinPlateConnection
import yaml
from utils.common.component import Bolt, Plate, Weld
from Common import *
import os

path = r'.\ResourceFiles\design_example'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.osi' in file:
            files.append(os.path.join(r, file))

for f in files:
    print(f)
    with open(f, 'r') as input_file:
        d = yaml.load(input_file, Loader=yaml.FullLoader)

    module = d['Module']
    if module == 'Fin Plate':
        main = FinPlateConnection
        main.set_osdaglogger(None)
        main.set_input_values(main, d)
        base = os.path.basename(f)
        filename = str(os.path.splitext(base)[0])+".txt"
        main.results_to_test(main, os.path.basename(filename))
    # elif module == 'Column Coverplate Connection':
    #     self = ColumnCoverPlate
    #     self.set_osdaglogger()
    #     self.set_input_values(self, d)




