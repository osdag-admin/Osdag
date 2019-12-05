from utils.common.material import Material


class Main():

    def __init__(self, fu, fy):
        self.material = Material(fy=fy, fu=fu)
