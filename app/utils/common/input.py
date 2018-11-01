from app.utils.common.component import Bolt, Weld, Plate, Angle


class Input(object):
    pass


class ConnectionInput(Input):
    pass


class ShearConnectionInput(Input):

    def __init__(self):
        self.connectivity = ""
        self.supporting_member = None
        self.supported_member = None
        self.bolt = Bolt()
        self.bolt_diameter_list = []
        self.weld = Weld()
        self.weld_size_list = []


class FinPlateConnectionInput(ShearConnectionInput):

    def __init__(self):
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
