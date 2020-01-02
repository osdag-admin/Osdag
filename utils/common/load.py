class Load(object):

    def __init__(self, axial_force=0.0, shear_force=0.0, moment=0.0):
        self.axial_force = float(axial_force)
        self.shear_force = float(shear_force)
        self.moment = float(moment)

    def __repr__(self):
        repr = "Load\n"
        repr += "Axial Force: {}\n".format(self.axial_force)
        repr += "Shear Force: {}\n".format(self.shear_force)
        repr += "Moment: {}\n".format(self.moment)
        return repr
