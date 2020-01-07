from design_type.connection.moment_connection import MomentConnection
from utils.common.component import *
from Common import *
from utils.common.load import Load
import yaml
import os
import shutil
import logging

class ColumnCoverPlate(MomentConnection):

    def __init__(self):
        super(ColumnCoverPlate, self).__init__()


    def input_values(self, existingvalues={}):

        options_list = []

        if KEY_CONN in existingvalues:
            existingvalue_key_conn = existingvalues[KEY_CONN]
        else:
            existingvalue_key_conn = ''

        if KEY_SECSIZE in existingvalues:
            existingvalue_key_secsize = existingvalues[KEY_SECSIZE]
        else:
            existingvalue_key_secsize = ''

        if KEY_MATERIAL in existingvalues:
            existingvalue_key_mtrl = existingvalues[KEY_MATERIAL]
        else:
            existingvalue_key_mtrl = ''

        if KEY_MOMENT in existingvalues:
            existingvalues_key_moment = existingvalues[KEY_MOMENT]
        else:
            existingvalues_key_moment = ''

        if KEY_SHEAR in existingvalues:
            existingvalue_key_versh = existingvalues[KEY_SHEAR]
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

        if KEY_FLANGEPLATE_PREFERENCES in existingvalues:
            existingvalue_key_fplate_pref = existingvalues[KEY_PLATETHK]
        else:
            existingvalue_key_fplate_pref = ''

        if KEY_FLANGEPLATE_THICKNESS in existingvalues:
            existingvalue_key_fplate_thk = existingvalues[KEY_PLATETHK]
        else:
            existingvalue_key_fplate_thk = ''

        if KEY_WEBPLATE_THICKNESS in existingvalues:
            existingvalue_key_wplate_thk = existingvalues[KEY_PLATETHK]
        else:
            existingvalue_key_wplate_thk = ''

        t16 = (KEY_MODULE, KEY_DISP_COLUMNCOVERPLATE, TYPE_MODULE, None, None)
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX, existingvalue_key_secsize, connectdb("Columns"))
        options_list.append(t4)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
        options_list.append(t15)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL)
        options_list.append(t5)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None)
        options_list.append(t6)

        t17 = (KEY_MOMENT, KEY_DISP_MOMENT, TYPE_TEXTBOX,existingvalues_key_moment,None)
        options_list.append(t17)

        t7 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, existingvalue_key_versh, None)
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

        t18 = (None, DISP_TITLE_FLANGESPLICEPLATE, TYPE_TITLE, None, None)
        options_list.append(t18)

        t19 = (KEY_FLANGEPLATE_PREFERENCES, KEY_DISP_FLANGESPLATE_PREFERENCES, TYPE_COMBOBOX, existingvalue_key_fplate_pref, VALUES_FLANGEPLATE_PREFERENCES)
        options_list.append(t19)

        t20 = (KEY_FLANGEPLATE_THICKNESS, KEY_DISP_FLANGESPLATE_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_fplate_thk, VALUES_FLANGEPLATE_THICKNESS)
        options_list.append(t20)

        t21 = (None, DISP_TITLE_WEBSPLICEPLATE, TYPE_TITLE, None, None)
        options_list.append(t21)

        t22 = (KEY_WEBPLATE_THICKNESS, KEY_DISP_WEBPLATE_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_wplate_thk, VALUES_WEBPLATE_THICKNESS)
        options_list.append(t22)


        # t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, None)
        # options_list.append(t13)
        #
        # t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_platethk, VALUES_PLATETHK)
        # options_list.append(t14)

        return options_list
