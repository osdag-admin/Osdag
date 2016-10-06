import sys
import unittest, model
from SeatAngleCalc import SeatAngleConnection
from PyQt4 import QtGui

class TestSeatAngleConnection(unittest.TestCase, SeatAngleConnection):
    # def test_bolt_shear(self):
    #     self.assertAlmostEquals(bolt_shear(20, 1, 410), 45.3)
    def setUp(self):
        pass
    def test_sa_params(self):
        app = QtGui.QApplication(sys.argv)
        model.module_setup()
        sample_input = create_sample_ui_input()
        self.sa_params(sample_input)
        self.assertEqual(self.angle_A, 150)
        self.assertEqual(self.top_angle, "ISA 100X65X8")
        self.assertEqual(self.connectivity, "Column flange-Beam web")
        self.assertEqual(self.beam_fu, 410)
        self.assertEqual(self.beam_section, "ISMB 300")
        self.assertEqual(self.column_section, "ISSC 200")
        self.assertEqual(self.shear_force, 140)
        self.assertEqual(self.beam_w_t, 7.7)
        self.assertEqual(self.beam_f_t, 13.1)
        self.assertEqual(self.angle_t, 12)

def create_sample_ui_input():
    input_dict = {'Member': {}, 'Load': {}, 'Bolt': {}, 'Angle': {}}
    input_dict['Member']['Connectivity'] = "Column flange-Beam web"
    input_dict['Member']['BeamSection'] = "ISMB 300"
    input_dict['Member']['ColumnSection'] = "ISSC 200"
    input_dict['Member']['fu (MPa)'] = 410
    input_dict['Member']['fy (MPa)'] = 250
    input_dict['Load']['ShearForce (kN)'] = 140
    input_dict['Bolt']['Diameter (mm)'] = 20
    input_dict['Bolt']['Type'] = "Black Bolt"
    input_dict['Bolt']['Grade'] = "4.6"
    input_dict['Angle']["AngleSection"] = "ISA 150X75X12"
    return input_dict

if __name__ == '__main__':
    unittest.main()
    # launchSeatAngleController(None)
    # set_osdaglogger()
    # rawLogger = logging.getLogger("raw")
    # rawLogger.setLevel(logging.INFO)
    # # while launching from Osdag Main:
    # # fh = logging.FileHandler("./Connections/Shear/SeatAngle/seatangle.log", mode="w")
    # # while launching from Seated Angle folder
    # fh = logging.FileHandler("./seatangle.log", mode="w")
    # formatter = logging.Formatter('''%(message)s''')
    # fh.setFormatter(formatter)
    # rawLogger.addHandler(fh)
    # # while launching from Osdag Main:
    # rawLogger.info('''<link rel="stylesheet" type="text/css" href="./Connections/Shear/SeatedAngle/log.css"/>''')
    # while launching from Seated Angle folder:
    # rawLogger.info('''<link rel="stylesheet" type="text/css" href=".//log.css"/>''')

    app = QtGui.QApplication(sys.argv)
    # window = MainController()
    # window.show()
    ex = TestSeatAngleConnection()
    sys.exit(app.exec_())


