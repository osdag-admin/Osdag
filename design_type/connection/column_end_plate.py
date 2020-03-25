from design_type.connection.moment_connection import MomentConnection
from utils.common.component import *
from Common import *
from utils.common.load import Load
import yaml
import os
import shutil
import logging
import time

class ColumnEndPlate(MomentConnection):

    def __init__(self):
        super(ColumnEndPlate, self).__init__()

    def set_osdaglogger(key):

        """
        Function to set Logger for FinPlate Module
        """
        global logger
        logger = logging.getLogger('osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # handler.setLevel(logging.INFO)
        # formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        # handler.setFormatter(formatter)
        # logger.addHandler(handler)
        handler = OurLog(key)
        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def module_name(self):
        return KEY_DISP_COLUMNENDPLATE

    def input_values(self, existingvalues={}):

        options_list = []

        if KEY_SECSIZE in existingvalues:
            existingvalue_key_secsize = existingvalues[KEY_SECSIZE]
        else:
            existingvalue_key_secsize = ''

        if KEY_CONN in existingvalues:
            existingvalue_key_conn = existingvalues[KEY_CONN]
        else:
            existingvalue_key_conn = ''

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

        if KEY_ENDPLATE_THICKNESS in existingvalues:
            existingvalue_key_endplatethk = existingvalues[KEY_ENDPLATE_THICKNESS]
        else:
            existingvalue_key_endplatethk = ''

        t16 = (KEY_MODULE, KEY_DISP_COLUMNENDPLATE, TYPE_MODULE, None, None)
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX, existingvalue_key_secsize, connectdb("Columns"))
        options_list.append(t4)

        t8 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, existingvalue_key_conn, VALUES_CONN_3)
        options_list.append(t8)

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

        t21 = (None, DISP_TITLE_ENDPLATE, TYPE_TITLE, None, None)
        options_list.append(t21)

        t22 = (KEY_ENDPLATE_THICKNESS, KEY_DISP_ENDPLATE_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_endplatethk, VALUES_ENDPLATE_THICKNESS)
        options_list.append(t22)

        return options_list

    def spacing(self, status):

        spacing = []

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.plate.pitch_provided if status else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.plate.end_dist_provided if status else '')
        spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.plate.gauge_provided if status else '')
        spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.plate.edge_dist_provided if status else '')
        spacing.append(t12)

        return spacing

    def plate_details(self, flag):
        plate_details = []

        t8 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_HEIGHT, TYPE_TEXTBOX, self.plate.height if flag else '')
        plate_details.append(t8)

        t9 = (KEY_OUT_PLATE_WIDTH, KEY_OUT_DISP_PLATE_WIDTH, TYPE_TEXTBOX,self.plate.length if flag else '')
        plate_details.append(t9)

        t10 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX, self.plate.thickness if flag else '')
        plate_details.append(t10)

        return plate_details

    def output_values(self, flag):

        out_list = []

        t1 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None)
        out_list.append(t1)

        t2 = (KEY_D, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX,self.bolt.bolt_diameter_provided if flag else '')
        out_list.append(t2)

        t3 = (KEY_GRD, KEY_DISP_GRD, TYPE_TEXTBOX,self.bolt.bolt_grade_provided if flag else '')
        out_list.append(t3)

        t4 = (None, DISP_TITLE_BOLT_CAPACITIES, TYPE_TITLE, None)
        out_list.append(t4)

       

    def set_input_values(self, design_dictionary):

        print(design_dictionary)

        super(ColumnEndPlate, self).set_input_values(self, design_dictionary)

        self.section = Column(designation=design_dictionary[KEY_SECSIZE],
                              material_grade=design_dictionary[KEY_MATERIAL])

        self.start_time = time.time()

        self.module = design_dictionary[KEY_MODULE]

        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None), material_grade=design_dictionary[KEY_PLATE_MATERIAL])
        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                         bolt_type=design_dictionary[KEY_TYP], material_grade=design_dictionary[KEY_MATERIAL],
                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         mu_f=design_dictionary[KEY_DP_BOLT_SLIP_FACTOR],
                         corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])

    def detailing(self):
        self.n_bw = ((self.section.depth -(2 * self.section.flange_thickness - (2 * self.plate.end_dist_provided))) / self.plate.pitch_provided) + 1
        self.n_bf = ((self.section.flange_width/2) - (self.section.web_thickness/2) - (2 * self.plate.end_dist_provided) / self.plate.pitch_provided) + 1
        if self.n_bw % 2 == 0:
            self.p_2 = self.section.depth - (2 * self.section.flange_thickness) - (2 * self.plate.end_dist_provided) - ((self.n_bw - 2) * self.plate.pitch_provided)
        else:
            self.p_2 = self.section.depth - (2 * self.section.flange_thickness) - (2 * self.plate.end_dist_provided) - ((self.n_bw - 3) * self.plate.pitch_provided)

        self.x = (self.section.flange_width/2) - (self.section.web_thickness/2) - self.plate.end_dist_provided - (self.n_bf * self.plate.pitch_provided)

    def hard_values(self):
            # flange bolt
            self.load.moment = 20  # kN
            self.factored_axial_load = 300  # KN
            self.load.shear_force = 50  # kN
            self.flange_bolt.bolt_type = "Bearing Bolt"
            # self.flange_bolt.bolt_hole_type = bolt_hole_type
            # self.flange_bolt.edge_type = edge_type
            # self.flange_bolt.mu_f = float(mu_f)
            self.flange_bolt.connecting_plates_tk = None

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
        d = VALUES_COLUMN_ENDPLATE_THICKNESS_CUSTOMIZED
        return d

    def customized_input(self):

        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)
        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)
        t6 = (KEY_ENDPLATE_THICKNESS, self.endplate_thick_customized)
        list1.append(t6)
        return list1