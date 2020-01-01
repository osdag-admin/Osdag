from design_type.connection.connection import Connection
from utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column
from Common import *
from utils.common.load import Load

class ShearConnection(Connection):

    def __init__(self):
        super(ShearConnection, self).__init__()

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

    def fn_conn_suptngsec_lbl(self):

        if self in VALUES_CONN_1:
            return KEY_DISP_COLSEC
        elif self in VALUES_CONN_2:
            return KEY_DISP_PRIBM
        else:
            return ''

    def fn_conn_suptdsec_lbl(self):

        if self in VALUES_CONN_1:
            return KEY_DISP_BEAMSEC
        elif self in VALUES_CONN_2:
            return KEY_DISP_SECBM
        else:
            return ''

    def fn_conn_suptngsec(self):

        if self in VALUES_CONN_1:
            return VALUES_COLSEC
        elif self in VALUES_CONN_2:
            return VALUES_PRIBM
        else:
            return []

    def fn_conn_suptdsec(self):

        if self in VALUES_CONN_1:
            return VALUES_BEAMSEC
        elif self in VALUES_CONN_2:
            return VALUES_SECBM
        else:
            return []

    def fn_conn_image(self):
        if self == VALUES_CONN[0]:
            return './ResourceFiles/images/fin_cf_bw.png'
        elif self == VALUES_CONN[1]:
            return './ResourceFiles/images/fin_cw_bw.png'
        elif self in VALUES_CONN_2:
            return './ResourceFiles/images/fin_beam_beam.png'
        else:
            return ''

    def input_value_changed(self):

        lst = []

        t1 = (KEY_CONN, KEY_SUPTNGSEC, TYPE_LABEL, self.fn_conn_suptngsec_lbl)
        lst.append(t1)

        t2 = (KEY_CONN, KEY_SUPTNGSEC, TYPE_COMBOBOX, self.fn_conn_suptngsec)
        lst.append(t2)

        t3 = (KEY_CONN, KEY_SUPTDSEC, TYPE_LABEL, self.fn_conn_suptdsec_lbl)
        lst.append(t3)

        t4 = (KEY_CONN, KEY_SUPTDSEC, TYPE_COMBOBOX, self.fn_conn_suptdsec)
        lst.append(t4)

        t5 = (KEY_CONN, KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t5)

        return lst

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
        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None), material_grade=design_dictionary[KEY_MATERIAL])
        print(self.supported_section, self.supporting_section)