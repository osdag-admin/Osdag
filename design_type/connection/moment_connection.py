from design_type.connection.connection import Connection
from utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column
from Common import *
from utils.common.load import Load
from utils.common import common_calculation
import numpy as np

from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap, QPalette
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog
import pickle
import logging
import cmath


class MomentConnection(Connection):
    def __init__(self):
        super(MomentConnection, self).__init__()

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

    @staticmethod
    def plate_thick_customized():
        f = VALUES_PLATETHICKNESS_CUSTOMIZED
        return f
    @staticmethod
    def endplate_thick_customized():
        d = VALUES_ENDPLATE_THICKNESS_CUSTOMIZED
        return d
    def customized_input(self):

        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)
        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)
        t4 = (KEY_WEBPLATE_THICKNESS, self.plate_thick_customized)
        list1.append(t4)
        t5 = (KEY_FLANGEPLATE_THICKNESS, self.plate_thick_customized)
        list1.append(t5)


        return list1
    def set_input_values(self, design_dictionary):
        self.mainmodule = "Moment Connection"
        self.load = Load(shear_force=design_dictionary[KEY_SHEAR], axial_force=design_dictionary.get(KEY_AXIAL, None),
                         moment=design_dictionary[KEY_MOMENT])

    def get_bolt_details(self):
        pass


    def warn_text(self):
        pass
        # old_col_section = get_oldcolumncombolist()
        # old_beam_section = get_oldbeamcombolist()
        #
        # if my_d[KEY_SECSIZE] in old_beam_section or old_col_section:
        #     del_data = open('logging_text.log', 'w')
        #     del_data.truncate()
        #     del_data.close()
        #     logging.basicConfig(format='%(asctime)s %(message)s', filename='logging_text.log',level=logging.DEBUG)
        #     logging.warning(" : You are using a section (in red color) that is not available in latest version of IS 808")
        #     with open('logging_text.log') as file:
        #         data = file.read()
        #         file.close()
        #     # file = open('logging_text.log', 'r')
        #     # # This will print every line one by one in the file
        #     # for each in file:
        #     #     print(each)
        #     key.setText(data)
        # else:
        #     key.setText("")


    def input_value_changed(self):
        pass

    def web_force(column_d, column_f_t, column_t_w, factored_axial_force, column_area):
        pass

    def block_shear_strength_plate(A_vg, A_vn, A_tg, A_tn, f_u, f_y):
        pass

    def block_shear_strength_section(A_vg, A_vn, A_tg, A_tn, f_u, f_y):
        pass

    def tension_member_design_due_to_yielding_of_gross_section(A_v, fy):
        pass

    def tension_member_design_due_to_rupture_of_critical_section(A_vn, fu):
        pass

    # Base Plate module
    @staticmethod
    def calculate_c(flange_width, depth, web_thickness, flange_thickness, min_area_req, anchor_hole_dia):
        """ calculate the 'projection' based on the Effective Area Method for rolled and welded columns only.

        Args:
            flange_width (float) - flange width of the column section (bf)
            depth (float) - depth of the column section (h)
            web_thickness (float) - web thickness of the column section (tw)
            flange_thickness (float) - flange thickness of the column section (tf)
            min_area_req (float) - minimum effective bearing area (A_bc)
            anchor_hole_dia (int) - diameter of the anchor hole

        Returns: projection in 'mm' (float)

        Note: 1) The following expression is used to calculate a, b and c [Ref: Design of Steel Structures,
                 N. Subramanian, 2nd. edition 2018, Example 15.2]:
                 A_bc = (bf + 2c) (h + 2c) - [{h - 2(tf + c)}(bf - tw)]

              2) Adding anchor hole diameter (half on each side) to the value of the projection to avoid punching
                 of the hole in the effective area which in turn shall avoid any stress concentration
        """
        a = 4
        b = (4 * flange_width) + (2 * depth) - (2 * web_thickness)
        c = (2 * flange_thickness * flange_width) + (depth * web_thickness) + (2 * flange_thickness * web_thickness)\
            - min_area_req

        roots = np.roots([a, b, c])  # finding roots of the equation
        r_1 = roots[0]
        r_2 = roots[1]
        r = max(r_1, r_2)  # picking the highest positive value from the roots

        projection = common_calculation.round_up(r + anchor_hole_dia, 5)  # mm

        return projection


