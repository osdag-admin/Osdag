from app.utils.common.is800_2007 import IS800_2007


class Validator (object):

    # TODO : Check these functions static
    def validate_fu (self, fu):
        return 290 <= fu <= 780

    def validate_fy (self, fy):
        return 165 <= fy <= 650

    def validate_fu_fy (self, fu, fy):
        return fu > fy

    def validate_number (self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def validate_positive_value (self, value):
        return value > 0


class ConnectionValidator(Validator):

    def filter_weld_list(self, weld_size_list, part1_thickness, part2_thickness):

        min_weld_size = IS800_2007.cl_10_5_2_3_min_weld_size(part1_thickness, part2_thickness)
        # TODO : max weld size - throat thickness ambiguity
        max_weld_size = IS800_2007.cl_10_5_3_1_max_weld_throat_thickness(part1_thickness, part2_thickness)
        filtered_weld_size_list = list(filter(lambda x: min_weld_size <= x <= max_weld_size,
                                              weld_size_list))

        return filtered_weld_size_list


class ShearConnectionValidator(ConnectionValidator):

    def validate_height_min(self, height, supported_member):
        return height >= 0.6 * supported_member.depth

    def validate_height_max(self, height, connectivity, supporting_member, supported_member):
        if connectivity == "column_flange_beam_web" or connectivity == "column_web_beam_web":
            max_plate_height = supported_member.depth - 2 * (
                    supported_member.flange_thickness + supported_member.r1 + 5)
        elif connectivity == "beam_beam":
            max_plate_height = supported_member.depth - max(supporting_member.flange_thickness + supporting_member.r1,
                                                            supported_member.flange_thickness + supported_member.r1) \
                                                            - supported_member.flange_thickness \
                                                            + supported_member.r1 + 10
        return height <= max_plate_height


class FinPlateConnectionValidator(ShearConnectionValidator):

    def filter_plate_thickness(self, plate_thickness_list, bolt, supported_member):
        bolt_diameter = bolt.diameter
        supported_member_web_thickness = supported_member.web_thickness

        min_plate_thickness = supported_member_web_thickness
        max_plate_thickness = bolt_diameter / 2

        filtered_plate_thickness_list = list(filter(lambda x: min_plate_thickness <= x <= max_plate_thickness,
                                                    plate_thickness_list))

        return filtered_plate_thickness_list

    def filter_weld_list(self, weld_size_list, connectivity, supporting_member, plate):
        if connectivity == "column_flange_beam_web":
            return ConnectionValidator.filter_weld_list(weld_size_list, supporting_member.flange_thickness, plate.thickness)
        elif connectivity == "column_web_beam_web" or connectivity == "beam_beam":
            return ConnectionValidator.filter_weld_list(weld_size_list, supporting_member.web_thickness, plate.thickness)

    def validate_plate_height_min(self, plate, supported_member):
        plate_height = plate.height
        return ShearConnectionValidator.validate_height_min(plate_height, supported_member)

    def validate_plate_height_max(self, plate, connectivity, supporting_member, supported_member):
        plate_height = plate.height
        return ShearConnectionValidator.validate_height_max(plate_height, connectivity, supporting_member, supported_member)


class EndPlateConnectionValidator(ShearConnectionValidator):

    def filter_plate_thickness(self, plate_thickness_list, bolt):

        bolt_diameter = bolt.diameter
        max_plate_thickness = bolt_diameter / 2

        filtered_plate_thickness_list = []
        for plate_thickness in plate_thickness_list:
            if plate_thickness <= max_plate_thickness:
                filtered_plate_thickness_list.append(plate_thickness)

        return filtered_plate_thickness_list

    def validate_plate_width_max(self, plate_width, connectivity, supporting_member):
        if connectivity == "column_flange_beam_web":
            max_plate_width = supporting_member.flange_width
        elif connectivity == "column_web_beam_web":
            max_plate_width = supporting_member.depth - 2 * (supporting_member.flange_thickness + supporting_member.r1 + 5)
        else:
            return True
        return plate_width <= max_plate_width

    def filter_weld_list(self, weld_size_list, supported_member, plate):
        return ConnectionValidator.filter_weld_list(weld_size_list, supported_member.web_thickness, plate.thickness)

    def validate_plate_height_min(self, plate, supported_member):
        plate_height = plate.height
        return ShearConnectionValidator.validate_height_min(plate_height, supported_member)

    def validate_plate_height_max(self, plate, connectivity, supporting_member, supported_member):
        plate_height = plate.height
        return ShearConnectionValidator.validate_height_max(plate_height, connectivity, supporting_member,
                                                            supported_member)


class CleatAngleConnectionValidator(ShearConnectionValidator):

    def validate_angle_height_min(self, angle, supported_member):
        angle_height = angle.height
        return ShearConnectionValidator.validate_height_min(angle_height, supported_member)

    def validate_angle_height_max(self, angle, connectivity, supporting_member, supported_member):
        angle_height = angle.height
        return ShearConnectionValidator.validate_height_max(angle_height, connectivity, supporting_member,
                                                            supported_member)


class SeatedAngleConnectionValidator(ShearConnectionValidator):
    pass
