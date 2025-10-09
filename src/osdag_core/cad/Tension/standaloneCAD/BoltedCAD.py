"""
Initialized on 23-04-2020
Comenced on
@author: Anand Swaroop
"""

import numpy
import copy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse


class TensionAngleBoltCAD(object):
    def __init__(self, Obj, member, plate, nut_bolt_array, intermittentConnection):
        """
        :param member: Angle or Channel
        :param plate: Plate
        :param input: input parameters
        :param memb_data: data of the members
        """


        self.Obj = Obj  # 'Star Angles'  # 'Back to Back Channels'  #'Channels'  #'  #'Angles'  #      or 'Back to Back Angles' 'Channels' or
        self.loc = 'Long Leg'
        self.member = member
        self.plate = plate
        self.nut_bolt_array = nut_bolt_array
        self.intermittentConnection = intermittentConnection

        self.plate1 = copy.deepcopy(self.plate)
        self.plate2 = copy.deepcopy(self.plate)

        self.member1 = copy.deepcopy(self.member)
        self.member2 = copy.deepcopy(self.member)
        # self.member2 = copy.deepcopy(self.member)
        self.nut_bolt_arrayL = copy.deepcopy(self.nut_bolt_array)
        self.nut_bolt_arrayR = copy.deepcopy(self.nut_bolt_array)
        self.nut_bolt_arrayL_SA = copy.deepcopy(self.nut_bolt_array)
        self.nut_bolt_arrayR_SA = copy.deepcopy(self.nut_bolt_array)

        # front side member
        # weld vertical right side

        self.col = 2  # self.Obj.plate.bolt_line
        self.end = 35  # self.Obj.plate.end_dist_provided
        self.pitch = 45  # self.Obj.plate.pitch_provided
        self.plate_intercept = 2 * self.end + (self.col - 1) * self.pitch

    def create_3DModel(self):

        self.createMemberGeometry()
        self.createPlateGeometry()
        self.create_nut_bolt_array()

    def createMemberGeometry(self):

        if self.loc == 'Long Leg':
            if self.Obj == 'Angles':
                member1OriginL = numpy.array([-self.plate_intercept, 0.0, self.member.A / 2])
                member1_uDir = numpy.array([0.0, -1.0, 0.0])
                member1_wDir = numpy.array([1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

            elif self.Obj == 'Back to Back Angles':
                member1OriginL = numpy.array([-self.plate_intercept, 0.0, self.member.A / 2])
                member1_uDir = numpy.array([0.0, -1.0, 0.0])
                member1_wDir = numpy.array([1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

                member2OriginL = numpy.array([self.member.L - self.plate_intercept, self.plate.T, self.member.A / 2])
                member2_uDir = numpy.array([0.0, 1.0, 0.0])
                member2_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.member2.place(member2OriginL, member2_uDir, member2_wDir)

                self.member2_Model = self.member2.create_model()

            elif self.Obj == 'Star Angles':
                member1OriginL = numpy.array([-self.plate_intercept, 0.0, 0.0])
                member1_uDir = numpy.array([0.0, -1.0, 0.0])
                member1_wDir = numpy.array([1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

                member2OriginL = numpy.array([-self.plate_intercept, self.plate.T, 0.0])
                member2_uDir = numpy.array([0.0, 1.0, 0.0])
                member2_wDir = numpy.array([1.0, 0.0, 0.0])
                self.member2.place(member2OriginL, member2_uDir, member2_wDir)

                self.member2_Model = self.member2.create_model()

        else:
            if self.Obj == 'Angles':
                member1OriginL = numpy.array([-self.plate_intercept + self.member.L, 0.0, self.member.B / 2])
                member1_uDir = numpy.array([0.0, 0.0, -1.0])
                member1_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

            elif self.Obj == 'Back to Back Angles':
                member1OriginL = numpy.array([-self.plate_intercept + self.member.L, 0.0, self.member.B / 2])
                member1_uDir = numpy.array([0.0, 0.0, -1.0])
                member1_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

                member2OriginL = numpy.array([- self.plate_intercept, self.plate.T, self.member.B / 2])
                member2_uDir = numpy.array([0.0, 0.0, -1.0])
                member2_wDir = numpy.array([1.0, 0.0, 0.0])
                self.member2.place(member2OriginL, member2_uDir, member2_wDir)

                self.member2_Model = self.member2.create_model()

            elif self.Obj == 'Star Angles':
                member1OriginL = numpy.array([-self.plate_intercept + self.member.L, 0.0, 0.0])
                member1_uDir = numpy.array([0.0, 0.0, -1.0])
                member1_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

                member2OriginL = numpy.array([-self.plate_intercept + self.member.L, self.plate.T, 0.0])
                member2_uDir = numpy.array([0.0, 0.0, 1.0])
                member2_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.member2.place(member2OriginL, member2_uDir, member2_wDir)

                self.member2_Model = self.member2.create_model()

    def createPlateGeometry(self):
        plate1OriginL = numpy.array([0.0, 0.0, 0.0])
        plate1_uDir = numpy.array([1.0, 0.0, 0.0])
        plate1_wDir = numpy.array([0.0, 0.0, 1.0])
        self.plate1.place(plate1OriginL, plate1_uDir, plate1_wDir)

        self.plate1_Model = self.plate1.create_model()

        plate2OriginL = numpy.array([self.member.L - 2 * self.plate_intercept, self.plate.T, 0.0])
        plate2_uDir = numpy.array([-1.0, 0.0, 0.0])
        plate2_wDir = numpy.array([0.0, 0.0, 1.0])
        self.plate2.place(plate2OriginL, plate2_uDir, plate2_wDir)

        self.plate2_Model = self.plate2.create_model()

        if self.Obj == 'Back to Back Angles' or self.Obj == 'Back to Back Channels' or self.Obj == 'Star Angles' and self.member.L >1000:
            intermittentConnectionOriginL = numpy.array([0, 0.0, 0.0])
            intermittentConnection_uDir = numpy.array([0.0, 0.0, -1.0])
            intermittentConnection_vDir = numpy.array([1.0, 0.0, 0.0])
            intermittentConnection_wDir = numpy.array([0.0, 1.0, 0.0])
            self.intermittentConnection.place(intermittentConnectionOriginL, intermittentConnection_uDir,
                                              intermittentConnection_vDir, intermittentConnection_wDir)

            self.intermittentConnection_Model = self.intermittentConnection.create_model()
            self.inter_conc_bolts = self.intermittentConnection.get_nut_bolt_models()
            self.inter_conc_plates = self.intermittentConnection.get_plate_models()

    def create_nut_bolt_array(self):
        """

        :return: Geometric Orientation of this component
        """
        if self.Obj == 'Channels' or self.Obj == 'Back to Back Channels':
            self.member.A = self.member.D
            self.member.T = self.member.t
        # nutboltArrayOrigin = self.baseplate.sec_origin + numpy.array([0.0, 0.0, self.baseplate.T /2+ 100])

        if self.Obj == 'Star Angles':
            nutboltArrayLOrigin = numpy.array([-self.plate_intercept, -self.member.T, 0.0])
            gaugeDir = numpy.array([0.0, 0, -1.0])
            pitchDir = numpy.array([1.0, 0.0, 0])
            boltDir = numpy.array([0, 1.0, 0.0])
            self.nut_bolt_arrayL.place(nutboltArrayLOrigin, gaugeDir, pitchDir, boltDir)

            self.nutboltArrayLModels = self.nut_bolt_arrayL.create_model()

            nutboltArrayROrigin = numpy.array([self.member.L - 2 * self.plate_intercept, -self.member.T, 0.0])
            gaugeDir = numpy.array([0.0, 0, -1.0])
            pitchDir = numpy.array([1.0, 0.0, 0])
            boltDir = numpy.array([0, 1.0, 0.0])
            self.nut_bolt_arrayR.place(nutboltArrayROrigin, gaugeDir, pitchDir, boltDir)

            self.nutboltArrayRModels = self.nut_bolt_arrayR.create_model()

            nutboltArrayL_SAOrigin = numpy.array([-self.plate_intercept, self.member.T + self.plate.T, 0.0])
            gaugeDir = numpy.array([0.0, 0, 1.0])
            pitchDir = numpy.array([1.0, 0.0, 0])
            boltDir = numpy.array([0, -1.0, 0.0])
            self.nut_bolt_arrayL_SA.place(nutboltArrayL_SAOrigin, gaugeDir, pitchDir, boltDir)

            self.nutboltArrayL_SAModels = self.nut_bolt_arrayL_SA.create_model()

            nutboltArrayR_SAOrigin = numpy.array(
                [self.member.L - 2 * self.plate_intercept, self.member.T + self.plate.T, 0.0])
            gaugeDir = numpy.array([0.0, 0, 1.0])
            pitchDir = numpy.array([1.0, 0.0, 0])
            boltDir = numpy.array([0, -1.0, 0.0])
            self.nut_bolt_arrayR_SA.place(nutboltArrayR_SAOrigin, gaugeDir, pitchDir, boltDir)

            self.nutboltArrayR_SAModels = self.nut_bolt_arrayR_SA.create_model()

        else:
            if self.loc == 'Long Leg':
                self.placement = self.member.A / 2
            else:
                self.placement = self.member.B / 2
            nutboltArrayLOrigin = numpy.array([-self.plate_intercept, -self.member.T, self.placement])
            gaugeDir = numpy.array([0.0, 0, -1.0])
            pitchDir = numpy.array([1.0, 0.0, 0])
            boltDir = numpy.array([0, 1.0, 0.0])
            self.nut_bolt_arrayL.place(nutboltArrayLOrigin, gaugeDir, pitchDir, boltDir)

            self.nutboltArrayLModels = self.nut_bolt_arrayL.create_model()

            nutboltArrayROrigin = numpy.array(
                [-2 * self.plate_intercept + self.member.L, -self.member.T, self.placement])
            gaugeDir = numpy.array([0.0, 0, -1.0])
            pitchDir = numpy.array([1.0, 0.0, 0])
            boltDir = numpy.array([0, 1.0, 0.0])
            self.nut_bolt_arrayR.place(nutboltArrayROrigin, gaugeDir, pitchDir, boltDir)

            self.nutboltArrayRModels = self.nut_bolt_arrayR.create_model()

    def get_members_models(self):

        if self.Obj == 'Angles':
            member = self.member1_Model

        else:
            member = BRepAlgoAPI_Fuse(self.member1_Model, self.member2_Model).Shape()

        return member

    def get_plates_models(self):
        plate = BRepAlgoAPI_Fuse(self.plate1_Model, self.plate2_Model).Shape()
        if self.Obj == 'Back to Back Angles' or self.Obj == 'Back to Back Channels' or self.Obj == 'Star Angles' and self.member.L >= 1000:
            plate = BRepAlgoAPI_Fuse(plate, self.inter_conc_plates).Shape()
        return plate

    def get_nut_bolt_array_models(self):

        if self.Obj == 'Star Angles':
            nut_bolts = [self.nutboltArrayLModels, self.nutboltArrayRModels, self.nutboltArrayL_SAModels,
                         self.nutboltArrayR_SAModels]
            array = nut_bolts[0]
            for comp in nut_bolts:
                array = BRepAlgoAPI_Fuse(comp, array).Shape()
        else:
            array = BRepAlgoAPI_Fuse(self.nutboltArrayLModels, self.nutboltArrayRModels).Shape()
        # array = nut_bolts[0]
        # for comp in nut_bolts:
        #     array = BRepAlgoAPI_Fuse(comp, array).Shape()

        if self.Obj == 'Back to Back Angles' or self.Obj == 'Back to Back Channels' or self.Obj == 'Star Angles' and self.member.L >= 1000:
            array = BRepAlgoAPI_Fuse(array, self.inter_conc_bolts).Shape()

        return array

    def get_models(self):
        pass


class TensionChannelBoltCAD(TensionAngleBoltCAD):

    def createMemberGeometry(self):
        if self.Obj == 'Channels':
            member1OriginL = numpy.array([-self.plate_intercept, -self.member.B, self.member.D / 2])
            member1_uDir = numpy.array([0.0, -1.0, 0.0])
            member1_wDir = numpy.array([1.0, 0.0, 0.0])
            self.member1.place(member1OriginL, member1_uDir, member1_wDir)

            self.member1_Model = self.member1.create_model()

        elif self.Obj == 'Back to Back Channels':
            member1OriginL = numpy.array([-self.plate_intercept, -self.member.B, self.member.D / 2])
            member1_uDir = numpy.array([0.0, -1.0, 0.0])
            member1_wDir = numpy.array([1.0, 0.0, 0.0])
            self.member1.place(member1OriginL, member1_uDir, member1_wDir)

            self.member1_Model = self.member1.create_model()

            member2OriginL = numpy.array(
                [self.member.L - self.plate_intercept, self.plate.T + self.member.B, self.member.D / 2])
            member2_uDir = numpy.array([0.0, 1.0, 0.0])
            member2_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.member2.place(member2OriginL, member2_uDir, member2_wDir)

            self.member2_Model = self.member2.create_model()

    def get_members_models(self):

        if self.Obj == 'Channels':
            member = self.member1_Model
        elif self.Obj == 'Back to Back Channels':
            member = BRepAlgoAPI_Fuse(self.member1_Model, self.member2_Model).Shape()

        return member


if __name__ == '__main__':
    import math
    from ...items.plate import Plate
    from ...items.channel import Channel
    from ...items.angle import Angle
    from ...items.bolt import Bolt
    from ...items.nut import Nut
    from ...items.stiffener_plate import StiffenerPlate
    from ...items.Gasset_plate import GassetPlate
    from .nutBoltPlacement import NutBoltArray
    from .IntermittentConnections import IntermittentNutBoltPlateArray

    import OCC.Core.V3d
    from OCC.Core.Quantity import Quantity_NOC_SADDLEBROWN, Quantity_NOC_BLUE1
    from OCC.Core.Graphic3d import Graphic3d_NOM_ALUMINIUM
    from ....utilities import osdag_display_shape
    # from ...common_logic import CommonDesignLogic

    from OCC.gp import gp_Pnt
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    Obj = 'Star Angles'  #'Back to Back Channels'  # 'Channels'  #'  #'Angles'  #      or 'Back to Back Angles' 'Channels' or

    # weld_size = 6
    # s = max(15, weld_size)

    plate = GassetPlate(L=360 + 50, H=205.0, T=10, degree=30)
    bolt = Bolt(R=8, T=5, H=6, r=3)
    nut = Nut(R=bolt.R, T=bolt.T, H=bolt.T + 1, innerR1=bolt.r)
    intermittentPlate = Plate(L= 2*125 , W=70, T=plate.T)

    if Obj == 'Channels' or Obj == 'Back to Back Channels':
        member = Channel(B=50, T=6.6, D=125, t=3, R1=6.0, R2=2.4, L=4000)
        # plate_intercept = plate.L - s - 50
        if Obj == 'Channels':
            nut_space = member.t + plate.T + nut.T  # member.T + plate.T + nut.T
        else:
            nut_space = 2 * member.t + plate.T + nut.T  # 2*member.T + plate.T + nut.T
        # plateObj = 0.0

        nut_bolt_array = NutBoltArray(Obj, nut, bolt, nut_space)
        intermittentConnection = IntermittentNutBoltPlateArray(Obj, nut, bolt, intermittentPlate, nut_space)

        tensionCAD = TensionChannelBoltCAD(Obj, member, plate, nut_bolt_array, intermittentConnection)


    else:
        member = Angle(L=2000.0, A=90.0, B=65.0, T=10.0, R1=8.0, R2=0.0)
        plate = GassetPlate(L=295 + 50, H=120, T=10, degree=30)
        # plate_intercept = plate.L - s - 50
        if Obj == 'Back to Back Angles':
            nut_space = 2 * member.T + plate.T + nut.T  # member.T + plate.T + nut.T
        else:
            nut_space = member.T + plate.T + nut.T  # 2*member.T + plate.T + nut.T

        plateObj = 0.0

        nut_bolt_array = NutBoltArray(plateObj, nut, bolt, nut_space)
        intermittentConnection = IntermittentNutBoltPlateArray(Obj, nut, bolt, intermittentPlate, nut_space)

        tensionCAD = TensionAngleBoltCAD(Obj, member, plate, nut_bolt_array, intermittentConnection)

    tensionCAD.create_3DModel()
    plate = tensionCAD.get_plates_models()
    mem = tensionCAD.get_members_models()
    nutbolt = tensionCAD.get_nut_bolt_array_models()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    display.DisplayShape(mem, update=True)
    display.DisplayShape(plate, color='BLUE', update=True)
    display.DisplayShape(nutbolt, color='YELLOW', update=True)

    start_display()
