class Material(object):

    def __init__(self, fy=0.0, fu=0.0):
        self.fy = fy
        self.fu = fu

    def __repr__(self):
        repr = "Material:\n"
        repr += "fy: {}\n".format(self.fy)
        repr += "fu: {}".format(self.fu)
        return repr
