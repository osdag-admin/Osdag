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

        if KEY_FU in existingvalues:
            existingvalue_key_fu = existingvalues[KEY_FU]
        else:
            existingvalue_key_fu = ''

        if KEY_FY in existingvalues:
            existingvalue_key_fy = existingvalues[KEY_FY]
        else:
            existingvalue_key_fy = ''

        if KEY_VERSH in existingvalues:
            existingvalue_key_versh = existingvalues[KEY_VERSH]
        else:
            existingvalue_key_versh = ''

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

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)

        t2 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, existingvalue_key_conn, VALUES_CONN)
        options_list.append(t2)

        t3 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, existingvalue_key_suptngsec, VALUES_COLSEC)
        options_list.append(t3)

        t4 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, existingvalue_key_suptdsec, VALUES_BEAMSEC)
        options_list.append(t4)

        t5 = (KEY_FU, KEY_DISP_FU, TYPE_TEXTBOX, existingvalue_key_fu, None)
        options_list.append(t5)

        t6 = (KEY_FY, KEY_DISP_FY, TYPE_TEXTBOX, existingvalue_key_fy, None)
        options_list.append(t6)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None)
        options_list.append(t7)

        t8 = (KEY_VERSH, KEY_DISP_VERSH, TYPE_TEXTBOX, existingvalue_key_versh, None)
        options_list.append(t8)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, None)
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX, existingvalue_key_d, VALUES_D)
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, existingvalue_key_typ, VALUES_TYP)
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX, existingvalue_key_grd, VALUES_GRD)
        options_list.append(t12)

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, None)
        options_list.append(t13)

        t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX, existingvalue_key_platethk, VALUES_PLATETHK)
        options_list.append(t14)

        return options_list


    def input_value_changed():

        def fn_conn_suptngsec_lbl(v):

            if v in VALUES_CONN_1:
                return KEY_DISP_COLSEC
            elif v in VALUES_CONN_2:
                return KEY_DISP_PRIBM
            else:
                return ''

        def fn_conn_suptdsec_lbl(v):

            if v in VALUES_CONN_1:
                return KEY_DISP_BEAMSEC
            elif v in VALUES_CONN_2:
                return KEY_DISP_SECBM
            else:
                return ''

        def fn_conn_suptngsec(v):

            if v in VALUES_CONN_1:
                return VALUES_COLSEC
            elif v in VALUES_CONN_2:
                return VALUES_PRIBM
            else:
                return []

        def fn_conn_suptdsec(v):

            if v in VALUES_CONN_1:
                return VALUES_BEAMSEC
            elif v in VALUES_CONN_2:
                return VALUES_SECBM
            else:
                return []

        lst = []

        t1 = (KEY_CONN, KEY_SUPTNGSEC + "_label", TYPE_LABEL, fn_conn_suptngsec_lbl)
        lst.append(t1)

        t2 = (KEY_CONN, KEY_SUPTNGSEC, TYPE_COMBOBOX, fn_conn_suptngsec)
        lst.append(t2)

        t3 = (KEY_CONN, KEY_SUPTDSEC + "_label", TYPE_LABEL, fn_conn_suptdsec_lbl)
        lst.append(t3)

        t4 = (KEY_CONN, KEY_SUPTDSEC, TYPE_COMBOBOX, fn_conn_suptdsec)
        lst.append(t4)

        return lst



    def get_weld(self):
        return self.weld

    def set_weld(self, weld):
        self.weld = weld

    def set_weld_by_size(self, weld_size, length=0, material=Material()):
        self.weld = Weld(weld_size,length,material)


# fin_plate_input = FinPlateConnectionInput(connectivity, supporting_member_section, supported_member_section, material)


fin_plate_input = FinPlateConnection(connectivity, supporting_member_section, supported_member_section, fu, fy,
                                     shear_force, axial_force, bolt_diameter, bolt_type, bolt_grade,
                                     weld_size, plate_thickness)
bolt = Bolt(grade=bolt_grade, diameter=bolt_diameter, bolt_type=bolt_type, material=material)
load = Load(shear_force=shear_force)
plate = Plate(thickness=plate_thickness, material=material)
weld = Weld(size=weld_size, material=material)

fin_plate_input.bolt = bolt
fin_plate_input.load = load
fin_plate_input.plate = plate
fin_plate_input.weld = weld

print(fin_plate_input.bolt)

with open("filename", 'w') as out_file:
    yaml.dump(fin_plate_input, out_file)
