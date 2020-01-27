from design_type.connection.shear_connection import ShearConnection
from design_type.connection.fin_plate_connection import FinPlateConnection
from design_type.connection.end_plate_connection import EndPlateConnectionInput
from design_type.connection.cleat_angle_connection import CleatAngleConnectionInput
import yaml
from utils.common.component import Bolt, Plate, Weld
from Common import *


def set_osdaglogger(key):
    global logger
    logger = logging.getLogger('osdag')

    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler = logging.FileHandler('logging_text.log')

    handler.setLevel(logging.WARNING)
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler = OurLog(key)
    handler.setLevel(logging.WARNING)
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def set_input_values(self, design_dictionary, signal):
    if signal:
        super(FinPlateConnection, self).set_input_values(design_dictionary)
    else:
        super(FinPlateConnection, self).set_input_values(design_dictionary)
    self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None),
                       material_grade=design_dictionary[KEY_MATERIAL], gap=design_dictionary[KEY_DP_DETAILING_GAP])
    print("input values are set. Doing preliminary member checks")
    member_capacity(self)


def member_capacity(self):
    # print(KEY_CONN,VALUES_CONN_1,self.supported_section.build)
    if self.connectivity in VALUES_CONN_1:
        if self.supported_section.build == "Rolled":
            length = self.supported_section.depth
        else:
            length = self.supported_section.depth - (2*self.supported_section.flange_thickness)    # -(2*self.supported_section.root_radius)
    else:
        length = self.supported_section.depth - 50.0  # TODO: Subtract notch height for beam-beam connection

    self.supported_section.shear_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)
    self.supported_section.tension_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)

    print(self.supported_section.shear_yielding_capacity, self.load.shear_force,
          self.supported_section.tension_yielding_capacity, self.load.axial_force)

    if self.supported_section.shear_yielding_capacity > self.load.shear_force and \
            self.supported_section.tension_yielding_capacity > self.load.axial_force:
        print("preliminary member check is satisfactory. Doing bolt checks")
        self.get_bolt_details()
    else:
        logger.error(" : shear yielding capacity {} and/or tension yielding capacity {} is less "
                       "than applied loads, Please select larger sections or decrease loads"
                        .format(self.supported_section.shear_yielding_capacity,
                                self.supported_section.tension_yielding_capacity))
        print("failed in preliminary member checks. Select larger sections or decrease loads")


print("Select a module number:")
print("1. FinPlate")
print("2. EndPlate")
module = int(input("Enter module number: "))

path = input("Enter the file location: ")
with open(path, 'r') as f:
    d = yaml.load(f)
#set_input_values(FinPlateConnection(), d, False)
#set_input_values(EndPlateConnectionInput(), d, False)
if module == 1:
    set_input_values(FinPlateConnection(), d, False)
else:
    set_input_values(EndPlateConnectionInput(EndPlateConnectionInput,'','','','','','','','','',''), d, False)




