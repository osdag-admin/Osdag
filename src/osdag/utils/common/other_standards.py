"""Module for Indian Standards other than IS 800 : 2007

Included standards,
    IS 1363 - Part 1 : 2002
    IS 1363 - Part 3 : 2002
    IS 1367 - Part 3 : 2002
    IS 3757 : 1985
    IS 6623 : 2004
    IS 5624:1993, Foundation Bolts - Specification

Started on 15 - Nov - 2018

@author: ajmalbabums, Danish Ansari, Sourabh Das
"""
import sqlite3
import math
import os
import sys
PATH_TO_DATABASE = os.path.join(sys.path[0],'ResourceFiles','Database','Intg_osdag.sqlite')




# IS 1363 - Part 1 : 2002
class IS1363_part_1_2002(object):
    """Perform calculations as per IS 1363 (Part 1) : 2002 [ISO 4016: 1999]
    Hexagon head bolts, screws, and nuts of product grade C
    Part 1 : Hexagon head bolts (size M5 to M64)
    """

    # Dimensions of Metric bolts as per Table 1 and 2 of IS 1363(Part-1) :2002 (dict)
    bolt_dimensions = {
        5: {'pitch': 0.80, 'head_thick': 3.5, 'head_diag': 8.630, 'head_dia': 8.0, 'thread': "preferred"},
        6: {'pitch': 1.00, 'head_thick': 4.0, 'head_diag': 10.890, 'head_dia': 10.0, 'thread': "preferred"},
        8: {'pitch': 1.25, 'head_thick': 5.3, 'head_diag': 14.200, 'head_dia': 13.0, 'thread': "preferred"},
        10: {'pitch': 1.50, 'head_thick': 6.4, 'head_diag': 17.590, 'head_dia': 16.0, 'thread': "preferred"},
        12: {'pitch': 1.75, 'head_thick': 7.5, 'head_diag': 19.850, 'head_dia': 18.0, 'thread': "preferred"},
        16: {'pitch': 2.00, 'head_thick': 10.0, 'head_diag': 26.170, 'head_dia': 24.0, 'thread': "preferred"},
        20: {'pitch': 2.50, 'head_thick': 12.5, 'head_diag': 32.950, 'head_dia': 30.0, 'thread': "preferred"},
        24: {'pitch': 3.00, 'head_thick': 15.0, 'head_diag': 39.550, 'head_dia': 36.0, 'thread': "preferred"},
        30: {'pitch': 3.50, 'head_thick': 18.7, 'head_diag': 50.850, 'head_dia': 46.0, 'thread': "preferred"},
        36: {'pitch': 4.00, 'head_thick': 22.5, 'head_diag': 60.790, 'head_dia': 55.0, 'thread': "preferred"},
        42: {'pitch': 4.50, 'head_thick': 26.0, 'head_diag': 71.300, 'head_dia': 65.0, 'thread': "preferred"},
        48: {'pitch': 5.00, 'head_thick': 30.0, 'head_diag': 82.600, 'head_dia': 75.0, 'thread': "preferred"},
        56: {'pitch': 5.50, 'head_thick': 35.0, 'head_diag': 93.560, 'head_dia': 85.0, 'thread': "preferred"},
        64: {'pitch': 6.00, 'head_thick': 40.0, 'head_diag': 104.86, 'head_dia': 95.0, 'thread': "preferred"},
        14: {'pitch': 2.00, 'head_thick': 8.8, 'head_diag': 22.780, 'head_dia': 21.0, 'thread': "non_preferred"},
        18: {'pitch': 2.50, 'head_thick': 11.5, 'head_diag': 29.560, 'head_dia': 27.0, 'thread': "non_preferred"},
        22: {'pitch': 2.50, 'head_thick': 14.0, 'head_diag': 37.290, 'head_dia': 34.0, 'thread': "non_preferred"},
        27: {'pitch': 3.00, 'head_thick': 17.0, 'head_diag': 45.200, 'head_dia': 41.0, 'thread': "non_preferred"},
        33: {'pitch': 3.50, 'head_thick': 21.0, 'head_diag': 55.370, 'head_dia': 50.0, 'thread': "non_preferred"},
        39: {'pitch': 4.00, 'head_thick': 25.0, 'head_diag': 66.440, 'head_dia': 60.0, 'thread': "non_preferred"},
        45: {'pitch': 4.50, 'head_thick': 28.0, 'head_diag': 76.950, 'head_dia': 70.0, 'thread': "non_preferred"},
        52: {'pitch': 5.00, 'head_thick': 33.0, 'head_diag': 86.250, 'head_dia': 80.0, 'thread': "non_preferred"},
        60: {'pitch': 5.50, 'head_thick': 38.0, 'head_diag': 99.210, 'head_dia': 90.0, 'thread': "non_preferred"}
    }

    # Available lengths of bolts as per Table 1 and 2 of IS 1363(Part-1) :2002 (list)
    # Preferred threads
    bolt_length_preferred = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180,
                             200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500]
    # Non preferred threads
    bolt_length_non_preferred = [60, 65, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200, 220, 240,
                                 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500]


# IS 1363 - Part 3 : 2002
class IS1363_part_3_2002(object):
    """Perform calculations as per IS 1363 (Part 3) : 2002 [ISO 4034: 1999]
    Hexagon head bolts, screws, and nuts of product grade C
    Part 3 : Hexagon nuts (size M5 to M64)
    """

    # Dimensions of Metric nuts as per Table 1 and 2 of IS 1363(Part-3) :2002 (dict)
    nut_dimensions = {
        5: {'pitch': 0.80, 'nut_dia': 8.0, 'nut_diag': 8.630, 'nut_thick_max': 5.6, 'nut_thick_min': 4.4,
            'thread': "preferred"},
        6: {'pitch': 1.00, 'nut_dia': 10.0, 'nut_diag': 10.890, 'nut_thick_max': 6.4, 'nut_thick_min': 4.9,
            'thread': "preferred"},
        8: {'pitch': 1.25, 'nut_dia': 13.0, 'nut_diag': 14.200, 'nut_thick_max': 7.9, 'nut_thick_min': 6.4,
            'thread': "preferred"},
        10: {'pitch': 1.50, 'nut_dia': 16.0, 'nut_diag': 17.590, 'nut_thick_max': 9.5, 'nut_thick_min': 8.0,
             'thread': "preferred"},
        12: {'pitch': 1.75, 'nut_dia': 18.0, 'nut_diag': 19.850, 'nut_thick_max': 12.2, 'nut_thick_min': 10.4,
             'thread': "preferred"},
        16: {'pitch': 2.00, 'nut_dia': 24.0, 'nut_diag': 26.170, 'nut_thick_max': 15.9, 'nut_thick_min': 14.1,
             'thread': "preferred"},
        20: {'pitch': 2.50, 'nut_dia': 30.0, 'nut_diag': 32.950, 'nut_thick_max': 19.0, 'nut_thick_min': 16.9,
             'thread': "preferred"},
        24: {'pitch': 3.00, 'nut_dia': 36.0, 'nut_diag': 39.550, 'nut_thick_max': 22.3, 'nut_thick_min': 20.2,
             'thread': "preferred"},
        30: {'pitch': 3.50, 'nut_dia': 46.0, 'nut_diag': 50.850, 'nut_thick_max': 26.4, 'nut_thick_min': 24.3,
             'thread': "preferred"},
        36: {'pitch': 4.00, 'nut_dia': 55.0, 'nut_diag': 60.790, 'nut_thick_max': 31.9, 'nut_thick_min': 29.4,
             'thread': "preferred"},
        42: {'pitch': 4.50, 'nut_dia': 65.0, 'nut_diag': 71.300, 'nut_thick_max': 34.9, 'nut_thick_min': 32.4,
             'thread': "preferred"},
        48: {'pitch': 5.00, 'nut_dia': 75.0, 'nut_diag': 82.600, 'nut_thick_max': 38.9, 'nut_thick_min': 36.4,
             'thread': "preferred"},
        56: {'pitch': 5.50, 'nut_dia': 85.0, 'nut_diag': 93.560, 'nut_thick_max': 45.9, 'nut_thick_min': 43.4,
             'thread': "preferred"},
        64: {'pitch': 6.00, 'nut_dia': 95.0, 'nut_diag': 104.860, 'nut_thick_max': 52.4, 'nut_thick_min': 49.4,
             'thread': "preferred"},
        14: {'pitch': 2.00, 'nut_dia': 21.0, 'nut_diag': 22.780, 'nut_thick_max': 13.9, 'nut_thick_min': 12.1,
             'thread': "non_preferred"},
        18: {'pitch': 2.50, 'nut_dia': 27.0, 'nut_diag': 29.560, 'nut_thick_max': 16.9, 'nut_thick_min': 15.1,
             'thread': "non_preferred"},
        22: {'pitch': 2.50, 'nut_dia': 34.0, 'nut_diag': 37.290, 'nut_thick_max': 20.2, 'nut_thick_min': 18.1,
             'thread': "non_preferred"},
        27: {'pitch': 3.00, 'nut_dia': 41.0, 'nut_diag': 45.200, 'nut_thick_max': 24.7, 'nut_thick_min': 22.6,
             'thread': "non_preferred"},
        33: {'pitch': 3.50, 'nut_dia': 50.0, 'nut_diag': 55.370, 'nut_thick_max': 29.5, 'nut_thick_min': 27.4,
             'thread': "non_preferred"},
        39: {'pitch': 4.00, 'nut_dia': 60.0, 'nut_diag': 66.440, 'nut_thick_max': 34.3, 'nut_thick_min': 31.8,
             'thread': "non_preferred"},
        45: {'pitch': 4.50, 'nut_dia': 70.0, 'nut_diag': 76.950, 'nut_thick_max': 36.9, 'nut_thick_min': 34.4,
             'thread': "non_preferred"},
        52: {'pitch': 5.00, 'nut_dia': 80.0, 'nut_diag': 88.250, 'nut_thick_max': 42.9, 'nut_thick_min': 40.4,
             'thread': "non_preferred"},
        60: {'pitch': 5.50, 'nut_dia': 90.0, 'nut_diag': 99.210, 'nut_thick_max': 48.9, 'nut_thick_min': 46.4,
             'thread': "non_preferred"}
    }


# IS 1367 - Part 3 : 2002
class IS1367_Part3_2002(object):
    """Perform calculations as per IS 1367 (Part 3) : 2002 [ISO 898-1:1999]
    Technical supply conditions for threaded steel fasteners
    Part 3 : Mechanical properties of fasteners made of carbon steel and alloy steel-
    Bolts, screws and studs
    """

    @staticmethod
    def get_bolt_PC():
        # Bolt grades available as per Table 1 of IS 1367(Part-3) :2002 (list)
        bolt_grades = ['3.6', '4.6', '4.8', '5.6', '5.8', '6.8', '8.8', '9.8', '10.9', '12.9']
        return bolt_grades

    # Calculate bolt nominal tensile strength depending upon grade of bolt
    @staticmethod
    def get_bolt_fu_fy(bolt_PC, bolt_diameter):
        """Calculate nominal tensile strength and yield strength of bolt

        Args:
            bolt_PC: Property Class of bolt (property class as per the designation)  (float)

        Return:
             Nominal tensile strength of bolt in MPa and Yield strength in MPa (list)

        Note:
            Reference:
            IS 1367 (Part 3) :2002 cl. 3

        """
        try:
            bolt_PC = float(bolt_PC)
            bolt_diameter = int(bolt_diameter)
        except ValueError:
            return

        conn = sqlite3.connect(PATH_TO_DATABASE)
        db_query = "SELECT * FROM Bolt_fy_fu WHERE Property_Class = ? AND Diameter_min < ? AND Diameter_max >= ?"
        cur = conn.cursor()
        cur.execute(db_query, (bolt_PC, bolt_diameter, bolt_diameter,))
        row = cur.fetchone()

        bolt_fy = float(row[3])
        bolt_fu = float(row[4])

        print(bolt_fu, bolt_fy)
        # print(type(bolt_fu))

        # bolt_fu = float(int(bolt_grade) * 100)
        # bolt_fy = float((bolt_grade - int(bolt_grade)) * bolt_fu)
        return [bolt_fu, bolt_fy]

    # Returns bolt shank area and nominal stress area depending upon diameter of bolt
    @staticmethod
    def bolt_area(bolt_diameter):
        """Calculate shank area and nominal stress area (thread area) of bolt

        Args:
            bolt_diameter: Nominal diameter of bolt in mm (float)

        Return:
             Shank area and nominal stress area of bolt as given in Table 6 of IS 1367 (Part-3) : 2002 (list)

        Note:
            Reference:
            IS 1367 (Part 3) :2002 Table 6
        """
        try:
            shank_area = round(math.pi * bolt_diameter ** 2 / 4)  # mm^2
        except ValueError:
            return

        #Note: The area of the bolts for diameter 48, 56, 64 and 72 has been added for base plate design
        # (these might not be available in IS 1367 (Part-3) : 2002)
        table_6 = {3: 5.03, 3.5: 6.78, 4: 8.78, 5: 14.2, 6: 20.1, 7: 28.9, 8: 36.6, 10: 58,
                   12: 84.3, 14: 115, 16: 157, 18: 192, 20: 245, 22: 303, 24: 353, 27: 459,
                   30: 561, 33: 694, 36: 817, 39: 976, 42: 1080, 45: 1240, 48: 1411, 52: 1656, 56: 1921, 60: 2205, 64: 2508, 72: 3175}
        try:
            return [shank_area, table_6[bolt_diameter]]
        except KeyError:
            return


# IS 3757 : 1985
class IS3757_1985(object):
    """Perform calculations as per IS 3757 : 1985 [ISO/DIS 7412]
    Specifications for high strength structural bolts
    """

    # Dimensions of High Strength Structural Bolts as per Table 1 (dict) [key: Diameter of bolt]
    bolt_dimensions = {
        16: {'pitch': 2.00, 'head_thick': 10.0, 'head_diag': 29.56, 'head_dia': 27.0, 'thread': "preferred"},
        20: {'pitch': 2.50, 'head_thick': 12.5, 'head_diag': 37.29, 'head_dia': 34.0, 'thread': "preferred"},
        22: {'pitch': 2.50, 'head_thick': 14.0, 'head_diag': 39.55, 'head_dia': 36.0, 'thread': "non_preferred"},
        24: {'pitch': 3.00, 'head_thick': 15.0, 'head_diag': 45.20, 'head_dia': 41.0, 'thread': "preferred"},
        27: {'pitch': 3.00, 'head_thick': 17.0, 'head_diag': 50.85, 'head_dia': 46.0, 'thread': "non_preferred"},
        30: {'pitch': 3.50, 'head_thick': 18.7, 'head_diag': 55.37, 'head_dia': 50.0, 'thread': "preferred"},
        36: {'pitch': 4.00, 'head_thick': 22.5, 'head_diag': 66.44, 'head_dia': 60.0, 'thread': "preferred"}
    }

    # Returns a list of available bolt lengths in mm depending upon diameter of bolt
    @staticmethod
    def bolt_length(bolt_diameter):
        """Make a list of available bolt lengths in mm for the given diameter of bolt

        Args:
            bolt_diameter: Nominal diameter of bolt in mm (float)

        Return:
             List of available bolt lengths in mm as per IS: 3757 : 1985 for the given diameter (list)

        Note:
            Reference:
            IS 3757 : 1985, Table 2
        """
        bolt_lengths = [40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110, 120, 130, 140, 150,
                        160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300]
        length_index = {16: 0, 20: 1, 22: 2, 24: 3, 27: 4, 30: 5, 36: 7}
        return bolt_lengths[length_index[bolt_diameter]:]


# IS 6623 : 2004
class IS6623_2004(object):
    """Perform calculations on steel design as per Indian Standard, IS 6623 :2004
        High Strength Structural Nuts - Specification
    """

    # Dimensions of High Strength Nuts as per Table 1 (dict) [key: Nut thread size in mm]
    nut_dimensions = {
        12: {'pitch': 1.75, 'nut_dia': 21.0, 'nut_diag': 22.780, 'nut_thick_max': 12.3, 'nut_thick_min': 11.9,
             'thread': "preferred"},
        16: {'pitch': 2.00, 'nut_dia': 27.0, 'nut_diag': 29.56, 'nut_thick_max': 17.1, 'nut_thick_min': 16.4,
             'thread': "preferred"},
        20: {'pitch': 2.50, 'nut_dia': 34.0, 'nut_diag': 37.29, 'nut_thick_max': 20.7, 'nut_thick_min': 19.4,
             'thread': "preferred"},
        22: {'pitch': 2.50, 'nut_dia': 35.0, 'nut_diag': 39.55, 'nut_thick_max': 23.6, 'nut_thick_min': 22.3,
             'thread': "non_preferred"},
        24: {'pitch': 3.00, 'nut_dia': 41.0, 'nut_diag': 45.20, 'nut_thick_max': 24.2, 'nut_thick_min': 22.9,
             'thread': "preferred"},
        27: {'pitch': 3.00, 'nut_dia': 46.0, 'nut_diag': 50.85, 'nut_thick_max': 27.6, 'nut_thick_min': 26.3,
             'thread': "non_preferred"},
        30: {'pitch': 3.50, 'nut_dia': 50.0, 'nut_diag': 55.37, 'nut_thick_max': 30.7, 'nut_thick_min': 29.1,
             'thread': "preferred"},
        36: {'pitch': 4.00, 'nut_dia': 60.0, 'nut_diag': 66.44, 'nut_thick_max': 36.6, 'nut_thick_min': 35.0,
             'thread': "preferred"}
    }


# IS 5624:1993, Foundation Bolts - Specification
class IS_5624_1993(object):
    """Specifications of IS 5624:1993"""

    @staticmethod
    def table1(anchor_dia):
        """Dimensions and preferred length dia combination of anchor bolt

        Args: anchor_dia (str) - Diameter of the anchor bolt

        Returns: anchor_length (int) - A list with the minimum and maximum length of the anchor bolt in mm

        Note: The length of the anchor bolt is decided based on the range suggested by Table 1 of IS 5624:1993.
        The average value is rounded off to a higher multiple of 5.

        """
        anchor_details = {
            'M8': {'dia': 8, 'min_len': 80, 'max_len': 200, 'avg_len': 140},
            'M10': {'dia': 10, 'min_len': 100, 'max_len': 250, 'avg_len': 175},
            'M12': {'dia': 12, 'min_len': 125, 'max_len': 320, 'avg_len': 225},
            'M16': {'dia': 16, 'min_len': 160, 'max_len': 500, 'avg_len': 330},
            'M20': {'dia': 20, 'min_len': 200, 'max_len': 800, 'avg_len': 500},
            'M24': {'dia': 24, 'min_len': 250, 'max_len': 1250, 'avg_len': 750},
            'M30': {'dia': 30, 'min_len': 320, 'max_len': 2000, 'avg_len': 1160},
            'M36': {'dia': 36, 'min_len': 400, 'max_len': 2500, 'avg_len': 1450},
            'M42': {'dia': 42, 'min_len': 400, 'max_len': 2500, 'avg_len': 1450},
            'M48': {'dia': 48, 'min_len': 630, 'max_len': 3200, 'avg_len': 1915},
            'M56': {'dia': 56, 'min_len': 800, 'max_len': 3200, 'avg_len': 2000},
            'M64': {'dia': 64, 'min_len': 1000, 'max_len': 3200, 'avg_len': 2100},
            'M72': {'dia': 72, 'min_len': 1000, 'max_len': 3200, 'avg_len': 2100},
        }[str(anchor_dia)]

        anchor_details_list = [anchor_details.get('dia'), anchor_details.get('min_len'),
                               anchor_details.get('max_len'), anchor_details.get('avg_len')]

        return anchor_details_list


class AISC(object):
    # TODO: This formula based on AISC guidelines, check if this should be included
    @staticmethod
    def cl_j_4_2_b_shear_rupture(A_vn, fu):
        '''
        Args:
            A_vn (float) Net area under shear
            beam_fu (float) Ultimate stress of beam material
        Returns:
            Capacity of beam web in shear rupture
        Note:
            Reference:
            J4.2(b) Speciﬁcation for Structural Steel Buildings, June 22, 2010, AISC
        '''
        R_n = (0.75 * fu * A_vn)
        shear_rupture_capacity = round(R_n, 2)
        return shear_rupture_capacity


class IS6649(object):
    """ IS 6649:1985, Hardened and Tempered Washers for High Strength Structural Bolts and Nuts

    """
    @staticmethod
    def circular_washer_dimensions(bolt_dia):
        """ Calculate the dimensions - diameter (inner and outer) and thickness for circular washer (Type A) confirming to IS 6649:1985.
        The washers are used for high strength structural bolts and nuts.

        Args:
            bolt_dia: diameter of the bolt in mm (int)

        Returns:
            inner and outer diameter of the washer in mm (dictionary)
            thickness of the washer in mm (dictionary)

        Reference - Table 1, IS 6649:1985

        Note: The IS code does not specify dimensions of washer for bolt sizes of M8, M10, M12, M16, M42, M48, M56, M64 and M72
              The dimensions of these washers are thus calculated/approximated referring to those specified by the code
        """
        washer_dimensions = {
            8: {'dia_in': 10, 'dia_out': 18, 'washer_thk': 4.6},
            10: {'dia_in': 12, 'dia_out': 20, 'washer_thk': 4.6},
            12: {'dia_in': 14, 'dia_out': 25, 'washer_thk': 4.6},
            16: {'dia_in': 18, 'dia_out': 34, 'washer_thk': 4.6},
            20: {'dia_in': 22, 'dia_out': 42, 'washer_thk': 4.6},
            22: {'dia_in': 24, 'dia_out': 44, 'washer_thk': 4.6},
            24: {'dia_in': 26, 'dia_out': 50, 'washer_thk': 4.6},
            27: {'dia_in': 30, 'dia_out': 66, 'washer_thk': 4.6},
            30: {'dia_in': 33, 'dia_out': 60, 'washer_thk': 4.6},
            36: {'dia_in': 39, 'dia_out': 72, 'washer_thk': 4.6},
            42: {'dia_in': 45, 'dia_out': 85, 'washer_thk': 6.0},
            48: {'dia_in': 51, 'dia_out': 100, 'washer_thk': 6.0},
            56: {'dia_in': 59, 'dia_out': 115, 'washer_thk': 6.0},
            64: {'dia_in': 67, 'dia_out': 130, 'washer_thk': 6.0},
            72: {'dia_in': 75, 'dia_out': 145, 'washer_thk': 6.0},
        }[bolt_dia]

        return washer_dimensions

    @staticmethod
    def square_washer_dimensions(bolt_dia):
        """ Calculate the dimensions - diameter (inner and outer) and thickness for circular washer (Type B and C) confirming to IS 6649:1985.
        The washers are used for high strength structural bolts and nuts.

        Args:
            bolt_dia: diameter of the bolt in mm (int)

        Returns:
            inner and outer diameter of the washer in mm (dictionary)
            thickness of the washer in mm (dictionary)

        Reference - Table 2, IS 6649:1985

        Note: The IS code does not specify dimensions of washer for bolt sizes of M8, M10, M12, M16, M42, M48, M56, M64 and M72
              The dimensions of these washers are thus calculated/approximated referring to those specified by the code

              Table 2 gives washer thickness for tapered washers, however for non-tapered washers, mean thickness is used.

              The sizes of the washer is adjusted such that its size is atleast greater than the bolt/anchor diameter

              The 'side' dimension of the washer is chosen maximum considering the nut size as per IS:3757(1989) and IS:1364 (PART-1) : 2002
              Adding 10 mm extra on each side

              boltHeadDia = {5: 8, 6: 10, 8: 13, 10: 16, 12: 18, 14: 21, 16: 24, 18: 27, 20: 30, 22: 34, 24: 36, 27: 41,
                               30: 46, 33: 50, 36: 55, 39: 60, 42: 65, 48: 75, 56: 85, 64: 95, 72: 110}

        """
        washer_dimensions = {
            8: {'dia_in': 10, 'side': max(25, 23), 'washer_thk': 6.0},
            10: {'dia_in': 12, 'side': max(25, 26), 'washer_thk': 6.0},
            12: {'dia_in': 14, 'side': max(25, 28), 'washer_thk': 6.0},
            16: {'dia_in': 18, 'side': max(45, 34), 'washer_thk': 8.5},
            20: {'dia_in': 22, 'side': max(45, 40), 'washer_thk': 8.5},
            22: {'dia_in': 24, 'side': max(45, 44), 'washer_thk': 8.5},
            24: {'dia_in': 26, 'side': max(45, 46), 'washer_thk': 8.5},
            27: {'dia_in': 30, 'side': max(58, 52), 'washer_thk': 8.5},
            30: {'dia_in': 33, 'side': max(58, 56), 'washer_thk': 8.5},
            36: {'dia_in': 39, 'side': max(58, 65), 'washer_thk': 8.5},
            42: {'dia_in': 45, 'side': max(80, 75), 'washer_thk': 10.0},
            48: {'dia_in': 51, 'side': max(80, 85), 'washer_thk': 10.0},
            56: {'dia_in': 59, 'side': max(100, 95), 'washer_thk': 12.0},
            64: {'dia_in': 67, 'side': max(100, 105), 'washer_thk': 12.0},
            72: {'dia_in': 75, 'side': max(100, 120), 'washer_thk': 12.0},
        }[bolt_dia]
        return washer_dimensions


class IS1364Part3(object):
    """ Hexagon Head Bolts, Screws, and Nuts of Product Grade A, and B, Part 3: Hexagon Nuts (Size Range M5 to M64)

    """

    @staticmethod
    def nut_thick(bot_dia):
        """ Returns the thickness of the hexagon nut (Grade A and B) depending upon the nut diameter as per IS1364-3(2002) - Table 1

        Args:
            bot_dia: diameter of the bolt in mm (int)

        Returns: the thickness of the hexagon nut (float)

        Note: The nut thk for 72 diameter is not available in IS code, however an approximated value is assumed.
              72 mm dia bolt is used in the base plate module.
        """
        nut_thickness = {
            5: 4.7,
            6: 5.2,
            8: 6.8,
            10: 8.4,
            12: 10.8,
            14: 12.8,
            16: 14.8,
            18: 15.8,
            20: 18.0,
            22: 19.4,
            24: 21.5,
            27: 23.8,
            30: 25.6,
            33: 28.7,
            36: 31,
            39: 33.4,
            42: 34.0,
            48: 38.0,
            56: 45.0,
            64: 51.0,
            72: 60.0
        }[bot_dia]

        return nut_thickness

    @staticmethod
    def nut_size(bot_dia):
        """ Returns the size of the hexagon nut (Grade A and B) depending upon the nut diameter as per IS1364-3(2002) - Table 1

        Args:
            bot_dia: diameter of the bolt in mm (int)

        Returns: size of the hexagon nut [maximum of s and e, refer fig. 1 of IS 1364-3:2002] (float)

        Note: The nut size for 72 diameter is not available in IS code, however an approximated value is assumed.
              72 mm dia bolt is used in the base plate module.
        """
        nut_size = {
            5: max(8.0, 8.79),
            6: max(10.0, 11.5),
            8: max(16.0, 14.38),
            10: max(16.0, 17.77),
            12: max(18.0, 20.03),
            14: max(21.0, 23.36),
            16: max(24.0, 26.75),
            18: max(27.0, 29.56),
            20: max(30.0, 32.95),
            22: max(34.0, 37.29),
            24: max(36.0, 39.55),
            27: max(41.0, 45.2),
            30: max(46.0, 50.85),
            33: max(50.0, 55.37),
            36: max(55.0, 60.79),
            39: max(60.0, 66.44),
            42: max(65.0, 71.3),
            45: max(70.0, 76.95),
            48: max(75.0, 82.6),
            52: max(80.0, 88.0),
            56: max(85.0, 93.56),
            60: max(90.0, 99.21),
            64: max(95.0, 104.86),
        }[bot_dia]

        return nut_size
