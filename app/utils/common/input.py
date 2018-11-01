from app.utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column


class Input(object):
    pass


class ConnectionInput(Input):
    pass


class ShearConnectionInput(Input):

    def __init__(self):
        self.bolt = Bolt()
        self.bolt_diameter_list = []
        self.weld = Weld()
        self.weld_size_list = []


class FinPlateConnectionInput(ShearConnectionInput):

    def __init__(self, connectivity, supporting_member_section, supported_member_section):
        self.connectivity = connectivity
        if connectivity == "column_flange_beam_web" or "column_web_beam_web":
            self.supporting_member = Column(supporting_member_section)
        elif connectivity == "beam_beam":
            self.supporting_member = Beam(supporting_member_section)
        self.supported_member = Beam(supported_member_section)
        self.plate = Plate()
        super(FinPlateConnectionInput, self).__init__()


class EndPlateConnectionInput(ShearConnectionInput):

    def __init__(self):
        self.plate = Plate()
        super(EndPlateConnectionInput, self).__init__()


class CleatAngleConnectionInput(ShearConnectionInput):

    def __init__(self):
        self.angle = Angle()
        super(CleatAngleConnectionInput, self).__init__()


class SeatedAngleConnectionInput(ShearConnectionInput):

    def __init__(self):
        self.angle = Angle()
        super(SeatedAngleConnectionInput, self).__init__()
