import math


class IS1367_Part3_2002(object):
    """ Perform calculations on steel design as per Indian Standard, IS 1367( Part 3 ) :2002 [ISO 898-1:1999]
        'TECHNICAL SUPPLY CONDITIONS FOR THREADED STEEL FASTENERS'
         PART 3 - MECHANICAL PROPERTIES OF FASTENERS MADE OF CARBON
                STEEL AND ALLOY STEEL — BOLTS, SCREWS AND STUDS

    """

    # Calculate bolt nominal tensile strength depending upon grade of bolt
    @staticmethod
    def cl_3_get_bolt_fu_fy(bolt_grade):
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


