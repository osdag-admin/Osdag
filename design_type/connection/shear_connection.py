from design_type.connection.connection import Connection
from utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column
from Common import *
from utils.common.load import Load

class ShearConnection(Connection):

# <<<<<<< HEAD
#     def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load, axial_load,
#                  bolt_diameter, bolt_type, bolt_grade):
#         super(ShearConnection, self).__init__(fu, fy)
#         self.connectivity = connectivity
#         # self.material = Material(fy=fy, fu=fu)
#         if connectivity == "column_flange_beam_web" or "column_web_beam_web":
#             self.supporting_member = Column(supporting_member_section, self.material)
#         elif connectivity == "beam_beam":
#             self.supporting_member = Beam(supporting_member_section, self.material)
#         self.supported_member = Beam(supported_member_section, self.material)
#         self.load = Load(shear_force=shear_load, axial_force=axial_load)
#         self.bolt = Bolt(diameter=bolt_diameter, grade=bolt_grade, bolt_type=bolt_type)
#         self.bolt_diameter_list = []
#
#     def get_connectivity(self):
#         return self.connectivity
#
#     def set_connectivity(self,connectivity):
#         self.connectivity = connectivity
#
#     def get_supporting_member_section(self):
#         return self.supporting_member
#
#     def set_supporting_member_section(self,connectivity,supporting_member_section):
#         if self.connectivity == "column_flange_beam_web" or "column_web_beam_web":
#             self.supporting_member = Column(supporting_member_section, self.material)
#         elif connectivity == "beam_beam":
#             self.supporting_member = Beam(supporting_member_section, self.material)
#     #
#     # def get_supported_member_section(self):
#     #     pass
# =======
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
            return connectdb("Columns")
        elif self in VALUES_CONN_2:
            return connectdb("Beams")
        else:
            return []

    def fn_conn_suptdsec(self):

        if self in VALUES_CONN:
            return connectdb("Beams")
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

        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                         bolt_type=design_dictionary[KEY_TYP],
                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                         material_grade=design_dictionary[KEY_MATERIAL],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         mu_f=design_dictionary.get(KEY_DP_BOLT_SLIP_FACTOR, None),
                         corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])

        self.load = Load(shear_force=design_dictionary[KEY_SHEAR], axial_force=design_dictionary.get(KEY_AXIAL, None))



