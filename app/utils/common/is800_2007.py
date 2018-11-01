class IS800_2007(object):

    @staticmethod
    def compute_min_weld_thickness(part1_thickness, part2_thickness):
        thicker_part_thickness = max(part1_thickness, part2_thickness)

        if thicker_part_thickness <= 10:
            return 3
        elif thicker_part_thickness <= 20:
            return 5
        elif thicker_part_thickness <= 32:
            return 6
        elif thicker_part_thickness <= 50:
            return 10

    @staticmethod
    def compute_max_weld_thickness(part1_thickness, part2_thickness):
        return min(part1_thickness, part2_thickness)