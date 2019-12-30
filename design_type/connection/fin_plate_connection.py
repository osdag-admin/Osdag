from utils.common.material import Material
from design_type.connection.shear_connection import ShearConnection
from utils.common.component import Bolt, Plate, Weld
from Common import *
from utils.common.load import Load
import yaml
import os
import shutil
import logging
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap, QPalette
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog
import pickle

#from ...gui.newnew import Ui_Form
#newnew_object = Ui_Form()

connectivity = "column_flange_beam_web"
supporting_member_section = "HB 400"
supported_member_section = "MB 300"
fy = 250.0
fu = 410.0
shear_force = 100.0
axial_force=100.0
bolt_diameter = 24.0
bolt_type = "friction_grip"
bolt_grade = 8.8
plate_thickness = 10.0
weld_size = 6
material = Material(fy=fy, fu=fu)

logger = None


def module_setup():
    global logger
    logger = logging.getLogger("osdag.finPlateCalc")


module_setup()


class FinPlateConnection(ShearConnection):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load,axial_load,
                 bolt_diameter, bolt_type, bolt_grade, weld_size, plate_thickness, plate_height=0.0, plate_width=0.0):
        super(FinPlateConnection, self).__init__(connectivity, supporting_member_section, supported_member_section,
                                                      fu, fy, shear_load, axial_load, bolt_diameter, bolt_type, bolt_grade)

        self.weld = Weld(weld_size)
        self.weld_size_list = []
        self.plate = Plate(thickness=plate_thickness, height=plate_height, width=plate_width, material=self.material)


    def input_values(self, existingvalues={}):

        options_list = []

        if KEY_CONN in existingvalues:
            existingvalue_key_conn = existingvalues[KEY_CONN]
        else:
            existingvalue_key_conn = ''

        if KEY_SUPTNGSEC in existingvalues:
           existingvalue_key_suptngsec = existingvalues[KEY_SUPTNGSEC]
        else:
            existingvalue_key_suptngsec = ''

        if KEY_SUPTDSEC in existingvalues:
            existingvalue_key_suptdsec = existingvalues[KEY_SUPTDSEC]
        else:
            existingvalue_key_suptdsec = ''

        if KEY_MATERIAL in existingvalues:
            existingvalue_key_mtrl = existingvalues[KEY_MATERIAL]
        else:
            existingvalue_key_mtrl = ''

        if KEY_VERSH in existingvalues:
            existingvalue_key_versh = existingvalues[KEY_VERSH]
        else:
            existingvalue_key_versh = ''

        if KEY_AXIAL in existingvalues:
            existingvalue_key_axial = existingvalues[KEY_AXIAL]
        else:
            existingvalue_key_axial = ''

        if KEY_D in existingvalues:
            existingvalue_key_d = existingvalues[KEY_D]
        else:
            existingvalue_key_d = ''

        if KEY_TYP in existingvalues:
            existingvalue_key_typ = existingvalues[KEY_TYP]
        else:
            existingvalue_key_typ = ''

        if KEY_GRD in existingvalues:
            existingvalue_key_grd = existingvalues[KEY_GRD]
        else:
            existingvalue_key_grd = ''

        if KEY_PLATETHK in existingvalues:
            existingvalue_key_platethk = existingvalues[KEY_PLATETHK]
        else:
            existingvalue_key_platethk = ''

        t16 = (KEY_MODULE, KEY_DISP_FINPLATE, TYPE_MODULE, None, None)
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)

        t2 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, existingvalue_key_conn, VALUES_CONN)
        options_list.append(t2)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
        options_list.append(t15)

        t3 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, existingvalue_key_suptngsec, VALUES_COLSEC)
        options_list.append(t3)

        t4 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, existingvalue_key_suptdsec, VALUES_BEAMSEC)
        options_list.append(t4)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL)
        options_list.append(t5)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None)
        options_list.append(t6)

        t7 = (KEY_VERSH, KEY_DISP_VERSH, TYPE_TEXTBOX, existingvalue_key_versh, None)
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, existingvalue_key_axial, None)
        options_list.append(t8)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, None)
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_d, VALUES_D)
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, existingvalue_key_typ, VALUES_TYP)
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_grd, VALUES_GRD)
        options_list.append(t12)

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, None)
        options_list.append(t13)

        t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_platethk, VALUES_PLATETHK)
        options_list.append(t14)

        return options_list

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
            return''

    def input_value_changed(self):

        lst = []

        t1 = (KEY_CONN, KEY_SUPTNGSEC , TYPE_LABEL,self.fn_conn_suptngsec_lbl)
        lst.append(t1)

        t2 = (KEY_CONN, KEY_SUPTNGSEC, TYPE_COMBOBOX, self.fn_conn_suptngsec)
        lst.append(t2)

        t3 = (KEY_CONN, KEY_SUPTDSEC , TYPE_LABEL, self.fn_conn_suptdsec_lbl)
        lst.append(t3)

        t4 = (KEY_CONN, KEY_SUPTDSEC, TYPE_COMBOBOX, self.fn_conn_suptdsec)
        lst.append(t4)

        t5 = (KEY_CONN, KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t5)

        return lst

    def to_get_d(self, my_d):
        # self.set_connectivity(self, my_d[KEY_CONN])
        # self.set_supporting_section(self,my_d[KEY_SUPTNGSEC])
        # self.set_supported_section(self,my_d[KEY_SUPTDSEC])
        # self.set_material(self,my_d[KEY_MATERIAL])
        # self.set_shear(self, my_d[KEY_SHEAR])
        # self.set_axial(self,my_d[KEY_AXIAL])
        # self.set_bolt_dia(self,my_d[KEY_D])
        # self.set_bolt_type(self,my_d[KEY_TYP])
        # self.set_bolt_grade(self,my_d[KEY_GRD])
        # self.set_plate_thk(self,my_d[KEY_PLATETHK])
        # self.weld = Weld(weld_size)
        # self.weld_size_list = []
        self.connectivity = my_d[KEY_CONN]

        if self.connectivity in VALUES_CONN_1:
            self.supporting_section = Column(designation=my_d[KEY_SUPTNGSEC], material_grade=my_d[KEY_MATERIAL])
        else:
            self.supporting_section = Beam(designation=my_d[KEY_SUPTNGSEC], material_grade=my_d[KEY_MATERIAL])

        self.supported_section = Beam(designation=my_d[KEY_SUPTNGSEC], material_grade=my_d[KEY_MATERIAL])
        self.bolt = Bolt(grade=my_d[KEY_GRD], diameter=my_d[KEY_D], bolt_type=my_d[KEY_TYP],
                         material_grade=material_grade)
        self.load = Load(shear_force=my_d[KEY_SHEAR], axial_force=my_d[KEY_AXIAL])
        self.plate = Plate(thickness=my_d[KEY_PLATETHK], material_grade=my_d[KEY_MATERIAL])

    # def set_axial(self, axial):
    #     self.axial = axial
    #
    # def set_plate_thk(self, plate_thk):
    #     self.plate_thk = plate_thk
    #
    # def set_supporting_section(self, supporting_section):
    #     self.supporting_section = supporting_section
    #
    # def set_supported_section(self, supported_section):
    #     self.supported_section = supported_section
    #
    # def set_material(self, material=Material(material_grade)):
    #     self.material = Material(material)
    #     print(self.material)
    #
    # def set_weld_by_size(self, weld_size, length=0, material=Material(material_grade)):
    #     self.weld = Weld(weld_size,length,material)
    #
    # def get_shear_capacity(self):
    #     shear_capacity = self.shear

    # fin_plate_input = FinPlateConnectionInput(connectivity, supporting_member_section, supported_member_section, material)

fin_plate_input = FinPlateConnection(self.connectivity, supporting_member_section, supported_member_section, fu, fy,
                                     shear_force, axial_force, bolt_diameter, bolt_type, bolt_grade,
                                     weld_size, plate_thickness)
bolt = Bolt(grade=bolt_grade, diameter=bolt_diameter, bolt_type=bolt_type, material_grade=material_grade)
load = Load(shear_force=shear_force)
plate = Plate(thickness=plate_thickness, material_grade=material_grade)
weld = Weld(size=weld_size, material_grade=material_grade)
fin_plate_input.bolt = bolt
fin_plate_input.load = load
fin_plate_input.plate = plate
fin_plate_input.weld = weld

print(fin_plate_input.bolt)

with open("filename", 'w') as out_file:
    yaml.dump(fin_plate_input, out_file)


# print(fin_plate_input.bolt)

with open("filename", 'w') as out_file:
    yaml.dump(fin_plate_input, out_file)
