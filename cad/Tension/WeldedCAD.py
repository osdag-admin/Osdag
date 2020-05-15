"""
Initialized on 23-04-2020
Comenced on
@author: Anand Swaroop
"""

import numpy
import copy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse

class TensionCAD(object):
    def __init__(self, member, plate, inline_weld, opline_weld, member_data):
        """
        :param member: Angle or Channel
        :param plate: Plate
        :param weld: weld
        :param input: input parameters
        :param memb_data: data of the members
        """

        self.member = member
        self.plate = plate
        self.inline_weld = inline_weld
        self.opline_weld = opline_weld
        self.member_data = member_data

        self.plate1 = copy.deepcopy(self.plate)
        self.plate2 = copy.deepcopy(self.plate)

        self.member1 = copy.deepcopy(self.member)
        #self.member2 = copy.deepcopy(self.member)

        # add all the required using ifelse logic

    def create_3DModel(self):

        self.createMemberGeometry()
        self.createPlateGeometry()
        self.createWeldGeometry()

    def createMemberGeometry(self):
        member1OriginL = numpy.array([0.0, 0.0, 0.0])
        member1_uDir = numpy.array([1.0, 0.0, 0.0])
        member1_wDir = numpy.array([0.0, -1.0, 0.0])
        self.member1.place(member1OriginL, member1_uDir, member1_wDir)

        self.member1_Model = self.member1.create_model()

    def createPlateGeometry(self):
        plate1OriginL = numpy.array([0.0, 0.0, 0.0])
        plate1_uDir = numpy.array([0.0, 1.0, 0.0])
        plate1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.plate1.place(plate1OriginL, plate1_uDir, plate1_wDir)

        self.plate1_Model = self.plate1.create_model()

        plate2OriginL = numpy.array([0.0, 0.0, 0.0])
        plate2_uDir = numpy.array([0.0, 1.0, 0.0])
        plate2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.plate2.place(plate2OriginL, plate2_uDir, plate2_wDir)

        self.plate2_Model = self.plate2.create_model()

    def createWeldGeometry(self):
        pass

    def get_members_models(self):
        member = self.member1_Model
        return member

    def get_plates_models(self):
        plate = BRepAlgoAPI_Fuse(self.plate1_Model, self.plate2_Model).Shape()
        return plate

    def get_welded_models(self):
        pass

    def get_models(self):
        pass

if __name__ == '__main__':
    import math
    from cad.items.plate import Plate
    from cad.items.filletweld import FilletWeld
    from cad.items.channel import Channel
    from cad.items.angle import Angle
    from cad.items.stiffener_plate import StiffenerPlate

    import OCC.Core.V3d
    from OCC.Core.Quantity import Quantity_NOC_SADDLEBROWN, Quantity_NOC_BLUE1
    from OCC.Core.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
    from utilities import osdag_display_shape
    # from cad.common_logic import CommonDesignLogic

    from OCC.gp import gp_Pnt
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    # member = Channel(B= , T= , D= , t= , R1= 0, R2= 0, L= 100)
    member = Angle(L=2000, A=75, B=75, T=5, R1=0, R2=0)
    # plate = Plate(L= , W= , T= )
    plate_h = member.A + 30
    plate_L = 100
    plate_H = plate_h + 2 * (math.tan(30) * plate_L)
    cut = 2 * (math.tan(30) * plate_L)
    plate = StiffenerPlate(L=plate_L, W=plate_H, T=5, R11=plate_L, R12=cut, R21=plate_L, R22=cut, )
    inline_weld = FilletWeld(b=0, h=0, L=0)
    opline_weld = FilletWeld(b=0, h=0, L=0)
    member_data = 'Channel'

    tensionCAD = TensionCAD(member, plate, inline_weld, opline_weld, member_data)

    tensionCAD.create_3DModel()
    plate = tensionCAD.get_plates_models()
    mem = tensionCAD.get_members_models()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    display.DisplayShape(mem, update=True)
    display.DisplayColoredShape(plate, color='BLUE', update=True)

    start_display()
