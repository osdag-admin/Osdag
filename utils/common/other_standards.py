"""Module for Indian Standards other than IS 800 : 2007

Included standards,
    IS 1363 - Part 1 : 2002
    IS 1363 - Part 3 : 2002
    IS 1367 - Part 3 : 2002
    IS 3757 : 1985
    IS 6623 : 2004

Started on 15 - Nov - 2018

@author: ajmalbabums
"""
import math


# IS 1363 - Part 1 : 2002
class IS1363_part_1_2002(object):
    """Perform calculations as per IS 1363 (Part 1) : 2002 [ISO 4016: 1999]
    Hexagon head bolts, screws, and nuts of product grade C
    Part 1 : Hexagon head bolts (size M5 to M64)
    """

    # Dimensions of Metric bolts as per Table 1 and 2 of IS 1363(Part-1) :2002 (dict)
    bolt_dimensions = {
        5:  {'pitch': 0.80, 'head_thick': 3.5,  'head_diag': 8.630,  'head_dia': 8.0,  'thread': "preferred"},
        6:  {'pitch': 1.00, 'head_thick': 4.0,  'head_diag': 10.890, 'head_dia': 10.0, 'thread': "preferred"},
        8:  {'pitch': 1.25, 'head_thick': 5.3,  'head_diag': 14.200, 'head_dia': 13.0, 'thread': "preferred"},
        10: {'pitch': 1.50, 'head_thick': 6.4,  'head_diag': 17.590, 'head_dia': 16.0, 'thread': "preferred"},
        12: {'pitch': 1.75, 'head_thick': 7.5,  'head_diag': 19.850, 'head_dia': 18.0, 'thread': "preferred"},
        16: {'pitch': 2.00, 'head_thick': 10.0, 'head_diag': 26.170, 'head_dia': 24.0, 'thread': "preferred"},
        20: {'pitch': 2.50, 'head_thick': 12.5, 'head_diag': 32.950, 'head_dia': 30.0, 'thread': "preferred"},
        24: {'pitch': 3.00, 'head_thick': 15.0, 'head_diag': 39.550, 'head_dia': 36.0, 'thread': "preferred"},
        30: {'pitch': 3.50, 'head_thick': 18.7, 'head_diag': 50.850, 'head_dia': 46.0, 'thread': "preferred"},
        36: {'pitch': 4.00, 'head_thick': 22.5, 'head_diag': 60.790, 'head_dia': 55.0, 'thread': "preferred"},
        42: {'pitch': 4.50, 'head_thick': 26.0, 'head_diag': 71.300, 'head_dia': 65.0, 'thread': "preferred"},
        48: {'pitch': 5.00, 'head_thick': 30.0, 'head_diag': 82.600, 'head_dia': 75.0, 'thread': "preferred"},
        56: {'pitch': 5.50, 'head_thick': 35.0, 'head_diag': 93.560, 'head_dia': 85.0, 'thread': "preferred"},
        64: {'pitch': 6.00, 'head_thick': 40.0, 'head_diag': 104.86, 'head_dia': 95.0, 'thread': "preferred"},
        14: {'pitch': 2.00, 'head_thick': 8.8,  'head_diag': 22.780, 'head_dia': 21.0, 'thread': "non_preferred"},
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
    bolt_length_preferred = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 80, 90, 100,110, 120, 130, 140, 150, 160, 180,
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

    # Bolt grades available as per Table 1 of IS 1367(Part-3) :2002 (list)
    bolt_grades = [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 8.8, 9.8, 10.9, 12.9]

    # Calculate bolt nominal tensile strength depending upon grade of bolt
    @staticmethod
    def get_bolt_fu_fy(bolt_grade):
        """Calculate nominal tensile strength and yield strength of bolt

        Args:
            bolt_grade: Grade of bolt (property class as per the designation)  (float)

        Return:
             Nominal tensile strength of bolt in MPa and Yield strength in MPa (list)

        Note:
            Reference:
            IS 1367 (Part 3) :2002 cl. 3

        """
        try:
            bolt_grade = float(bolt_grade)
        except ValueError:
            return
        bolt_fu = float(int(bolt_grade) * 100)
        bolt_fy = float((bolt_grade-int(bolt_grade)) * bolt_fu)
        return [bolt_fu, bolt_fy]

    # Returns bolt shank area and nominal stress area depending upon diameter of bolt
    @staticmethod
    def bolt_area(bolt_diameter):
        """Calculate shank area and nominal stress area of bolt

        Args:
            bolt_diameter: Nominal diameter of bolt in mm (float)

        Return:
             Shank area and nominal stress area of bolt as given in Table 6 of IS 1367 (Part-3) : 2002 (list)

        Note:
            Reference:
            IS 1367 (Part 3) :2002 Table 6
        """
        try:
            shank_area = math.pi * bolt_diameter**2 / 4
        except ValueError:
            return

        table_6 = {3: 5.03, 3.5: 6.78, 4: 8.78, 5: 14.2, 6: 20.1, 7: 28.9, 8: 36.6, 10: 58,
                   12: 84.3, 14: 115, 16: 157, 18: 192, 20: 245, 22: 303, 24: 353, 27: 459,
                   30: 561, 33: 694, 36: 817, 39: 976}
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

