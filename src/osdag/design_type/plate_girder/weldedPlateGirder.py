"""

@Author:    Rutvik Joshi - Osdag Team, IIT Bombay [(P) rutvikjoshi63@gmail.com / 30005086@iitb.ac.in]

@Module - Plate Girder- Welded

@Reference(s): 1) IS 800: 2007, General construction in steel - Code of practice (Third revision)
               2) IS 808: 1989, Dimensions for hot rolled steel beam, column, channel, and angle sections and
                                it's subsequent revision(s)
               3) Design of Steel Structures by N. Subramanian (Fifth impression, 2019, Chapter 15)
               4) Limit State Design of Steel Structures by S K Duggal (second edition, Chapter 11)

other          8)
references     9)

"""
import logging
import math
import numpy as np
from ...Common import *
# from ..connection.moment_connection import MomentConnection
from ...utils.common.material import *
from ...utils.common.load import Load
from ...utils.common.component import ISection, Material
from ...utils.common.component import *
from ..member import Member
from ...Report_functions import *
from ...design_report.reportGenerator_latex import CreateLatex
from ...utils.common.common_calculation import *
from ..tension_member import *
from ...utils.common.Section_Properties_Calculator import BBAngle_Properties
from ...utils.common import is800_2007
from ...utils.common.component import *
from ...utils.common.Section_Properties_Calculator import I_sectional_Properties
from ..flexural_member.flexure import Flexure
'''
Debugging tools
'''
# from icecream import ic

class Custom_Girder():#Material
    # def __new__(self,design_dictionary):
    def __init__(self, design_dictionary,design):
        # super(Custom_Girder,self).__init__()#material_grade
        print("Girder Object Initialised")
        self.designation = 'User Defined'
        if design:
            self.flange_thickness = 1e-3
            self.depth = 1e-3
            self.depth_web = 1e-3
            self.flange_width = 1e-3
            self.web_thickness = 1e-3
            self.flange_slope = 90
            self.root_radius = 1e-3
            self.toe_radius = 1e-3
            self.type = 'Welded'
            self.shear_area = self.depth_web * self.web_thickness
            self.mass = round(
                I_sectional_Properties().calc_Mass(self.depth, self.flange_width, self.web_thickness, self.flange_thickness,
                                                self.flange_slope, self.root_radius, self.toe_radius) * 10 ** 1)
            self.area = round(
                I_sectional_Properties().calc_Area(self.depth, self.flange_width, self.web_thickness, self.flange_thickness,
                                                self.flange_slope, self.root_radius, self.toe_radius) * 10 ** 2)
            self.mom_inertia_z = round(
                I_sectional_Properties().calc_MomentOfAreaZ(self.depth, self.flange_width, self.web_thickness,
                                                            self.flange_thickness, self.flange_slope, self.root_radius,
                                                            self.toe_radius) * 10 ** 4)
            self.mom_inertia_y = round(
                I_sectional_Properties().calc_MomentOfAreaY(self.depth, self.flange_width, self.web_thickness,
                                                            self.flange_thickness, self.flange_slope, self.root_radius,
                                                            self.toe_radius) * 10 ** 4)
            self.rad_of_gy_z = round(
                I_sectional_Properties().calc_RogZ(self.depth, self.flange_width, self.web_thickness, self.flange_thickness,
                                                self.flange_slope, self.root_radius, self.toe_radius) * 10 ** 1)
            self.rad_of_gy_y = round(
                I_sectional_Properties().calc_RogY(self.depth, self.flange_width, self.web_thickness, self.flange_thickness,
                                                self.flange_slope, self.root_radius, self.toe_radius) * 10 ** 1)
            self.elast_sec_mod_z = round(
                I_sectional_Properties().calc_ElasticModulusZz(self.depth, self.flange_width, self.web_thickness,
                                                            self.flange_thickness, self.flange_slope, self.root_radius,
                                                            self.toe_radius) * 10 ** 3)
            self.elast_sec_mod_y = round(
                I_sectional_Properties().calc_ElasticModulusZy(self.depth, self.flange_width, self.web_thickness,
                                                            self.flange_thickness, self.flange_slope, self.root_radius,
                                                            self.toe_radius) * 10 ** 3)
            self.plast_sec_mod_z = round(
                I_sectional_Properties().calc_PlasticModulusZpz(self.depth, self.flange_width, self.web_thickness,
                                                                self.flange_thickness, self.flange_slope, self.root_radius,
                                                                self.toe_radius) * 10 ** 3)
            self.plast_sec_mod_y = round(
                I_sectional_Properties().calc_PlasticModulusZpy(self.depth, self.flange_width, self.web_thickness,
                                                                self.flange_thickness, self.flange_slope, self.root_radius,
                                                                self.toe_radius) * 10 ** 3)
                # print(self.flange_thickness)
        else :
            self.section_defined(design_dictionary)

    def section_defined(self,design_dictionary):
        self.flange_thickness = float(design_dictionary[KEY_tf])
        self.depth_web = float(design_dictionary[KEY_dw])
        self.depth = float(design_dictionary[KEY_dw]) + 2 * self.flange_thickness
        self.flange_width = float(design_dictionary[KEY_bf])
        self.web_thickness = float(design_dictionary[KEY_tw])
        self.flange_slope = 90
        self.root_radius = 0
        self.toe_radius = 0
        self.type = 'Welded'
        self.shear_area = self.depth_web * self.web_thickness

        self.mass = round(
            I_sectional_Properties().calc_Mass(self.depth, self.flange_width, self.web_thickness, self.flange_thickness,
                                               self.flange_slope, self.root_radius, self.toe_radius) * 10 ** 1)
        self.area = round(
            I_sectional_Properties().calc_Area(self.depth, self.flange_width, self.web_thickness, self.flange_thickness,
                                               self.flange_slope, self.root_radius, self.toe_radius) * 10 ** 2)
        self.mom_inertia_z = round(
            I_sectional_Properties().calc_MomentOfAreaZ(self.depth, self.flange_width, self.web_thickness,
                                                        self.flange_thickness, self.flange_slope, self.root_radius,
                                                        self.toe_radius) * 10 ** 4)
        self.mom_inertia_y = round(
            I_sectional_Properties().calc_MomentOfAreaY(self.depth, self.flange_width, self.web_thickness,
                                                        self.flange_thickness, self.flange_slope, self.root_radius,
                                                        self.toe_radius) * 10 ** 4)
        self.rad_of_gy_z = round(
            I_sectional_Properties().calc_RogZ(self.depth, self.flange_width, self.web_thickness, self.flange_thickness,
                                               self.flange_slope, self.root_radius, self.toe_radius) * 10 ** 1)
        self.rad_of_gy_y = round(
            I_sectional_Properties().calc_RogY(self.depth, self.flange_width, self.web_thickness, self.flange_thickness,
                                               self.flange_slope, self.root_radius, self.toe_radius) * 10 ** 1)
        self.elast_sec_mod_z = round(
            I_sectional_Properties().calc_ElasticModulusZz(self.depth, self.flange_width, self.web_thickness,
                                                           self.flange_thickness, self.flange_slope, self.root_radius,
                                                           self.toe_radius) * 10 ** 3)
        self.elast_sec_mod_y = round(
            I_sectional_Properties().calc_ElasticModulusZy(self.depth, self.flange_width, self.web_thickness,
                                                           self.flange_thickness, self.flange_slope, self.root_radius,
                                                           self.toe_radius) * 10 ** 3)
        self.plast_sec_mod_z = round(
            I_sectional_Properties().calc_PlasticModulusZpz(self.depth, self.flange_width, self.web_thickness,
                                                            self.flange_thickness, self.flange_slope, self.root_radius,
                                                            self.toe_radius) * 10 ** 3)
        self.plast_sec_mod_y = round(
            I_sectional_Properties().calc_PlasticModulusZpy(self.depth, self.flange_width, self.web_thickness,
                                                            self.flange_thickness, self.flange_slope, self.root_radius,
                                                            self.toe_radius) * 10 ** 3)
        # print(self.flange_thickness)
    def __str__(self) -> str:
        return "Customised Girder generated"
class PlateGirderWelded(Member):

    def __init__(self):
        super(PlateGirderWelded, self).__init__()

    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):
        """

        :return: This function returns the list of tuples. Each tuple will create a tab in design preferences, in the
        order they are appended. Format of the Tuple is:
        [Tab Title, Type of Tab, function for tab content)
        Tab Title : Text which is displayed as Title of Tab,
        Type of Tab: There are Three types of tab layouts.
            Type_TAB_1: This have "Add", "Clear", "Download xlsx file" "Import xlsx file"
            TYPE_TAB_2: This contains a Text box for side note.
            TYPE_TAB_3: This is plain layout
        function for tab content: All the values like labels, input widgets can be passed as list of tuples,
        which will be displayed in chosen tab layout

        """
        tabs = []
        t1 = (KEY_DISP_COLSEC, TYPE_TAB_1, self.tab_section)
        tabs.append(t1)
        # t2 = ("Under Development", TYPE_TAB_2, self.optimization_tab_plate_girder_design)
        # tabs.append(t2)

        t5 = ("Under Development", TYPE_TAB_2, self.optimization_tab_plate_girder_design)
        tabs.append(t5)

        t1 = ("Stiffeners", TYPE_TAB_2, self.Stiffener_design)
        tabs.append(t1)

        t5 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t5)

        return tabs
    def tab_value_changed(self):
        change_tab = []

        t1 = (KEY_DISP_COLSEC, [KEY_SEC_MATERIAL], [KEY_SEC_FU, KEY_SEC_FY], TYPE_TEXTBOX, self.get_fu_fy_I_section)
        change_tab.append(t1)

        t4 = (KEY_DISP_COLSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22', KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t4)

        t5 = (KEY_DISP_COLSEC, ['Label_HS_1', 'Label_HS_2', 'Label_HS_3'],
              ['Label_HS_11', 'Label_HS_12', 'Label_HS_13', 'Label_HS_14', 'Label_HS_15', 'Label_HS_16', 'Label_HS_17', 'Label_HS_18',
               'Label_HS_19', 'Label_HS_20', 'Label_HS_21', 'Label_HS_22', KEY_IMAGE], TYPE_TEXTBOX, self.get_SHS_RHS_properties)
        change_tab.append(t5)

        t6 = (KEY_DISP_COLSEC, ['Label_CHS_1', 'Label_CHS_2', 'Label_CHS_3'],
              ['Label_CHS_11', 'Label_CHS_12', 'Label_CHS_13', 'Label_HS_14', 'Label_HS_15', 'Label_HS_16', 'Label_21', 'Label_22',
               KEY_IMAGE], TYPE_TEXTBOX, self.get_CHS_properties)
        change_tab.append(t6)

        t6 = (KEY_DISP_COLSEC, [KEY_SECSIZE], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t6)

        return change_tab

    def edit_tabs(self):
        """ This function is required if the tab name changes based on connectivity or profile or any other key.
                Not required for this module but empty list should be passed"""
        return []
    def input_dictionary_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to design dictionary.

         It returns list of tuple which contains, tab name, input widget type of keys, keys whose values to be saved,

         [(Tab Name, input widget type of keys, [List of keys to be saved])]
        TODO : Material pop-up
         """
        design_input = []

        t1 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])#Need to check
        design_input.append(t1)

        t1 = (KEY_DISP_COLSEC, TYPE_TEXTBOX, [KEY_SEC_FU, KEY_SEC_FY])
        design_input.append(t1)

        t2 = ("Under Development", TYPE_TEXTBOX, [ KEY_EFFECTIVE_AREA_PARA, KEY_LENGTH_OVERWRITE, KEY_BEARING_LENGTH]) #, KEY_STEEL_COST
        design_input.append(t2)

        t2 = ("Under Development", TYPE_COMBOBOX, [KEY_ALLOW_CLASS, KEY_LOAD, KEY_ShearBucklingOption]) #, KEY_STEEL_COST
        design_input.append(t2)

        t2 = ("Stiffeners", TYPE_COMBOBOX, [KEY_IntermediateStiffener])
        design_input.append(t2)

        t2 = ("Stiffeners", TYPE_TEXTBOX, [KEY_IntermediateStiffener_spacing])
        design_input.append(t2)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        return design_input
    def input_dictionary_without_design_pref(self):

        design_input = []
        t2 = (KEY_MATERIAL, [KEY_DP_DESIGN_METHOD], 'Input Dock')
        design_input.append(t2)

        t2 = (None, [KEY_ALLOW_CLASS, KEY_EFFECTIVE_AREA_PARA, KEY_LENGTH_OVERWRITE,KEY_BEARING_LENGTH, KEY_LOAD, KEY_DP_DESIGN_METHOD, KEY_ShearBucklingOption, KEY_IntermediateStiffener_spacing, KEY_IntermediateStiffener], '')
        design_input.append(t2)

        return design_input

    def refresh_input_dock(self):

        add_buttons = []

        t2 = (KEY_DISP_COLSEC, KEY_SECSIZE, TYPE_COMBOBOX, KEY_SECSIZE, None, None, "Columns")
        add_buttons.append(t2)

        return add_buttons

    def get_values_for_design_pref(self, key, design_dictionary):
        if design_dictionary[KEY_MATERIAL] != 'Select Material':
            material = Material(design_dictionary[KEY_MATERIAL], 41)
            fu = material.fu
            fy = material.fy
        else:
            fu = ''
            fy = ''

        val = {
            KEY_ALLOW_CLASS: 'Yes',
            KEY_EFFECTIVE_AREA_PARA: '1.0',
            KEY_LENGTH_OVERWRITE :'NA',
            KEY_BEARING_LENGTH : 'NA',
            KEY_LOAD : 'Normal',
            KEY_DP_DESIGN_METHOD: "Limit State Design",
            KEY_ShearBucklingOption: KEY_DISP_SB_Option[0],
            KEY_IntermediateStiffener:'Yes',
            KEY_IntermediateStiffener_spacing:'NA'
        }[key]

        return val
    ####################################
    # Design Preference Functions End
    ####################################

    # Setting up logger and Input and Output Docks
    ####################################
    def module_name(self):
        # self.mainmodule = KEY_PLATE_GIRDER_MAIN_MODULE
        return KEY_DISP_PLATE_GIRDER_WELDED

    def set_osdaglogger(key):
        """
        Set logger for Column Design Module.
        """
        global logger
        logger = logging.getLogger('Osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if key is not None:
            handler = OurLog(key)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def customized_input(self):

        c_lst = []
        t1 = (KEY_SECSIZE, self.fn_profile_section)
        c_lst.append(t1) # 'TEMP2'

        return c_lst
        # return []

    def fn_profile_section(self):

        profile = self[0]
        if profile == 'Beams': #Beam and Column
            return connectdb("Beams", call_type="popup")
            profile2 = connectdb("Columns", call_type="popup")
        if profile == 'Columns': #Beam and Column
            return connectdb("Columns", call_type="popup")

    def input_values(self):

        self.module = PlateGirderWelded.module_name(self)
        options_list = []

        # t1 = (KEY_MODULE, KEY_DISP_FLEXURE, TYPE_MODULE, None, True, "No Validator")
        # options_list.append(t1)

        t2 = (KEY_SEC_PROFILE, 'Section Profile', TYPE_COMBOBOX, VALUES_SEC_PROFILE3, True, 'No Validator') # 'TEMP1'
        options_list.append(t2)

        t4 = (KEY_SECSIZE, 'Section Size', TYPE_COMBOBOX_CUSTOMIZED, ['All','Customized'], True, 'No Validator') #'TEMP2'
        options_list.append(t4)

        t1 = (KEY_MODULE, self.module, TYPE_MODULE, None, True, "No Validator")
        options_list.append(t1)

        t1 = (KEY_SECTION_PROFILE, KEY_SECTION_DATA, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_SEC_PROFILE, KEY_DISP_Plate_Girder_PROFILE, TYPE_NOTE, KEY_PLATE_GIRDER_MAIN_MODULE, True, 'No Validator') #'Beam and Column'
        options_list.append(t2)

        t1 = (KEY_tf, KEY_DISP_tf + '*', TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t1)
        t1 = (KEY_tw, KEY_DISP_tw + '*', TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t1)
        t1 = (KEY_dw, KEY_DISP_dw + '*', TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t1)
        t1 = (KEY_bf, KEY_DISP_bf + '*', TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t1)

        t4 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t4)
        t5 = (KEY_LENGTH, KEY_DISP_LENGTH_BEAM, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t5)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t7)

        t8 = (KEY_MOMENT, KEY_DISP_MOMENT, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t8)

        t8 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t8)



        t8 = (KEY_BUCKLING_STRENGTH, KEY_DISP_BUCKLING_STRENGTH, TYPE_COMBOBOX, ['Yes','No'], True, 'No Validator')
        options_list.append(t8)

        t8 = (KEY_WEB_CRIPPLING, KEY_DISP_CRIPPLING_STRENGTH, TYPE_COMBOBOX, ['Yes','No'], True, 'No Validator')
        options_list.append(t8)
        return options_list

    def input_value_changed(self):

        lst = []

        t1 = ([KEY_SEC_PROFILE], KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, self.fn_profile_section)
        lst.append(t1)

        t3 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t3)
        return lst

    def output_values(self, flag):

        out_list = []
        t1 = (None, DISP_TITLE_STRUT_SECTION, TYPE_TITLE, None, True)

        out_list.append(t1)
        t2 = (KEY_betab_constatnt, KEY_DISP_betab_constatnt, TYPE_TEXTBOX,
              'NA', True)
        out_list.append(t2)

        t2 = (KEY_SEC_PROFILE, KEY_DISP_Plate_Girder_PROFILE, TYPE_NOTE, KEY_PLATE_GIRDER_MAIN_MODULE, True) #'Beam and Column'
        out_list.append(t2)

        t1 = (KEY_tf, KEY_DISP_tf, TYPE_TEXTBOX, self.result_tf if flag else '', True) # "NA"
        out_list.append(t1)
        t1 = (KEY_tw, KEY_DISP_tw, TYPE_TEXTBOX, self.result_tw if flag else '', True) # "NA"
        out_list.append(t1)
        t1 = (KEY_dw, KEY_DISP_dw, TYPE_TEXTBOX, self.result_dw if flag else '', True) # "NA"
        out_list.append(t1)
        t1 = (KEY_bf, KEY_DISP_bf, TYPE_TEXTBOX, self.result_bf if flag else '', True) # "NA"
        out_list.append(t1)

        t1 = (KEY_SHEAR_STRENGTH, KEY_DISP_DESIGN_STRENGTH_SHEAR, TYPE_TEXTBOX,
              self.result_shear if flag else
              '', True)
        out_list.append(t1)
        #
        t1 = (KEY_MOMENT_STRENGTH, KEY_DISP_DESIGN_STRENGTH_MOMENT, TYPE_TEXTBOX,
              self.result_bending if flag else
              '', True)
        out_list.append(t1)

        return out_list

    def func_for_validation(self, design_dictionary):
        print(f"func_for_validation here")
        all_errors = []
        self.design_status = False
        flag = False
        flag1 = False
        flag2 = False
        flag3 = False
        flag4 = False
        option_list = self.input_values(self)
        missing_fields_list = []
        print(f'func_for_validation option_list {option_list}'
            f"\n  design_dictionary {design_dictionary}")
        for option in option_list:
            # print(option_list)
            if option[2] == TYPE_TEXTBOX and option[0] == KEY_LENGTH or option[0] == KEY_SHEAR or option[0] == KEY_MOMENT:
                if design_dictionary[option[0]] == '':
                    missing_fields_list.append(option[1])
                    continue
                if option[0] == KEY_LENGTH:
                    if float(design_dictionary[option[0]]) <= 0.0:
                        print("Input value(s) cannot be equal or less than zero.")
                        error = "Input value(s) cannot be equal or less than zero."
                        all_errors.append(error)
                    else:
                        flag1 = True
                elif option[0] == KEY_SHEAR:
                    if float(design_dictionary[option[0]]) < 0.0:
                        print("Input value(s) cannot be less than zero.")
                        error = "Input value(s) cannot be less than zero."
                        all_errors.append(error)
                    else:
                        flag2 = True
                elif option[0] == KEY_MOMENT:
                    if float(design_dictionary[option[0]]) < 0.0:
                        print("Input value(s) cannot be less than zero.")
                        error = "Input value(s) cannot be less than zero."
                        all_errors.append(error)
                    else:
                        flag3 = True
            if option[0] == KEY_tf :
                if design_dictionary[KEY_tf] != "" and design_dictionary[KEY_tw] != "" and design_dictionary[KEY_dw] != "" and design_dictionary[KEY_bf] != "":
                    flag4 = True
                # TODO elif design_dictionary[KEY_tf] == "" and design_dictionary[KEY_tw] == "" and design_dictionary[KEY_dw] == "" and design_dictionary[KEY_bf] == "":
                #     flag4 = True
                else:
                    list_adder = lambda x,y: missing_fields_list.append(x) if design_dictionary[y] == "" else False
                    for i in [(KEY_tf,KEY_DISP_tf),(KEY_tw,KEY_DISP_tw),(KEY_dw,KEY_DISP_dw),(KEY_bf,KEY_DISP_bf)]:
                        list_adder(i[1],i[0])


        if len(missing_fields_list) > 0:
            error = self.generate_missing_fields_error_string(self, missing_fields_list)
            all_errors.append(error)
        else:
            flag = True

        if flag and flag1 and flag2 and flag3 and flag4:
            print(f"\n design_dictionary{design_dictionary}")
            self.set_input_values(self, design_dictionary) #
            self.results(self, design_dictionary) #
        else:
            return all_errors
    def isfloat(input_list):
        for i in range(len(input_list)):
            try:
                print(input_list[i])
                yield isinstance(float(input_list[i]),float)
            except:
                yield False
    # Setting inputs from the input dock GUI
    def set_input_values(self, design_dictionary):
        # out_list = []
        ### INPUT FROM INPUT DOCK ####
        self.length = float(design_dictionary[KEY_LENGTH])*10**3 #m -> mm
        self.material = design_dictionary[KEY_MATERIAL]
        self.load = Load(0,design_dictionary[KEY_SHEAR],design_dictionary[KEY_MOMENT],unit_kNm=True) #KN -> N
        print()
        self.sec_profile = design_dictionary[KEY_SEC_PROFILE]

        # Safety Factors
        self.gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]["yielding"]
        self.gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]["ultimate_stress"]
        self.material_property = Material(material_grade=self.material, thickness=0)
        self.epsilon = math.sqrt(250 / self.material_property.fy)

        ### INPUT FROM DESIGN PREFERENCE ###
        # Tab2
        self.support_cndition_shear_buckling = design_dictionary[KEY_ShearBucklingOption]
        self.section_class_req = "Plastic" # or "Compact"
        # end condition
        # self.support = design_dictionary[KEY_SUPPORT]
        # TODO check if self.effective_length could be different
        self.effective_length = self.length

        # Tab3
        # No option for End Post
        self.EndStiffener = 'Yes'
        self.IntermediateStiffener = design_dictionary[KEY_IntermediateStiffener]
        self.IntermediateStiffener_spacing=  design_dictionary[KEY_IntermediateStiffener_spacing] if self.IntermediateStiffener else "NA"
        print("Intermediate Stiffener",self.IntermediateStiffener)
        self.effective_area_factor = float(design_dictionary[KEY_EFFECTIVE_AREA_PARA])
        #TODO : future inputs add to design preference
        self.web_type_needed = "Thick" # or "Slim"
        # TODO self.servicibility_check CL: 8.6.1.1
        self.servicibility_check = True
        self.compression_flange_buckling = True


        ## Calculation Variables
        self.fyw = self.material_property.fy
        self.fyf = self.material_property.fy
        # Flexure.effective_length_beam(self, design_dictionary, self.length)
        self.web_siffened = False
        self.steel_cost_per_kg = 50
        self.section_parameters = [KEY_tf,KEY_tw,KEY_dw,KEY_bf]
        self.temp_section_list = [design_dictionary[KEY_tf], design_dictionary[KEY_tw],design_dictionary[KEY_dw],design_dictionary[KEY_bf]]#[1,4]
        self.section_list = [i for i in self.isfloat(self.temp_section_list)]
        print(self.section_list)

        # self.latex_efp = design_dictionary[KEY_LENGTH_OVERWRITE]


        # self.allowable_utilization_ratio = 1.0
        # self.optimization_parameter = "Utilization Ratio"
        # self.allow_class = design_dictionary[KEY_ALLOW_CLASS]  # if 'Semi-Compact' is available
        # # Step 2 - computing the design compressive stress for web_buckling & web_crippling
        # self.bearing_length = design_dictionary[KEY_BEARING_LENGTH]
        # #TAKE from Design Dictionary
        # self.allowed_sections = []
        # if self.allow_class == "Yes":
        #     self.allowed_sections == "Semi-Compact"
        # "Semi-Compact"
        #############
        # LATEX VARIABLES
        #############

        def main_controller(design_dictionary):
            # Assign custom section def to calulate properties
            self.optimum_section_ur_results = {}
            self.optimum_section_ur = []
            list_result = []
            list_1 = []
            # 1. optimization_tab_check from Design preference
            self.optimization_tab_check(self)
            # 2. Check if user has provided a section or wants us to find optimised section
            if all(self.section_list):
                # print()
                # self.optimization_tab_check(self)
                self.design = False
                N_sections_list = [tuple(self.temp_section_list)]
            else:
                self.design = True
                self.section_design(self,0, 150)
                self.optimum_section_ur_results['Section Dimension'] = self.designed_dict
                self.section_check_validator(self,True,True, design_dictionary)
                # TODO Get the section list

            # TODO 3. Loop starts to check a sections strength and utilization
            for section in N_sections_list:
                if self.design:
                    # TODO:
                    # Must return tuples of Section Sizes in the set of 10.. meaning if the most optmised section is at the end of the this list...find section...stronger or weaker
                    #  Find depth of web
                    #  1. d/tw and Kv determination
                    #  2. Servicibility requirement
                    #  3. Compression Buckling requirement
                    #
                    self.section_design(self,0, 150)
                    self.optimum_section_ur_results['Section Dimension'] = self.designed_dict
                    self.section_check_validator(self,True,True, design_dictionary)
                # TODO else:
                #     self.section_classification(self)
                #     self.section_check_validator(self,True,False, design_dictionary)
                print(section )

                self.girder_checks(self,section=section)

                # UR Check
                self.UR_ratio = max(self.single_section_dictionary['Shear_Strength']/self.load.shear_force*10**3,0)
                self.optimum_section_ur_results[self.UR_ratio] = self.single_section_dictionary

                print(self.optimum_section_ur_results)







        return main_controller(design_dictionary)

    def girder_checks(self,section):
        # Tuple to Dictionary Converter
        print(type(section))
        print(dict(zip(self.section_parameters,section)))
        self.single_section_dictionary = dict(zip(self.section_parameters,section))
        print(self.single_section_dictionary)
        # 4. Finding other parameters of the section
        self.Girder_SectionProperty(self,self.single_section_dictionary,self.design)

        # 5. Checks
        # 5.1 Web needed by User Thick or thin
        if 'Check1' not in self.single_section_dictionary :# TODO check if required -> or self.single_section_dictionary['Check1'] == None
            self.single_section_dictionary['Check1'] = self.checks(self,1)
        # 5.2 servicibility_check Only for Intermediate Transverse stiffener
        self.single_section_dictionary['Check2'] = self.checks(self,2)
        # 5.3 compression_flange_buckling
        self.single_section_dictionary['Check3'] = self.checks(self,3)

        # 6 Section Classification
        _ = self.section_classification(self)
        self.single_section_dictionary.update(_)

        # Calculation Variable
        self.effective_depth = self.section_property.depth_web

        # 6 Shear Strength
        # 6.1 Shear Strength without any Stiffeners
        self.Shear_Strength(self)
        self.single_section_dictionary['Shear_Strength'] = self.V_d
        self.single_section_dictionary['V_d'] = self.V_d
        print(self.V_d,self.load.shear_force)

        # 6.2 Shear Strength with end Stiffeners only
        if self.single_section_dictionary['Shear_Strength'] < self.load.shear_force/1000:
            if self.EndStiffener and self.support_cndition_shear_buckling == KEY_DISP_SB_Option[0] :#or self.support_cndition_shear_buckling == KEY_DISP_SB_Option[1])
        # Variables needed for to work
                Flexure.set_osdaglogger(None)
                Flexure.web_buckling_steps(self)
                _ = (('Kv',self.K_v),
                ('tau_crc',self.tau_crc),
                ('lambda_w', self.lambda_w),
                ('tau_b', self.tau_b),
                ("V_cr",self.V_cr))
                self.single_section_dictionary.update(_)

                self.single_section_dictionary['Shear_Strength'] = self.single_section_dictionary["V_cr"]
            elif self.EndStiffener and self.support_cndition_shear_buckling ==  KEY_DISP_SB_Option[1]:
                self.V_p = IS800_2007.cl_8_4_design_shear_strength(
                    self.section_property.shear_area,
                    self.material_property.fy
                ) / 10 ** 3 * self.gamma_m0
                self.Mfr = IS800_2007.cl_8_4_2_2_Mfr_TensionField(self.section_property.flange_width,
                                                        self.section_property.flange_thickness, self.fyf,
                                                        self.load.moment / (
                                                                self.section_property.depth - self.section_property.flange_thickness),
                                                        self.gamma_m0)

                if self.Mfr > 0:
                    print('Starting loop', int(round(self.effective_length*10**4/self.effective_depth,-1)/10))
                    # for c_d in range(3,self.effective_length/self.result_eff_d):
                    for c_d in reversed(list(range(3,int(round(self.effective_length * 1000/self.effective_depth,-1))))):
                        print('c_d',c_d,'c/d',self.effective_length * 1000/self.effective_depth)
                        c_d = c_d/10 + 0.1
                        self.c = round(c_d * self.effective_depth, -1)
                        print('c',self.c)
                        self.K_v = IS800_2007.cl_8_4_2_2_K_v_Simple_postcritical('many support', self.c, self.effective_depth)
                        self.plate_girder_strength2(self)

                        self.shear_strength = self.V_tf_girder / self.gamma_m0 * 10**-3
                        logger.info('Intermediate Stiffeners required d ={}, c = {}, Section = {}, V_tf = {}, V_d = {}'.format(self.effective_depth,self.c,
                        self.section_property.designation,self.V_tf_girder,self.shear_strength))
                        if self.shear_strength > self.load.shear_force * 10**-3:
                            return

        print(self.single_section_dictionary)

    def Girder_SectionProperty(self,design_dictionary,var):
        print(Custom_Girder)
        print(f'temp_section_list = {self.temp_section_list}')

        print(f'section_list = {self.section_list}')
        # if isinstance(float(design_dictionary[KEY_tf]),float) and

        self.section_property = Custom_Girder(design_dictionary, var)
        # print(self.section_property.flange_thickness,
        #       self.section_property.depth_web,
        #       self.section_property.depth_section,
        #       self.section_property.flange_width,
        #       self.section_property.web_thickness,
        #       self.section_property.flange_slope,
        #       self.section_property.root_radius,
        #       self.section_property.toe_radius,
        #       self.section_property.mass,
        #       self.section_property.area,  # mm
        #       self.section_property.mom_inertia_z,
        #       self.section_property.mom_inertia_y,
        #       self.section_property.rad_of_gy_z,
        #       self.section_property.rad_of_gy_y,
        #       self.section_property.elast_sec_mod_z,
        #       self.section_property.elast_sec_mod_y,
        #       self.section_property.plast_sec_mod_z,
        #       self.section_property.plast_sec_mod_y)

    def optimization_tab_check(self):
        print()
        # self.latex_tension_zone = False
        if (self.effective_area_factor <= 0.10) or (self.effective_area_factor > 1.0):
            logger.error(
                "The defined value of Effective Area Factor in the design preferences tab is out of the suggested range."
            )
            # logger.info("Provide an appropriate input and re-design.")
            logger.warning("Assuming a default value of 1.0.")
            self.effective_area_factor = 1.0
            # self.design_status = False
            # self.design_status_list.append(self.design_status)
            self.optimization_tab_check(self)
        logger.info("Provided appropriate design preference, now checking input.")

    def section_design(self,count, k= 150):
        self.section_class_girder = ""

          # 180, d/tw or take span/20 and go on increasing
        while self.section_class_girder != self.section_class_req and count <25:
            self.section_property.depth_web = int(round((self.load.moment * k / (self.material_property.fy)) ** 0.33, -1)) + count * 5
            self.section_property.web_thickness = int(min(round((self.load.moment / (self.material_property.fy * k**2)) ** 0.33,-1)),self.section_property.depth_web/k) + count * 5
            if self.IntermediateStiffener =="Yes":
                self.optimum_depth_thickness_web(self,self.checks,[1])
            else:
                self.optimum_depth_thickness_web(self,self.checks,[1,2,3])

            self.section_property.flange_width = self.myround(0.3 * self.section_property.depth_web - count,5 ,'low')
            i = 0
            while self.section_class_girder != self.section_class_req and self.section_property.flange_thickness<60:
                self.optimum_depth_thickness_flange(self,i)
                i+=1
                self.section_classification(self)
            # count = count+1
            # k = k + 5
            print(count,'depth & web_thickness',self.section_property.depth_web, self.section_property.web_thickness,self.section_property.flange_width,self.section_property.flange_thickness, "self.section_class_girder",self.section_class_girder)
        self.designed_dict = { KEY_tf  : self.section_property.flange_thickness  ,
                            KEY_dw:  self.section_property.depth_web ,
                            KEY_bf: self.section_property.flange_width  ,
                            KEY_tw:  self.section_property.web_thickness ,}

    def section_design_web(self,count, k= 150):
        # TODO
        self.section_property.web_thickness = ic(int(min(round((self.load.moment / (self.material_property.fy * k**2)) ** 0.33,-1)),self.section_property.depth_web/k)) + count * 5
    def optimum_depth_thickness_web(self,func,var_list):
        print('depth & web_thickness0',self.section_property.depth_web, self.section_property.web_thickness)
        while True:
            check = []
            for j in var_list:
                check.append(func(self,j))
            # check3 = self.checks(self,type=3)
            # print('depth & web_thickness before',self.section_property.depth_web, self.section_property.web_thickness,'check',all(check))
            if self.section_property.depth_web % 5 != 0 or self.section_property.web_thickness % 5 !=0:
                self.section_property.depth_web=self.myround(self.section_property.depth_web,5,'low')
                self.section_property.web_thickness = self.myround(self.section_property.web_thickness,5,'high')
            print('depth & web_thickness after',self.section_property.depth_web, self.section_property.web_thickness)

            if all(check):
                print('depth & web_thickness1',self.section_property.depth_web, self.section_property.web_thickness)
            # self.section_classification(self)
            # print("self.section_class_girder",self.section_class_girder)
                break
            else :
                print('depth & web_thickness2',self.section_property.depth_web, self.section_property.web_thickness)
                if i%2==1:
                    self.section_property.depth_web -= 10
                else:
                    self.section_property.web_thickness += 10
                continue
    def optimum_depth_thickness_flange(self, var):
        if self.section_class_req == "Plastic":
            self.section_property.flange_thickness = self.myround(self.section_property.flange_width / (2 * 8.4 * self.epsilon),5,'high') + var * 5
        elif self.section_class_req == "Compact":
            self.section_property.flange_thickness = self.myround(self.section_property.flange_width / (2 * 9.4 * self.epsilon),5,'high') + var * 5
        else: #Semi-Compact
            self.section_property.flange_thickness = math.ceil(myround(self.section_property.flange_width / (2 * 13.6 * self.epsilon),5,'high')) + var * 5
        print(self.section_property.flange_thickness, self.section_property.flange_width)

    def checks(self,type):
        # print('depth & web_thickness',self.section_property.depth_web, self.section_property.web_thickness)
        if type == 1:
            if self.web_type_needed == "Thick": # CL 8.4.2.1
                if not self.web_siffened:
                     self.single_section_dictionary['Web_Shear_Buckling_validator'] = IS800_2007.cl_8_4_2_1_web_buckling_stiff(self.section_property.depth_web, self.section_property.web_thickness,self.epsilon,1)
                else:
                     self.single_section_dictionary['Web_Shear_Buckling_validator'] = IS800_2007.cl_8_4_2_1_web_buckling_stiff(self.section_property.depth_web, self.section_property.web_thickness,self.epsilon,2, self.single_section_dictionary['Kv'])
            else:
                self.section_property.web_thickness = self.myround(self.section_property.depth_web / (67 * self.epsilon),10,'high')#math.ceil()
                print(self.section_property.depth_web / (67 * self.epsilon),'new web_thickness', self.section_property.web_thickness)
                return True
        elif type == 2:
            print('ratio 2', self.section_property.depth_web/self.section_property.web_thickness)
            if self.servicibility_check:
                return True if self.section_property.depth_web/self.section_property.web_thickness < 200 * self.epsilon else False
            # TODO No transverse stiffener web connected to flanges along both longitudinal edges CL 8.6.1.1
        elif type == 3:
            print('ratio 3', self.section_property.depth_web/self.section_property.web_thickness)
            if self.compression_flange_buckling:
                return True if self.section_property.depth_web / self.section_property.web_thickness <= 345 * self.epsilon**2 else False
        elif type == 4:
            ic('check 4', self.shear_strength,self.load.shear_force )
            return True if self.shear_strength > self.load.shear_force  else False

    def section_classification(self):
        self.web_class_list = IS800_2007.Table2_i(
            (self.section_property.flange_width - self.section_property.web_thickness) / 2,
            self.section_property.flange_thickness,
            self.material_property.fy, self.section_property.type
        )
        self.flange_class_list = ['Plastic',0]
        # IS800_2007.Table2_i(
        #     self.section_property.depth_web ,
        #     self.section_property.web_thickness,
        #     self.material_property.fy, self.section_property.type
        # )
        self.web_class = self.web_class_list[0]
        self.flange_class = self.flange_class_list[0]
        if self.flange_class == "Slender" or self.web_class == "Slender":
            self.section_class_girder = "Slender"
        else:
            if self.flange_class == "Plastic" and self.web_class == "Plastic":
                self.section_class_girder = "Plastic"
            elif self.flange_class == "Plastic" and self.web_class == "Compact":
                self.section_class_girder = "Compact"
            elif self.flange_class == "Plastic" and self.web_class == "Semi-Compact":
                self.section_class_girder = "Semi-Compact"
            elif self.flange_class == "Compact" and self.web_class == "Plastic":
                self.section_class_girder = "Compact"
            elif self.flange_class == "Compact" and self.web_class == "Compact":
                self.section_class_girder = "Compact"
            elif self.flange_class == "Compact" and self.web_class == "Semi-Compact":
                self.section_class_girder = "Semi-Compact"
            elif self.flange_class == "Semi-Compact" and self.web_class == "Plastic":
                self.section_class_girder = "Semi-Compact"
            elif self.flange_class == "Semi-Compact" and self.web_class == "Compact":
                self.section_class_girder = "Semi-Compact"
            elif self.flange_class == "Semi-Compact" and self.web_class == "Semi-Compact":
                self.section_class_girder = "Semi-Compact"
        print(self.web_class_list,self.flange_class_list,self.section_class_girder)
        return (('web_class',self.web_class),('flange_class',self.flange_class),('section_class_girder',self.section_class_girder),('Class Ratio',self.web_class_list[1]))

    def Shear_Strength(self):
        self.V_d = IS800_2007.cl_8_4_design_shear_strength(
            ic(self.section_property.shear_area),
            ic(self.material_property.fy)
        ) / 10 ** 3
        self.shear_strength = self.myround(self.V_d,5,'low')
    def plate_girder_strength(self):
        Flexure.plate_girder_strength(self)

        # self.shear_strength = self.myround(self.V_d,5,'low')
    def bending_strength_girder(self):
        # print('Inside bending_strength of girder ')
        # web_class = IS800_2007.Table2_i(
        #     (self.section_property.flange_width - self.section_property.web_thickness)/2,
        #     self.section_property.flange_thickness,
        #     self.material_property.fy, self.section_property.type
        # )[0]
        # flange_class = IS800_2007.Table2_i(
        #     self.section_property.depth - 2 * self.section_property.flange_thickness,
        #     self.section_property.web_thickness,
        #     self.material_property.fy,self.section_property.type
        # )[0]
        # if flange_class == "Slender" or web_class == "Slender":
        #     self.section_class_girder = "Slender"
        # else:
        #     if flange_class == "Plastic" and web_class == "Plastic":
        #         self.section_class_girder = "Plastic"
        #     elif flange_class == "Plastic" and web_class == "Compact":
        #         self.section_class_girder = "Compact"
        #     elif flange_class == "Plastic" and web_class == "Semi-Compact":
        #         self.section_class_girder = "Semi-Compact"
        #     elif flange_class == "Compact" and web_class == "Plastic":
        #         self.section_class_girder = "Compact"
        #     elif flange_class == "Compact" and web_class == "Compact":
        #         self.section_class_girder = "Compact"
        #     elif flange_class == "Compact" and web_class == "Semi-Compact":
        #         self.section_class_girder = "Semi-Compact"
        #     elif flange_class == "Semi-Compact" and web_class == "Plastic":
        #         self.section_class_girder = "Semi-Compact"
        #     elif flange_class == "Semi-Compact" and web_class == "Compact":
        #         self.section_class_girder = "Semi-Compact"
        #     elif flange_class == "Semi-Compact" and web_class == "Semi-Compact":
        #         self.section_class_girder = "Semi-Compact"
        # 4 - design bending strength
        I_flange = 2 * (self.section_property.flange_width * self.section_property.flange_thickness**3/12 + self.section_property.flange_width * self.section_property.flange_thickness * (self.section_property.depth/2 - self.section_property.flange_thickness/2)**2)
        Zez_flange = I_flange / self.section_property.depth /2
        y_top = (self.section_property.flange_width * self.section_property.flange_thickness * (self.section_property.depth - self.section_property.flange_thickness)/2) / (self.section_property.flange_width * self.section_property.flange_thickness)
        Zpz_flange = 2 * self.section_property.flange_width * self.section_property.flange_thickness * y_top
        M_d = IS800_2007.cl_8_2_1_2_design_bending_strength(
            self.section_class_girder,
            Zpz_flange,
            Zez_flange,
            self.material_property.fy,
            self.gamma_m0,
            self.support,
        )
        if self.section_class_girder == 'Plastic' or 'Compact' :
            self.beta_b_lt = 1
        else :            self.beta_b_lt = Zez_flange/Zpz_flange
        self.M_d = M_d
        if self.design_type == KEY_DISP_DESIGN_TYPE_FLEXURE:
            if self.high_shear_check:
                if self.section_class_girder == "Plastic" or self.section_class_girder == "Compact":
                    bending_strength_section
                    # TODO = self.bending_strength_reduction(self, M_d)
                else:
                    bending_strength_section = (
                        self.section_property.elast_sec_mod_z
                        * self.material_property.fy
                        / self.gamma_m0
                    )
            else:
                bending_strength_section = M_d
            print('Inside bending_strength 1', M_d, self.high_shear_check, bending_strength_section)
        else:
            # self.It = (
            #     2
            #     * self.section_property.flange_width
            #     * self.section_property.flange_thickness**3
            # ) / 3 + (
            #     (self.section_property.depth - self.section_property.flange_thickness)
            #     * self.section_property.web_thickness**3
            # ) / 3
            self.hf = self.section_property.depth - self.section_property.flange_thickness
            # self.Iw = 0.5**2 * self.section_property.mom_inertia_y * self.hf**2
            self.fcrb = IS800_2007.cl_8_2_2_Unsupported_beam_bending_fcrb(
                self.material_property.modulus_of_elasticity,
                self.effective_length/self.section_property.rad_of_gy_y,
                self.hf/self.section_property.flange_thickness
            )

            if self.section_class_girder == "Plastic" or self.section_class_girder == "Compact":
                self.beta_b_lt = 1.0
            else:
                self.beta_b_lt = (
                    self.section_property.elast_sec_mod_z
                    / self.section_property.plast_sec_mod_z
                )
            if self.section_property.type == "Rolled":
                alpha_lt = 0.21
            else:
                alpha_lt = 0.49
            lambda_lt = IS800_2007.cl_8_2_2_1_elastic_buckling_moment_fcrb(
                self.material_property.fy, self.fcrb
            )
            phi_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_phi_lt(
                alpha_lt, lambda_lt
            )
            X_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_stress_reduction_factor(
                phi_lt, lambda_lt
            )
            fbd = IS800_2007.cl_8_2_2_Unsupported_beam_bending_compressive_stress(
                X_lt, self.material_property.fy, self.gamma_m0
            )
            bending_strength_section = IS800_2007.cl_8_2_2_Unsupported_beam_bending_strength(
                    self.section_property.plast_sec_mod_z,
                    self.section_property.elast_sec_mod_z,
                    fcd=fbd,
                    section_class=self.section_class_girder
                )


            # self.beta_b_lt = beta_b
            self.alpha_lt = alpha_lt
            # self.lambda_lt = lambda_lt
            self.phi_lt = phi_lt
            self.X_lt = X_lt
            self.fbd_lt = fbd
            self.lateral_tb = self.fcrb * 10**-6
            print('Inside bending_strength 2.1', fbd, self.section_property.plast_sec_mod_z )
            if self.high_shear_check:
                if self.section_class_girder == "Plastic" or self.section_class_girder == "Compact":
                    bending_strength_section = self.bending_strength_reduction(self,Md=bending_strength_section
                    )
                else:
                    bending_strength_section = (
                        self.beta_b_lt
                        * self.section_property.plast_sec_mod_z
                        * fbd
                    )
            print('Inside bending_strength 2',It,self.hf,self.Iw,self.fcrb ,self.beta_b_lt,alpha_lt,lambda_lt,phi_lt,X_lt,fbd,bending_strength_section)
        self.bending_strength_section_reduced = bending_strength_section
        return bending_strength_section

    def plate_girder_strength(self):
        Flexure.plate_girder_strength(self)
    def plate_girder_strength2(self):
        Flexure.plate_girder_strength2(self)
    def myround(x, base,type):
        if type == 'high':
            return base * math.ceil(x / base)
        else:
            return base * round(x / base)


    def section_check_validator(self,var1,var2,var3):
        if var1 == var2:
            self.section_list = [True]
            self.Girder_SectionProperty(self, self.designed_dict,False) # var3 = design_dictionary
        check_list = []
        while var1 and (len(check_list)== 0 or all(check_list)):
            self.Shear_Strength(self)
            ic(check_list.append( self.checks(self,4)))

            var1 = var2
            break

    def results(self, design_dictionary):

        # sorting results from the dataset
        # if len(self.input_section_list) > 1:
        # results based on UR
        self.common_result(self,self.section_list,"NA")
        self.design_status = True

        return 0

        if self.optimization_parameter == "Utilization Ratio":
            filter_UR = filter(
                lambda x: x <= min(self.allowable_utilization_ratio, 1.0),
                self.optimum_section_ur
            )
            self.optimum_section_ur = list(filter_UR)

            self.optimum_section_ur.sort()
            # print(f"self.optimum_section_ur{self.optimum_section_ur}")
            # print(f"self.result_UR{self.result_UR}")

            # selecting the section with most optimum UR
            if len(self.optimum_section_ur) == 0:  # no design was successful
                logger.warning(
                    "The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
                    "criteria"
                )
                logger.error(
                    "The solver did not find any adequate section from the defined list."
                )
                logger.info(
                    "Re-define the list of sections or check the Design Preferences option and re-design."
                )
                self.design_status = False
                # self.design_status_list.append(self.design_status)

            else:
                self.result_UR = self.optimum_section_ur[
                    -1
                ]  # optimum section which passes the UR check
                print(f"self.result_UR{self.result_UR}")
                self.design_status = True
                # self.common_result(
                #     self,
                #     list_result=self.optimum_section_ur_results,
                #     result_type=self.result_UR,
                # )

        else:  # results based on cost
            self.optimum_section_cost.sort()

            # selecting the section with most optimum cost
            self.result_cost = self.optimum_section_cost[0]
            self.design_status = True

        self.design_status_list.append(self.design_status)
        for status in self.design_status_list:
            print('status list', status)
            if status is False:
                self.design_status = False
                break
            else:
                self.design_status = True
    def common_result(self, list_result, result_type, flag=1):
        # self.result_designation = list_result[result_type]["Designation"]
        ic()
        # TODO take dictionary of most optmised output and add here
        self.result_tf =  self.section_property.flange_thickness
        self.result_tw = self.section_property.web_thickness
        self.result_dw = self.section_property.depth_web
        self.result_bf = self.section_property.flange_width
        self.shear_strength = self.single_section_dictionary['Shear_Strength']

        try:
            self.result_shear = self.shear_strength
            self.result_bending = "NA"
        except:
            self.result_shear = "NA"
            self.result_bending = "NA"

    def list_changer(self, change, list,list_name, check = True):
        list_name.extend([
            "Designation"])
        list.extend(
            [self.result_tf,
        self.result_tw,
        self.result_dw,
        self.result_bf])
        list_name.extend([
                "Mfd",
                "Beta_reduced",
                'M_d'
            ])

    ### start writing save_design from here!
    def save_design(self, popup_summary):

        self.report_input = \
            {#KEY_MAIN_MODULE: self.mainmodule,
                KEY_MODULE: self.module, #"Axial load on column "
            }

        print(sys.path[0])
        rel_path = str(sys.path[0])
        rel_path = "." # TEMP
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']
        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                              rel_path, [], '', module=self.module) #
