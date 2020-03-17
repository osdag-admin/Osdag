from Common import *
from utils.common.load import Load
from utils.common.component import *

class Main():

    def __init__(self):
        pass


    # def customized_input(self):
    #
    #     list1 = []
    #     t1 = (KEY_GRD, self.grdval_customized)
    #     list1.append(t1)
    #     t3 = (KEY_D, self.diam_bolt_customized)
    #     list1.append(t3)
    #     t6 = (KEY_PLATETHK, self.plate_thick_customized)
    #     list1.append(t6)
    #     # t8 = (KEY_SIZE, self.size_customized)
    #     # list1.append(t8)
    #     return list1

    @staticmethod
    def grdval_customized():
        b = VALUES_GRD_CUSTOMIZED
        return b

    @staticmethod
    def diam_bolt_customized():
        c = connectdb1()
        return c

    @staticmethod
    def plate_thick_customized():
        d = VALUES_PLATETHK_CUSTOMIZED
        return d

    #
    # @staticmethod
    # def size_customized():
    #     d = VALUES_SIZE_CUSTOMIZED
    #     return d

    # def input_value_changed(self):
    #     pass

    def set_input_values(self, design_dictionary):
        self.mainmodule = "Tension"
        # self.connectivity = design_dictionary[KEY_CONN]

        # if self.connectivity in VALUES_CONN_1:
        #     self.supporting_section = Column(designation=design_dictionary[KEY_SUPTNGSEC], material_grade=design_dictionary[KEY_MATERIAL])
        # else:
        #     self.supporting_section = Beam(designation=design_dictionary[KEY_SUPTNGSEC], material_grade=design_dictionary[KEY_MATERIAL])


        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                         bolt_type=design_dictionary[KEY_TYP],
                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                         material_grade=design_dictionary[KEY_MATERIAL],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         mu_f=design_dictionary.get(KEY_DP_BOLT_SLIP_FACTOR, None),
                         corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])


