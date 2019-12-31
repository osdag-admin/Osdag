import sqlite3

class Database(object):
    def __init__(self):
        self.path_to_database = "ResourceFiles/Database/Intg_osdag.sqlite"

class Material(Database):

    def __init__(self, material_grade):
        super(Material, self).__init__()
        self.fy_20 = 0.0
        self.fy_20_40 = 0.0
        self.fy_40 = 0.0
        self.fu = 0.0
        self.connect_to_database_to_get_fy_fu(grade=material_grade)

    def __repr__(self):
        repr = "Material:\n"
        repr += "fy_20: {}\n".format(self.fy_20)
        repr += "fy_20_40: {}\n".format(self.fy_20_40)
        repr += "fy_40: {}\n".format(self.fy_40)
        repr += "fu: {}".format(self.fu)
        return repr

    def connect_to_database_to_get_fy_fu(self, grade):
        conn = sqlite3.connect(self.path_to_database)
        db_query = "SELECT * FROM Material WHERE Grade = ?"
        cur = conn.cursor()
        cur.execute(db_query,(grade,))
        row = cur.fetchone()
        self.fy_20 = row[1]
        self.fy_20_40 = row[2]
        self.fy_40 = row[3]
        self.fu = row[4]

        conn.close()