from design_type.connection.connection import Connection
from utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column
from Common import *
from utils.common.load import Load

class ShearConnection(Connection):

    def __init__(self):
        super(ShearConnection, self).__init__()

    def set_input_values(self, design_dictionary):
        self.connectivity = design_dictionary[KEY_CONN]

        if self.connectivity in VALUES_CONN_1:
            self.supporting_section = Column(designation=design_dictionary[KEY_SUPTNGSEC], material_grade=design_dictionary[KEY_MATERIAL])
        else:
            self.supporting_section = Beam(designation=design_dictionary[KEY_SUPTNGSEC], material_grade=design_dictionary[KEY_MATERIAL])

        self.supported_section = Beam(designation=design_dictionary[KEY_SUPTDSEC], material_grade=design_dictionary[KEY_MATERIAL])
        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D], bolt_type=design_dictionary[KEY_TYP],
                         material_grade=design_dictionary[KEY_MATERIAL])
        self.load = Load(shear_force=design_dictionary[KEY_SHEAR], axial_force=design_dictionary.get(KEY_AXIAL, None))
        self.plate = Plate(thickness=design_dictionary[KEY_PLATETHK], material_grade=design_dictionary[KEY_MATERIAL])
