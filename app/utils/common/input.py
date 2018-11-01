from app.Utils.Common.Component import Section, Bolt, Weld, Plate


class InputObject (object):
    def __init__(self, val):
        self.val = val


class ShearConnectionInputObject(InputObject):

    def __init__(self, a):
        self.connectivity = "test"
        # self.supporting_member = Section()
        # self.supported_member = Section()
        self.bolt = Bolt()
        self.bolt_diameter_list = []  # Get from database
        self.weld = Weld()
        self.weld_size_list = []
        super(ShearConnectionInputObject, self).__init__(a)


class FinPlateInputObject(ShearConnectionInputObject):

    def __init__(self, a):
        self.plate = Plate()
        super(FinPlateInputObject, self).__init__(a)


a = FinPlateInputObject(10)
print(a.val)