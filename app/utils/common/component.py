from app.utils.common.material import Material
import sqlite3


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
        super(Nut, self).__init__()


class Section(Component):

    def __init__(self, designation):
        self.designation = designation
        self.depth = 0.0
        self.flange_width = 0.0
        self.web_thickness = 0.0
        self.flange_thickness = 0.0
        self.root_radius = 0.0
        self.toe_radius = 0.0
        super(Section, self).__init__()

    def connect_to_database_update_other_attributes(self, table, designation):
        conn = sqlite3.connect("../../databases/Intg_osdag.sqlite")
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

    def __init__(self, designation):
        super(Beam, self).__init__(designation)
        self.connect_to_database_update_other_attributes("Beams", designation)


class Column(Section):

    def __init__(self, designation):
        super(Column, self).__init__(designation)
        self.connect_to_database_update_other_attributes("Columns", designation)


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

        self.leg_a_length = 0.0
        self.leg_b_length = 0.0
        self.thickness = 0.0

        self.connect_to_database_update_other_attributes(designation)

        self.length = 0.0
        super(Angle, self).__init__()

    def connect_to_database_update_other_attributes(self, designation):
        conn = sqlite3.connect("../../databases/Intg_osdag.sqlite")
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
