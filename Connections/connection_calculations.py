import math

class ConnectionCalculations(object):
    """Perform common calculations for connection components in abstract class.

    Note:
        This is the parent class for each connection module's calculation class.
    """

    def bolt_shear(self, bolt_diameter, number_of_bolts, bolt_fu):
        """Calculate factored shear capacity of bolt(s) based on IS 800, Cl 10.3.3.

        Args:
            bolt_diameter (int)
            number_of_bolts (int)
            bolt_fu (int)

        Returns:
            Factored shear capacity of bolt(s) as float.

        Note:
            Bolt factored shear capacity = bolt_fu * number_of_bolts * Area_bolt_net_tensile / (square_root(3) * gamma_mb)
            Assumptions:
            1)for all bolts, shear plane passes through threaded area
            2)for all bolts, tensile stress area equals the threaded area
            3)reduction factors for long joints, large grip lengths, packing plates are not applicable
            4) values for tensile stress area (mm^2) are taken from Table 5.9 in DoSS - N. Subramanian

        """
        gamma_mb = 1.25
        bolt_area = {
            '12': 84.3,
            '16': 157,
            '20': 245,
            '22': 303,
            '24': 353,
            '27': 459,
            '30': 561,
            '36': 817
        }[str(bolt_diameter)]
        bolt_nominal_shear_capacity = bolt_fu * number_of_bolts * bolt_area / math.sqrt(3) / 1000
        return round(bolt_nominal_shear_capacity / gamma_mb, 3)

    def bolt_hole_clearance(self, bolt_hole_type, bolt_diameter, custom_hole_clearance):
        """Calculate bolt hole clearance.

        Args:
            bolt_diameter (int)

        Returns:
            hole_clearance (int)

        Note:
            Reference:
            IS 800, Table 19 (Cl 10.2.1) : Clearances for Fastener Holes

        """
        if bolt_hole_type == 1:  # standard hole
            hole_clearance = {
                12: 1,
                14: 1,
                16: 2,
                18: 2,
                20: 2,
                22: 2,
                24: 2,
                30: 3,
                36: 3
            }[bolt_diameter]
        elif bolt_hole_type == 0:  # over size hole
            hole_clearance = {
                12: 3,
                14: 3,
                16: 4,
                18: 4,
                20: 4,
                22: 4,
                24: 6,
                30: 8,
                36: 8
            }[bolt_diameter]
        if custom_hole_clearance is not None:
            hole_clearance = custom_hole_clearance  # units: mm
        return hole_clearance  # units: mm