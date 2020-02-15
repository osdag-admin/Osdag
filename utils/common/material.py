import sqlite3
from Common import *

class Material(object):

    def __init__(self, material_grade):
        self.fy_20 = 0.0
        self.fy_20_40 = 0.0
        self.fy_40 = 0.0
        self.fu = 0.0
        self.fy = 0.0
        if material_grade is not "":
            self.connect_to_database_to_get_fy_fu(grade=material_grade)

    def __repr__(self):
        repr = "Material:\n"
        repr += "fy_20: {}\n".format(self.fy_20)
        repr += "fy_20_40: {}\n".format(self.fy_20_40)
        repr += "fy_40: {}\n".format(self.fy_40)
        repr += "fu: {}\n".format(self.fu)
        return repr

    def connect_to_database_to_get_fy_fu(self, grade):
        conn = sqlite3.connect(PATH_TO_DATABASE)
        db_query = "SELECT * FROM Material WHERE Grade = ?"
        cur = conn.cursor()
        cur.execute(db_query,(grade,))
        row = cur.fetchone()
        self.fy_20 = row[1]
        self.fy_20_40 = row[2]
        self.fy_40 = row[3]
        self.fy = min(self.fy_20,self.fy_20_40,self.fy_40)
        self.fu = row[4]
        conn.close()