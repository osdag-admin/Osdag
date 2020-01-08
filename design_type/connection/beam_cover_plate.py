from design_type.connection.moment_connection import MomentConnection
from utils.common.component import *
from Common import *
from utils.common.load import Load
import yaml
import os
import shutil
import logging

class BeamCoverPlate(MomentConnection):

    def __init__(self):
        super(BeamCoverPlate, self).__init__()


    def input_values(self, existingvalues={}):

        options_list = []

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

        t16 = (KEY_MODULE, KEY_DISP_BEAMCOVERPLATE, TYPE_MODULE, None, None)
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX, existingvalue_key_secsize, connectdb("Beams"))
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

        return options_list

    def set_input_values(self, design_dictionary):
        super(BeamCoverPlate, self).set_input_values(self, design_dictionary)

        self.preference = design_dictionary[KEY_FLANGEPLATE_PREFERENCES]

        self.section = Beam(designation=design_dictionary[KEY_SECSIZE], material_grade=design_dictionary[KEY_MATERIAL])

        self.web_bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                             bolt_type=design_dictionary[KEY_TYP], material_grade=design_dictionary[KEY_MATERIAL],
                             bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                             edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                             mu_f=design_dictionary[KEY_DP_BOLT_SLIP_FACTOR],
                             corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])

        self.flange_bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                                bolt_type=design_dictionary[KEY_TYP], material_grade=design_dictionary[KEY_MATERIAL],
                                bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                                edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                                mu_f=design_dictionary[KEY_DP_BOLT_SLIP_FACTOR],
                                corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])

        self.flange_plate = Plate(thickness=design_dictionary.get(KEY_FLANGEPLATE_THICKNESS, None),
                                  material_grade=design_dictionary[KEY_MATERIAL],
                                  gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.web_plate = Plate(thickness=design_dictionary.get(KEY_WEBPLATE_THICKNESS, None),
                               material_grade=design_dictionary[KEY_MATERIAL],
                               gap=design_dictionary[KEY_DP_DETAILING_GAP])

    def get_bolt_details(self):
        self.flange_bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.flange_bolt.bolt_diameter[0],
                                                       connecting_plates_tk=[self.flange_plate.thickness[0],
                                                                             self.section.flange_thickness],
                                                       bolt_hole_type=self.flange_bolt.bolt_hole_type)
        self.flange_bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.flange_bolt.bolt_diameter[0],
                                                       connecting_plates_tk=[self.web_plate.thickness[0],
                                                                             self.section.web_thickness],
                                                       bolt_hole_type=self.flange_bolt.bolt_hole_type)

        if self.preference == "Outside":
            self.flange_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.flange_bolt.bolt_diameter[0],
                                                     bolt_grade_provided=self.flange_bolt.bolt_grade[0],
                                                     connecting_plates_tk=[self.flange_plate.thickness[0],
                                                                           self.section.flange_thickness],
                                                     n_planes=1)
        else:
            self.flange_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.flange_bolt.bolt_diameter[0],
                                                     bolt_grade_provided=self.flange_bolt.bolt_grade[0],
                                                     connecting_plates_tk=[self.flange_plate.thickness[0],
                                                                           self.section.flange_thickness],
                                                     n_planes=2)
        min_plate_length = self.section.flange_width
        max_plate_length = self.section.flange_width
        axial_force_f = self.load.axial_force * self.section.flange_width * self.section.flange_thickness / self.section.area
        flange_force = (((self.load.moment * 1000000) / (self.section.depth - self.section.flange_thickness)) + (
                    axial_force_f * 1000)) / 1000

        self.flange_plate.get_web_plate_details(bolt_dia=self.flange_bolt.bolt_diameter[0],
                                                web_plate_l_min=min_plate_length,
                                                web_plate_l_max=max_plate_length,
                                                bolt_capacity=self.flange_bolt.bolt_capacity,
                                                connecting_plates_tk=[self.flange_plate.thickness[0],
                                                                      self.section.flange_thickness],
                                                bolt_hole_type=self.flange_bolt.bolt_hole_type,
                                                bolt_line_limit=10, axial_load=flange_force,
                                                shear_ecc=False)

        self.flange_plate.get_moment_cacacity(self.flange_plate.fy, self.flange_plate.thickness[0],
                                              self.flange_plate.length)
        ########################
        # Design of web splice plate

        min_web_plate_length = self.section.min_plate_length()
        max_web_plate_length = self.section.max_plate_length()
        axial_force_w = int(((self.section.depth - 2 * (
            self.section.flange_thickness)) * self.section.web_thickness * self.load.axial_force * 10) / self.section.area) / 1000
        self.web_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.web_bolt.bolt_diameter[0],
                                              bolt_grade_provided=self.web_bolt.bolt_grade[0],
                                              connecting_plates_tk=[self.web_plate.thickness[0],
                                                                    self.section.web_thickness],
                                              n_planes=2)

        self.web_plate.get_web_plate_details(bolt_dia=self.web_bolt.bolt_diameter[0],
                                             web_plate_l_min=min_web_plate_length,
                                             web_plate_l_max=max_web_plate_length,
                                             bolt_capacity=self.web_bolt.bolt_capacity,
                                             connecting_plates_tk=[2 * self.web_plate.thickness[0],
                                                                   self.section.web_thickness],
                                             bolt_hole_type=self.web_bolt.bolt_hole_type,
                                             bolt_line_limit=10, shear_load=self.load.shear_force,
                                             axial_load=axial_force_w,
                                             gap=self.web_plate.gap, shear_ecc=True)

        self.web_plate.get_moment_cacacity(self.web_plate.fy, self.web_plate.thickness[0],
                                           self.web_plate.length)
        print(self.section)
        print(self.load)
        print(self.flange_bolt)
        print(self.flange_plate)
        print(self.web_bolt)
        print(self.web_plate)