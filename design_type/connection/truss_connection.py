from design_type.connection.connection import Connection
from utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column, ISection
from utils.common.Section_Properties_Calculator import Single_Angle_Properties
from Common import *
from utils.common.load import Load
from utils.common.material import Material
from utils.common.common_calculation import *
from utils.common.is800_2007 import IS800_2007


class TrussConnection(Connection):
    def __init__(self):
        super(TrussConnection, self).__init__()

    ############################
    # Design Preferences functions
    ############################

    @staticmethod
    def pltthk_customized():
        a = VALUES_PLATETHK_CUSTOMIZED
        return a

    @staticmethod
    def grdval_customized():
        b = VALUES_GRD_CUSTOMIZED
        return b

    @staticmethod
    def diam_bolt_customized():
        c = connectdb1()
        return c

    def customized_input(self):
        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)
        t2 = (KEY_PLATETHK, self.pltthk_customized)
        list1.append(t2)
        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)
        return list1

    def input_value_changed(self):

        lst = []
        return lst
