"""
Initialized on 23-04-2020
Comenced on
@author: Anand Swaroop
"""

import numpy
import copy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse

class TensionAngleCAD(object):
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
        self.member2 = copy.deepcopy(self.member)
        #self.member2 = copy.deepcopy(self.member)

        # add all the required using ifelse logic

    def create_3DModel(self):

        self.createMemberGeometry()
        self.createPlateGeometry()
        self.createWeldGeometry()

    def createMemberGeometry(self):

        if self.member_data == 'B2BAngle' or self.member_data == 'Angle':
            member1OriginL = numpy.array([- self.plate.L + 50, 0.0, self.member.A / 2])
            member1_uDir = numpy.array([0.0, -1.0, 0.0])
            member1_wDir = numpy.array([1.0, 0.0, 0.0])
            self.member1.place(member1OriginL, member1_uDir, member1_wDir)

            self.member1_Model = self.member1.create_model()

        elif self.member_data == 'B2BAngle':
            member2OriginL = numpy.array([self.member.L - self.plate.L + 50, self.plate.T, self.member.A / 2])
            member2_uDir = numpy.array([0.0, 1.0, 0.0])
            member2_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.member2.place(member2OriginL, member2_uDir, member2_wDir)

            self.member2_Model = self.member2.create_model()

        elif self.member_data == 'Star Angle':
            member1OriginL = numpy.array([- self.plate.L + 50, 0.0, 0.0])
            member1_uDir = numpy.array([0.0, -1.0, 0.0])
            member1_wDir = numpy.array([1.0, 0.0, 0.0])
            self.member1.place(member1OriginL, member1_uDir, member1_wDir)

            self.member1_Model = self.member1.create_model()

            member2OriginL = numpy.array([- self.plate.L + 50, self.plate.T, 0.0])
            member2_uDir = numpy.array([0.0, 1.0, 0.0])
            member2_wDir = numpy.array([1.0, 0.0, 0.0])
            self.member2.place(member2OriginL, member2_uDir, member2_wDir)

            self.member2_Model = self.member2.create_model()

    def createPlateGeometry(self):
        plate1OriginL = numpy.array([0.0, 0.0, 0.0])
        plate1_uDir = numpy.array([1.0, 0.0, 0.0])
        plate1_wDir = numpy.array([0.0, 0.0, 1.0])
        self.plate1.place(plate1OriginL, plate1_uDir, plate1_wDir)

        self.plate1_Model = self.plate1.create_model()

        plate2OriginL = numpy.array([self.member.L - 2 * (self.plate.L - 50), self.plate.T, 0.0])
        plate2_uDir = numpy.array([-1.0, 0.0, 0.0])
        plate2_wDir = numpy.array([0.0, 0.0, 1.0])
        self.plate2.place(plate2OriginL, plate2_uDir, plate2_wDir)

        self.plate2_Model = self.plate2.create_model()

    def createWeldGeometry(self):
        pass

    def get_members_models(self):

        if self.member_data == 'Angle':
            member = self.member1_Model

        else:
            member = BRepAlgoAPI_Fuse(self.member1_Model, self.member2_Model).Shape()

        return member

    def get_plates_models(self):
        plate = BRepAlgoAPI_Fuse(self.plate1_Model, self.plate2_Model).Shape()
        return plate

    def get_welded_models(self):
        pass

    def get_models(self):
        pass


class TensionChannelCAD(TensionAngleCAD):

    def createMemberGeometry(self):
        if self.member_data == 'Channel':
            member1OriginL = numpy.array([- self.plate.L + 50, -self.member.B, self.member.D / 2])
            member1_uDir = numpy.array([0.0, -1.0, 0.0])
            member1_wDir = numpy.array([1.0, 0.0, 0.0])
            self.member1.place(member1OriginL, member1_uDir, member1_wDir)

            self.member1_Model = self.member1.create_model()

        elif self.member_data == 'B2BChannel':
            member1OriginL = numpy.array([- self.plate.L + 50, -self.member.B, self.member.D / 2])
            member1_uDir = numpy.array([0.0, -1.0, 0.0])
            member1_wDir = numpy.array([1.0, 0.0, 0.0])
            self.member1.place(member1OriginL, member1_uDir, member1_wDir)

            self.member1_Model = self.member1.create_model()

            member2OriginL = numpy.array(
                [self.member.L - self.plate.L + 50, self.plate.T + self.member.B, self.member.D / 2])
            member2_uDir = numpy.array([0.0, 1.0, 0.0])
            member2_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.member2.place(member2OriginL, member2_uDir, member2_wDir)

            self.member2_Model = self.member2.create_model()

    def crearteWeldGeometry(self):
        pass

    def get_members_models(self):

        if self.member_data == 'Channel':
            member = self.member1_Model
        elif self.member_data == 'B2BChannel':
            member = BRepAlgoAPI_Fuse(self.member1_Model, self.member2_Model).Shape()

        return member


if __name__ == '__main__':
    import math
    from cad.items.plate import Plate
    from cad.items.filletweld import FilletWeld
    from cad.items.channel import Channel
    from cad.items.angle import Angle
    from cad.items.stiffener_plate import StiffenerPlate
    from cad.items.Gasset_plate import GassetPlate

    import OCC.Core.V3d
    from OCC.Core.Quantity import Quantity_NOC_SADDLEBROWN, Quantity_NOC_BLUE1
    from OCC.Core.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
    from utilities import osdag_display_shape
    # from cad.common_logic import CommonDesignLogic

    from OCC.gp import gp_Pnt
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    member_data = 'B2BChannel'  # 'Channel' #'Star Angle' #B2BAngle or 'Angle' 'Channel' or

    inline_weld = FilletWeld(b=0, h=0, L=0)
    opline_weld = FilletWeld(b=0, h=0, L=0)

    if member_data == 'Channel' or member_data == 'B2BChannel':
        member = Channel(B=75, T=10.2, D=175, t=6, R1=0, R2=0, L=5000)
        plate = GassetPlate(L=560, H=210, T=16, degree=30)

        tensionCAD = TensionChannelCAD(member, plate, inline_weld, opline_weld, member_data)


    else:
        member = Angle(L=2000, A=75, B=75, T=5, R1=0, R2=0)
        plate = GassetPlate(L=540, H=255, T=5, degree=30)

        tensionCAD = TensionAngleCAD(member, plate, inline_weld, opline_weld, member_data)

    tensionCAD.create_3DModel()
    plate = tensionCAD.get_plates_models()
    mem = tensionCAD.get_members_models()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    display.DisplayShape(mem, update=True)
    display.DisplayColoredShape(plate, color='BLUE', update=True)

    start_display()
