class OutputObject (object):
    pass


class ConnectionOutput(OutputObject):
    pass


class ShearConnectionOutput(ConnectionOutput):

    def __init__(self):
        pass


class FinPlateConnectionOutput(ShearConnectionOutput):

    def __init__(self):
        super(FinPlateConnectionOutput, self).__init__()


class EndPlateConnectionOutput(ShearConnectionOutput):

    def __init__(self):
        super(EndPlateConnectionOutput, self).__init__()


class CleatAngleConnectionOutput(ShearConnectionOutput):

    def __init__(self):
        super(CleatAngleConnectionOutput, self).__init__()


class SeatedAngleConnectionOutput(ShearConnectionOutput):

    def __init__(self):
        super(SeatedAngleConnectionOutput, self).__init__()
