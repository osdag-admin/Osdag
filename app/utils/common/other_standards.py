import math


# IS 1363 - Part 1 : 2002
class IS1363_part_1_2002(object):
    """


    """


# IS 1367 - Part 3 : 2002
class IS1367_Part3_2002(object):
    """ Perform calculations on steel design as per Indian Standard, IS 1367( Part 3 ) :2002 [ISO 898-1:1999]
        'TECHNICAL SUPPLY CONDITIONS FOR THREADED STEEL FASTENERS'
         PART 3 - MECHANICAL PROPERTIES OF FASTENERS MADE OF CARBON
                STEEL AND ALLOY STEEL — BOLTS, SCREWS AND STUDS

    """

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

    # Returns bolt nominal stress area depending upon diameter of bolt
    @staticmethod
    def bolt_nominal_stress_area(bolt_diameter):
        """Calculate nominal stress area of bolt

        Args:
            bolt_diameter: Nominal diameter of bolt

        Return:
             Nominal stress area of bolt as given in Table 6 of IS 1367 (Part-3) : 2002

        Note:
            Reference:
            IS 1367 (Part 3) :2002 Table 6
        """
        table_6 = {3: 5.03, 3.5: 6.78, 4: 8.78, 5: 14.2, 6: 20.1, 7: 28.9, 8: 36.6, 10: 58,
                   12: 84.3, 14: 115, 16: 157, 18: 192, 20: 245, 22: 303, 24: 353, 27: 459,
                   30: 561, 33: 694, 36: 817, 39: 976}
        try:
            return table_6[bolt_diameter]
        except KeyError:
            return
