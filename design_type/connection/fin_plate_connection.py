from design_type.connection.shear_connection import ShearConnection

from utils.common.component import Bolt, Plate, Weld
# from gui.ui_summary_popup import Ui_Dialog
from utils.common.component import *
from utils.common.material import *
from Common import *
from utils.common.load import Load
import yaml
from design_report.reportGenerator import save_html
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
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog,QMessageBox
import pickle
import pdfkit
import configparser
import cairosvg
from io import StringIO




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
material_grade = "E 250 (Fe 410 W)B"
material = Material(material_grade)

def desired_location(self, filename, base_type):
    if base_type == ".svg":
        cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.maincontroller.folder), "images_html",
                                                                  "cmpylogoExtendEndplate.svg"))
    else:
        shutil.copyfile(filename,
                        os.path.join(str(self.maincontroller.folder), "images_html", "cmpylogoExtendEndplate.png"))

def saveUserProfile(self):
    inputData = self.get_report_summary()
    filename, _ = QFileDialog.getSaveFileName(self, 'Save Files',
                                              os.path.join(str(self.maincontroller.folder), "Profile"), '*.txt')
    if filename == '':
        flag = False
        return flag
    else:
        infile = open(filename, 'w')
        pickle.dump(inputData, infile)
        infile.close()


def getPopUpInputs(self):
    input_summary = {}
    input_summary["ProfileSummary"] = {}
    input_summary["ProfileSummary"]["CompanyName"] = str(self.ui.lineEdit_companyName.text())
    input_summary["ProfileSummary"]["CompanyLogo"] = str(self.ui.lbl_browse.text())
    input_summary["ProfileSummary"]["Group/TeamName"] = str(self.ui.lineEdit_groupName.text())
    input_summary["ProfileSummary"]["Designer"] = str(self.ui.lineEdit_designer.text())

    input_summary["ProjectTitle"] = str(self.ui.lineEdit_projectTitle.text())
    input_summary["Subtitle"] = str(self.ui.lineEdit_subtitle.text())
    input_summary["JobNumber"] = str(self.ui.lineEdit_jobNumber.text())
    input_summary["AdditionalComments"] = str(self.ui.txt_additionalComments.toPlainText())
    input_summary["Client"] = str(self.ui.lineEdit_client.text())


def useUserProfile(self):
    filename, _ = QFileDialog.getOpenFileName(self, 'Open Files',
                                              os.path.join(str(self.maincontroller.folder), "Profile"),
                                              "All Files (*)")
    if os.path.isfile(filename):
        outfile = open(filename, 'r')
        reportsummary = pickle.load(outfile)
        self.ui.lineEdit_companyName.setText(reportsummary["ProfileSummary"]['CompanyName'])
        self.ui.lbl_browse.setText(reportsummary["ProfileSummary"]['CompanyLogo'])
        self.ui.lineEdit_groupName.setText(reportsummary["ProfileSummary"]['Group/TeamName'])
        self.ui.lineEdit_designer.setText(reportsummary["ProfileSummary"]['Designer'])
    else:
        pass


class FinPlateConnection(ShearConnection):


    def __init__(self):
        super(FinPlateConnection, self).__init__()

    def set_osdaglogger(key):
        global logger
        logger = logging.getLogger('osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        handler.setLevel(logging.WARNING)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = OurLog(key)
        handler.setLevel(logging.WARNING)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)


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

        t3 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, existingvalue_key_suptngsec, connectdb("Columns"))
        options_list.append(t3)

        t4 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, existingvalue_key_suptdsec, connectdb("Beams"))
        options_list.append(t4)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL)
        options_list.append(t5)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None)
        options_list.append(t6)

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

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, None)
        options_list.append(t13)

        t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_platethk, VALUES_PLATETHK)
        options_list.append(t14)

        return options_list

    def output_values(self, flag):

        out_list = []

        t1 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None)
        out_list.append(t1)

        t2 = (KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX,  self.bolt.bolt_diameter_provided if flag == 'True' else '')
        out_list.append(t2)

        t3 = (KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_GRD_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_grade_provided if flag == 'True' else '')
        out_list.append(t3)

        t4 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,  round(self.bolt.bolt_shear_capacity/1000,2) if flag == 'True' else '')
        out_list.append(t4)

        t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, round(self.bolt.bolt_bearing_capacity/1000,2) if flag == 'True' else '')
        out_list.append(t5)

        t6 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX, round(self.bolt.bolt_capacity/1000,2) if flag == 'True' else '')
        out_list.append(t6)

        t21 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_FORCE, TYPE_TEXTBOX, round(self.plate.bolt_force / 1000, 2) if flag == 'True' else '')
        out_list.append(t21)

        t7 = (KEY_OUT_BOLT_LINE, KEY_OUT_DISP_BOLT_LINE, TYPE_TEXTBOX, self.plate.bolt_line if flag == 'True' else '')
        out_list.append(t7)

        t8 = (KEY_OUT_BOLTS_ONE_LINE, KEY_OUT_DISP_BOLTS_ONE_LINE, TYPE_TEXTBOX, self.plate.bolts_one_line if flag == 'True' else '')
        out_list.append(t8)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.plate.pitch_provided if flag == 'True' else '')
        out_list.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.plate.end_dist_provided if flag == 'True' else '')
        out_list.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.plate.gauge_provided if flag == 'True' else '')
        out_list.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.plate.edge_dist_provided if flag == 'True' else '')
        out_list.append(t12)

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None)
        out_list.append(t13)

        t14 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX, self.plate.thickness_provided if flag == 'True' else '')
        out_list.append(t14)

        t15 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_HEIGHT, TYPE_TEXTBOX, self.plate.height if flag == 'True' else '')
        out_list.append(t15)

        t16 = (KEY_OUT_PLATE_LENGTH, KEY_OUT_DISP_PLATE_LENGTH, TYPE_TEXTBOX, self.plate.length if flag == 'True' else '')
        out_list.append(t16)

        t17 = (KEY_OUT_PLATE_SHEAR, KEY_OUT_DISP_PLATE_SHEAR, TYPE_TEXTBOX, round(self.plate.shear_yielding_capacity,2) if flag == 'True' else '')
        out_list.append(t17)

        t18 = (KEY_OUT_PLATE_BLK_SHEAR, KEY_OUT_DISP_PLATE_BLK_SHEAR, TYPE_TEXTBOX, round(self.plate.block_shear_capacity,2) if flag == 'True' else '')
        out_list.append(t18)

        t19 = (KEY_OUT_PLATE_MOM_DEMAND, KEY_OUT_DISP_PLATE_MOM_DEMAND, TYPE_TEXTBOX, round(self.plate.moment_demand/1000000,2) if flag == 'True' else '')
        out_list.append(t19)

        t20 = (KEY_OUT_PLATE_MOM_CAPACITY, KEY_OUT_DISP_PLATE_MOM_CAPACITY, TYPE_TEXTBOX, round(self.plate.moment_capacity,2) if flag == 'True' else '')
        out_list.append(t20)

        return out_list

    def warn_text(self):
        red_list = red_list_function()
        if self.supported_section.designation in red_list or self.supporting_section.designation in red_list:
            logger.warning(
                " : You are using a section (in red color) that is not available in latest version of IS 808")

    def set_input_values(self, design_dictionary):
        super(FinPlateConnection,self).set_input_values(self, design_dictionary)
        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None),
                           material_grade=design_dictionary[KEY_MATERIAL], gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.member_capacity(self)

    def member_capacity(self):
        # print(KEY_CONN,VALUES_CONN_1,self.supported_section.build)
        if self.connectivity in VALUES_CONN_1:
            if self.supported_section.build == "Rolled":
                length = self.supported_section.depth
            else:
                length = self.supported_section.depth - (2*self.supported_section.flange_thickness)    # -(2*self.supported_section.root_radius)
        else:
            length = self.supported_section.depth - 50.0  # TODO: Subtract notch height for beam-beam connection

        self.supported_section.shear_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)
        self.supported_section.tension_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)

        print(self.supported_section.shear_yielding_capacity, self.load.shear_force,
              self.supported_section.tension_yielding_capacity, self.load.axial_force)

        if self.supported_section.shear_yielding_capacity > self.load.shear_force and \
                self.supported_section.tension_yielding_capacity > self.load.axial_force:
            self.get_bolt_details(self)
        else:
            logger.error(" : shear yielding capacity {} and/or tension yielding capacity {} is less "
                           "than applied loads, Please select larger sections or decrease loads"
                            .format(self.supported_section.shear_yielding_capacity,
                                    self.supported_section.tension_yielding_capacity))

    def get_bolt_details(self):

        min_plate_height = self.supported_section.min_plate_height()
        max_plate_height = self.supported_section.max_plate_height()
        self.plate.thickness_provided = round_up(self.supported_section.web_thickness, 2)
        bolts_required_previous = 2
        bolt_diameter_previous = self.bolt.bolt_diameter[-1]
        bolt_grade_previous = self.bolt.bolt_grade[-1]
        res_force = math.sqrt(self.load.shear_force ** 2 + self.load.axial_force ** 2) * 1000
        self.bolt.bolt_grade_provided = self.bolt.bolt_grade[-1]
        count = 0
        for self.bolt.bolt_diameter_provided in reversed(self.bolt.bolt_diameter):
            self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                    connecting_plates_tk=[self.plate.thickness_provided,
                                                                          self.supported_section.web_thickness])

            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              connecting_plates_tk=[self.plate.thickness_provided,
                                                                    self.supported_section.web_thickness],
                                              n_planes=1)

            self.plate.bolts_required = max(int(math.ceil(res_force / self.bolt.bolt_capacity)), 2)

            if self.plate.bolts_required > bolts_required_previous and count >= 1:
                self.bolt.bolt_diameter_provided = bolt_diameter_previous
                self.plate.bolts_required = bolts_required_previous
                break
            bolts_required_previous = self.plate.bolts_required
            bolt_diameter_previous = self.bolt.bolt_diameter_provided
            count += 1

        bolts_required_previous = self.plate.bolts_required

        for self.bolt.bolt_grade_provided in reversed(self.bolt.bolt_grade):
            count = 1
            self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                    connecting_plates_tk=[self.plate.thickness_provided,
                                                                          self.supported_section.web_thickness])

            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              connecting_plates_tk=[self.plate.thickness_provided,
                                                                    self.supported_section.web_thickness],
                                              n_planes=1)

            self.plate.bolts_required = max(int(math.ceil(res_force / self.bolt.bolt_capacity)), 2)

            if self.plate.bolts_required > bolts_required_previous and count >= 1:
                self.bolt.bolt_grade_provided = bolt_grade_previous
                self.plate.bolts_required = bolts_required_previous
                break
            bolts_required_previous = self.plate.bolts_required
            bolt_grade_previous = self.bolt.bolt_grade_provided
            count += 1

        self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                connecting_plates_tk=[self.plate.thickness_provided,
                                                                      self.supported_section.web_thickness])

        self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                          bolt_grade_provided=self.bolt.bolt_grade_provided,
                                          connecting_plates_tk=[self.plate.thickness_provided,
                                                                self.supported_section.web_thickness],
                                          n_planes=1)

        self.plate.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                         web_plate_h_min=min_plate_height, web_plate_h_max=max_plate_height,
                                         bolt_capacity=self.bolt.bolt_capacity,
                                         min_edge_dist=self.bolt.min_edge_dist_round,
                                         min_gauge=self.bolt.min_gauge_round, max_spacing=self.bolt.max_spacing_round,
                                         max_edge_dist=self.bolt.max_edge_dist_round, shear_load=self.load.shear_force*1000,
                                         axial_load=self.load.axial_force*1000, gap=self.plate.gap,
                                         shear_ecc=True)

        edge_dist_rem = self.plate.edge_dist_provided+self.plate.gap

        #################################
        # Block Shear Check for supporting section
        #################################
        design_status_block_shear = False
        while design_status_block_shear is False:
            # print(design_status_block_shear)
            # print(0, self.web_plate.max_end_dist, self.web_plate.end_dist_provided, self.web_plate.max_spacing_round, self.web_plate.pitch_provided)
            Avg_a = 2 * (self.plate.end_dist_provided + self.plate.gap + (self.plate.bolt_line - 1) * self.plate.pitch_provided)\
                    * self.supporting_section.web_thickness
            Avn_a = 2 * (self.plate.end_dist_provided + (self.plate.bolt_line - 1) * self.plate.pitch_provided
                     - (self.plate.bolt_line - 0.5) * self.bolt.dia_hole) * self.supporting_section.web_thickness

            Atg_a = ((self.plate.bolts_one_line - 1) * self.plate.pitch_provided)\
                    * self.supporting_section.thickness_provided
            Atn_a = ((self.plate.bolts_one_line - 1) * self.plate.pitch_provided -
                     (self.plate.bolt_line - 1) * self.bolt.dia_hole) * \
                    self.supporting_section.web_thickness

            Avg_s = (self.plate.edge_dist_provided + (self.plate.bolts_one_line - 1) * self.plate.gauge_provided)\
                    * self.supporting_section.web_thickness
            Avn_s = ((self.plate.edge_dist_provided + (self.plate.bolts_one_line - 1) * self.plate.gauge_provided)
                     - (self.plate.bolts_one_line - 0.5) * self.bolt.dia_hole) * self.supporting_section.web_thickness

            Atg_s = ((self.plate.bolt_line - 1) * self.plate.pitch_provided + self.plate.end_dist_provided + self.plate.gap)\
                    * self.supporting_section.thickness_provided
            Atn_s = ((self.plate.bolt_line - 1) * self.plate.pitch_provided -
                     (self.plate.bolt_line - 0.5) * self.bolt.dia_hole + self.plate.end_dist_provided + self.plate.gap) * \
                    self.supporting_section.web_thickness

            self.supporting_section.block_shear_capacity_axial = self.block_shear_strength_section(A_vg=Avg_a, A_vn=Avn_a, A_tg=Atg_a,
                                                                                    A_tn=Atn_a,
                                                                                    f_u=self.supporting_section.fu,
                                                                                    f_y=self.supporting_section.fy)

            self.supporting_section.block_shear_capacity_shear = self.block_shear_strength_section(A_vg=Avg_s, A_vn=Avn_s, A_tg=Atg_s,
                                                                                    A_tn=Atn_s,
                                                                                    f_u=self.supporting_section.fu,
                                                                                    f_y=self.supporting_section.fy)

            if self.supporting_section.block_shear_capacity < self.load.axial_force:
                if self.bolt.max_spacing_round >= self.plate.pitch_provided + 5 and self.bolt.max_end_dist >= self.plate.end_dist_provided + 5:  # increase thickness todo
                    if self.plate.bolt_line == 1:
                        self.plate.end_dist_provided += 5
                    else:
                        self.plate.pitch_provided += 5
                else:
                    design_status_block_shear = False
            else:
                design_status_block_shear = True

        self.plate.blockshear(numrow=self.plate.bolts_one_line, numcol=self.plate.bolt_line, pitch=self.plate.pitch_provided,
                              gauge=self.plate.gauge_provided, thk=self.plate.thickness[0], end_dist=self.plate.end_dist_provided,
                              edge_dist=edge_dist_rem, dia_hole=self.bolt.dia_hole,
                              fy=self.supported_section.fy, fu=self.supported_section.fu)

        self.plate.shear_yielding(self.plate.height, self.plate.thickness[0], self.plate.fy)

        self.plate.shear_rupture_b(self.plate.height, self.plate.thickness[0], self.plate.bolts_one_line,
                                       self.bolt.dia_hole, self.plate.fu)

        plate_shear_capacity = min(self.plate.block_shear_capacity, self.plate.shear_rupture_capacity,
                                   self.plate.shear_yielding_capacity)

        # if self.load.shear_force > plate_shear_capacity:
        #     design_status = False
        #     logger.error(":shear capacity of the plate is less than the applied shear force, %2.2f kN [cl. 6.4.1]"
        #                  % self.load.shear_force)
        #     logger.warning(":Shear capacity of plate is %2.2f kN" % plate_shear_capacity)
        #     logger.info(": Increase the plate thickness")

        self.plate.get_moment_cacacity(self.plate.fy, self.plate.thickness[0], self.plate.height)

        # if self.plate.moment_capacity < self.plate.moment_demand:
        #     design_status = False
        #     logger.error(": Plate moment capacity is less than the moment demand [cl. 8.2.1.2]")
        #     logger.warning(": Re-design with increased plate dimensions")

        print(self.connectivity)
        print(self.supporting_section)
        print(self.supported_section)
        print(self.load)
        print(self.bolt)
        print(self.plate)

    def block_shear_strength_section(self, A_vg, A_vn, A_tg, A_tn, f_u, f_y):
        """Calculate the block shear strength of bolted connections as per cl. 6.4.1

        Args:
            A_vg: Minimum gross area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_vn: Minimum net area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_tg: Minimum gross area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            A_tn: Minimum net area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            f_u: Ultimate stress of the plate material in MPa (float)
            f_y: Yield stress of the plate material in MPa (float)

        Return:
            block shear strength of bolted connection in N (float)

        Note:
            Reference:
            IS 800:2007, cl. 6.4.1

        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_db1 = A_vg * f_y / (math.sqrt(3) * gamma_m0) + 0.9 * A_tn * f_u / gamma_m1
        T_db2 = 0.9 * A_vn * f_u / (math.sqrt(3) * gamma_m1) + A_tg * f_y / gamma_m0
        Tdb = min(T_db1, T_db2)
        Tdb = round(Tdb / 1000, 3)
        return Tdb
