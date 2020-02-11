from Common import *

class Main():

    def __init__(self):
        pass

    def customized_input(self):

        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)
        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)
        t6 = (KEY_ENDPLATE_THICKNESS, self.endplate_thick_customized)
        list1.append(t6)
        return list1

    @staticmethod
    def grdval_customized():
        b = VALUES_GRD_CUSTOMIZED
        return b

    @staticmethod
    def diam_bolt_customized():
        c = connectdb1()
        return c

    @staticmethod
    def endplate_thick_customized():
        d = VALUES_ENDPLATE_THICKNESS_CUSTOMIZED
        return d

    def input_value_changed(self):
        pass
