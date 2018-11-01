from app.utils.common.material import Material
import sqlite3


class Component(object):

    def __init__(self, material=Material()):
        self.material = material
        self.path_to_database = "../../databases/Intg_osdag.sqlite"


class Bolt(Component):

    def __init__(self, grade=0.0, diameter=0.0, bolt_type="", length=0.0, material=Material()):
        self.grade = grade
        self.diameter = diameter
        self.bolt_type = bolt_type
        self.length = length
        super(Bolt, self).__init__(material)


class Nut(Component):

    def __init__(self, diameter=0.0, material=Material()):
        self.diameter = diameter
        super(Nut, self).__init__(material)


class Section(Component):

    def __init__(self, designation, material=Material()):
        self.designation = designation
        self.depth = 0.0
        self.flange_width = 0.0
        self.web_thickness = 0.0
        self.flange_thickness = 0.0
        self.root_radius = 0.0
        self.toe_radius = 0.0
        super(Section, self).__init__(material)

    def connect_to_database_update_other_attributes(self, table, designation):
        conn = sqlite3.connect(self.path_to_database)
        db_query = "SELECT D, B, tw, T, R1, R2 FROM " + table + " WHERE Designation = ?"
        cur = conn.cursor()
        cur.execute(db_query, (designation,))
        row = cur.fetchone()

        self.depth = row[0]
        self.flange_width = row[1]
        self.web_thickness = row[2]
        self.flange_thickness = row[3]
        self.root_radius = row[4]
        self.toe_radius = row[5]

        conn.close()


class Beam(Section):

    def __init__(self, designation, material=Material()):
        super(Beam, self).__init__(designation, material)
        self.connect_to_database_update_other_attributes("Beams", designation)


class Column(Section):

    def __init__(self, designation, material=Material()):
        super(Column, self).__init__(designation, material)
        self.connect_to_database_update_other_attributes("Columns", designation)


class Weld(Component):

    def __init__(self, size=0.0, length=0.0, material=Material()):
        self.size = size
        self.length = length
        super(Weld, self).__init__(material)


class Plate(Component):

    def __init__(self, thickness=0.0, height=0.0, width=0.0, material=Material()):
        self.thickness = thickness
        self.height = height
        self.width = width
        super(Plate, self).__init__(material)


class Angle(Component):

    def __init__(self, designation, material=Material()):
        self.designation = designation

        self.leg_a_length = 0.0
        self.leg_b_length = 0.0
        self.thickness = 0.0

        self.connect_to_database_update_other_attributes(designation)

        self.length = 0.0
        super(Angle, self).__init__(material)

    def connect_to_database_update_other_attributes(self, designation):
        conn = sqlite3.connect(self.path_to_database)
        db_query = "SELECT AXB, t FROM Angles WHERE Designation = ?"
        cur = conn.cursor()
        cur.execute(db_query, (designation,))
        row = cur.fetchone()

        axb = row[0]
        axb = axb.lower()
        self.leg_a_length = float(axb.split("x")[0])
        self.leg_b_length = float(axb.split("x")[1])
        self.thickness = row[1]

        conn.close()
