class Load(object):

    def __init__(self,
                 axial_force=0.0,
                 shear_force=0.0,
                 shear_force_zz=0.0,
                 shear_force_yy=0.0,
                 moment=0.0,
                 moment_zz=0.0,
                 moment_yy=0.0,
                 moment_minor=0.0,
                 unit_kNm=False):

        force_multiplier = 1.0
        moment_multiplier = 1.0
        if unit_kNm is True:
            force_multiplier = 1e3
            moment_multiplier = 1e6
        print(force_multiplier, "is force multiplier")
        if axial_force is not "":
            self.axial_force = force_multiplier * float(axial_force)
        else:
            self.axial_force = 0.0

        '''
            Shear force
        '''
        if shear_force is not "":
            self.shear_force = force_multiplier * float(shear_force)
        else:
            self.shear_force = 0.0
        if shear_force_zz is not "":
            self.shear_force_zz = force_multiplier * float(shear_force_zz)
        else:
            self.shear_force_zz = 0.0
        if shear_force_yy is not "":
            self.shear_force_yy = force_multiplier * float(shear_force_yy)
        else:
            self.shear_force_yy = 0.0

        '''
            Moment force
        '''
        if moment is not "":
            self.moment = moment_multiplier * float(moment)
            self.moment_minor = moment_multiplier * float(moment_minor)
        else:
            self.moment = 0.0
            self.moment_minor = 0.0
        if moment_yy is not "":
            self.moment_yy = moment_multiplier * float(moment_yy)
            self.moment_minor = moment_multiplier * float(moment_minor)
        else:
            self.moment_yy = 0.0
            self.moment_minor = 0.0
        if moment_zz is not "":
            self.moment_zz = moment_multiplier * float(moment_zz)
            self.moment_minor = moment_multiplier * float(moment_minor)
        else:
            self.moment_zz = 0.0
            self.moment_minor = 0.0
        print("setting factored input loads as, axial force = {0} N, shear force = {1} N, moment = {2} Nmm".format(
            self.axial_force, self.shear_force, self.moment))

    def __repr__(self):
        repr = "Load\n"
        repr += "Axial Force: {}\n".format(self.axial_force)
        repr += "Shear Force: {}\n".format(self.shear_force)
        repr += "Moment: {}\n".format(self.moment)
        repr += "Moment Minor: {}\n".format(self.moment_minor)
        return repr
