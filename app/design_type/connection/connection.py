from app.utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column
from app.utils.common.load import Load
from app.utils.common.material import Material
from app.main import Main

class Connection(Main):
    pass


if __name__ == "__main__":
    connection = Connection()
    connection.test()
    connection.design()
