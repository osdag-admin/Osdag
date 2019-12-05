from utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column
from utils.common.load import Load
from utils.common.material import Material
from main import Main

class Connection(Main):
    pass


if __name__ == "__main__":
    connection = Connection()
    connection.test()
    connection.design()
