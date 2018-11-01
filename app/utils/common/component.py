from app.utils.common.material import Material


class Component(object):

    def __init__(self):
        self.material = Material()


class Bolt(Component):

    def __init__(self):
        self.grade = 0.0
        self.diameter = 0.0
        self.bolt_type = ""  # friction_grip or bearing
        self.length = 0.0
        super(Bolt, self).__init__()


class Nut(Component):

    def __init__(self):
        self.diameter = 0.0


class Section(Component):

    def __init__(self, designation):
        self.designation = designation

        # Connect to database and get other properties from section name
        # Then initialize other variables from those properties

        # self.depth
        # self.flange_width
        # self.flange_thickness
        # self.web_thickness
        # self.root_radius
        # self.toe_radius

        super(Section, self).__init__()


class Weld(Component):

    def __init__(self):
        self.size = 0.0
        self.length = 0.0
        super(Weld, self).__init__()


class Plate(Component):

    def __init__(self):
        self.thickness = 0.0
        self.height = 0.0
        self.width = 0.0
        super(Plate, self).__init__()


class Angle(Component):

    def __init__(self, designation):
        self.designation = designation

        # Connect to database and get other properties from section name
        # Then initialize other variables from those properties

        # self.leg_a_length
        # self.leg_b_length
        # self.thickness

        self.length = 0.0

        super(Angle, self).__init__()
