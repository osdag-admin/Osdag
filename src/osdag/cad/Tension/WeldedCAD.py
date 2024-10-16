"""
Initialized on 23-04-2020
Comenced on
@author: Anand Swaroop
"""

import numpy
import copy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse

class TensionAngleWeldCAD(object):
    def __init__(self, Obj, member, plate, inline_weld, opline_weld, weld_plate_array):
        """
        :param member: Angle or Channel
        :param plate: Plate
        :param weld: weld
        :param input: input parameters
        :param memb_data: data of the members
        """

        self.Obj = Obj
        self.member = member
        self.plate = plate
        self.inline_weld = inline_weld
        self.opline_weld = opline_weld
        self.intermittentConnection = weld_plate_array

        # self.Obj.loc = 'Long Leg'#'Short Leg'

        self.plate1 = copy.deepcopy(self.plate)
        self.plate2 = copy.deepcopy(self.plate)

        self.member1 = copy.deepcopy(self.member)
        self.member2 = copy.deepcopy(self.member)
        # self.member2 = copy.deepcopy(self.member)

        # front side member
        self.weldHL11 = copy.deepcopy(self.inline_weld)  # weld horizontal left side 1 (top side of member)
        self.weldHL12 = copy.deepcopy(self.inline_weld)  # weld horzontal left side 2 (bottom side of member)
        self.weldHR11 = copy.deepcopy(self.inline_weld)
        self.weldHR12 = copy.deepcopy(self.inline_weld)

        self.weldVL11 = copy.deepcopy(self.opline_weld)  # weld vertical left side
        self.weldVR11 = copy.deepcopy(self.opline_weld)  # weld vertical right side

        # for B2B members, back side member
        self.weldHL21 = copy.deepcopy(self.inline_weld)  # weld horizontal left side 1 (top side of member)
        self.weldHL22 = copy.deepcopy(self.inline_weld)  # weld horzontal left side 2 (bottom side of member)
        self.weldHR21 = copy.deepcopy(self.inline_weld)
        self.weldHR22 = copy.deepcopy(self.inline_weld)

        self.weldVL21 = copy.deepcopy(self.opline_weld)  # weld vertical left side
        self.weldVR21 = copy.deepcopy(self.opline_weld)  # weld vertical right side

        self.s = max(15, self.inline_weld.h)
        self.plate_intercept = self.plate.L - self.s - 50
        self.inter_length = self.member.L - 2*(self.plate.L - 50)

    def create_3DModel(self):

        self.createMemberGeometry()
        self.createPlateGeometry()
        self.createWeldGeometry()

    def createMemberGeometry(self):

        if self.Obj.loc == 'Long Leg':
            if self.Obj.sec_profile == 'Angles':
                member1OriginL = numpy.array([-self.plate_intercept, 0.0, self.opline_weld.L / 2])
                member1_uDir = numpy.array([0.0, -1.0, 0.0])
                member1_wDir = numpy.array([1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

            elif self.Obj.sec_profile == 'Back to Back Angles':
                member1OriginL = numpy.array([-self.plate_intercept, 0.0, self.opline_weld.L / 2])
                member1_uDir = numpy.array([0.0, -1.0, 0.0])
                member1_wDir = numpy.array([1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

                member2OriginL = numpy.array(
                    [self.member.L - self.plate_intercept, self.plate.T, self.opline_weld.L / 2])
                member2_uDir = numpy.array([0.0, 1.0, 0.0])
                member2_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.member2.place(member2OriginL, member2_uDir, member2_wDir)

                self.member2_Model = self.member2.create_model()

            elif self.Obj.sec_profile == 'Star Angles':
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
            if self.Obj.sec_profile == 'Angles':
                member1OriginL = numpy.array([-self.plate_intercept + self.member.L, 0.0, self.opline_weld.L / 2])
                member1_uDir = numpy.array([0.0, 0.0, -1.0])
                member1_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

            elif self.Obj.sec_profile == 'Back to Back Angles':
                member1OriginL = numpy.array([-self.plate_intercept + self.member.L, 0.0, self.opline_weld.L / 2])
                member1_uDir = numpy.array([0.0, 0.0, -1.0])
                member1_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

                member2OriginL = numpy.array([- self.plate_intercept, self.plate.T, self.opline_weld.L / 2])
                member2_uDir = numpy.array([0.0, 0.0, -1.0])
                member2_wDir = numpy.array([1.0, 0.0, 0.0])
                self.member2.place(member2OriginL, member2_uDir, member2_wDir)

                self.member2_Model = self.member2.create_model()

            elif self.Obj.sec_profile == 'Star Angles':
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

        if (self.Obj.sec_profile== 'Back to Back Angles' or self.Obj.sec_profile== 'Back to Back Channels' or self.Obj.sec_profile== 'Star Angles') and self.inter_length > 1000:
            intermittentConnectionOriginL = numpy.array([0, 0.0, 0.0])
            intermittentConnection_uDir = numpy.array([1.0, 0.0, 0.0])
            intermittentConnection_vDir = numpy.array([0.0, 1.0, 0.0])
            intermittentConnection_wDir = numpy.array([0.0, 0.0, 1.0])
            self.intermittentConnection.place(intermittentConnectionOriginL, intermittentConnection_uDir,
                                              intermittentConnection_vDir, intermittentConnection_wDir)

            self.intermittentConnection_Model = self.intermittentConnection.create_model()
            self.inter_conc_welds = self.intermittentConnection.get_welded_models()
            self.inter_conc_plates = self.intermittentConnection.get_plate_models()

    def createWeldGeometry(self):
        if self.Obj.sec_profile == 'Back to Back Angles' or self.Obj.sec_profile == 'Angles' or self.Obj.sec_profile == 'Channels' or self.Obj.sec_profile == 'Back to Back Channels':
            weldHL11OriginL = numpy.array([-self.plate_intercept, 0.0, self.opline_weld.L / 2])
            weldHL11_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHL11_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHL11.place(weldHL11OriginL, weldHL11_uDir, weldHL11_wDir)

            self.weldHL11_Model = self.weldHL11.create_model()

            weldHL12OriginL = numpy.array([0.0, 0.0, -self.opline_weld.L / 2])
            weldHL12_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHL12_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHL12.place(weldHL12OriginL, weldHL12_uDir, weldHL12_wDir)

            self.weldHL12_Model = self.weldHL12.create_model()

            weldHR11OriginL = numpy.array([-2 * self.plate_intercept + self.member.L, 0.0, self.opline_weld.L / 2])
            weldHR11_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHR11_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHR11.place(weldHR11OriginL, weldHR11_uDir, weldHR11_wDir)

            self.weldHR11_Model = self.weldHR11.create_model()

            weldHR12OriginL = numpy.array([-self.plate_intercept + self.member.L, 0.0, -self.opline_weld.L / 2])
            weldHR12_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHR12_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHR12.place(weldHR12OriginL, weldHR12_uDir, weldHR12_wDir)

            self.weldHR12_Model = self.weldHR12.create_model()

            weldVL11OriginL = numpy.array([-self.plate_intercept, 0.0, -self.opline_weld.L / 2])
            weldVL11_uDir = numpy.array([-1.0, 0.0, 0.0])
            weldVL11_wDir = numpy.array([0.0, 0.0, 1.0])
            self.weldVL11.place(weldVL11OriginL, weldVL11_uDir, weldVL11_wDir)

            self.weldVL11_Model = self.weldVL11.create_model()

            weldVR11OriginL = numpy.array([-self.plate_intercept + self.member.L, 0.0, self.opline_weld.L / 2])
            weldVR11_uDir = numpy.array([1.0, 0.0, 0.0])
            weldVR11_wDir = numpy.array([0.0, 0.0, -1.0])
            self.weldVR11.place(weldVR11OriginL, weldVR11_uDir, weldVR11_wDir)

            self.weldVR11_Model = self.weldVR11.create_model()

        if self.Obj.sec_profile == 'Back to Back Angles' or self.Obj.sec_profile == 'Back to Back Channels':
            weldHL21OriginL = numpy.array([0.0, self.plate.T, self.opline_weld.L / 2])
            weldHL21_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHL21_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHL21.place(weldHL21OriginL, weldHL21_uDir, weldHL21_wDir)

            self.weldHL21_Model = self.weldHL21.create_model()

            weldHL22OriginL = numpy.array([- self.plate_intercept, self.plate.T, -self.opline_weld.L / 2])
            weldHL22_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHL22_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHL22.place(weldHL22OriginL, weldHL22_uDir, weldHL22_wDir)

            self.weldHL22_Model = self.weldHL22.create_model()

            weldHR21OriginL = numpy.array(
                [- self.plate_intercept + self.member.L, self.plate.T, self.opline_weld.L / 2])
            weldHR21_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHR21_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHR21.place(weldHR21OriginL, weldHR21_uDir, weldHR21_wDir)

            self.weldHR21_Model = self.weldHR21.create_model()

            weldHR22OriginL = numpy.array(
                [-2 * self.plate_intercept + self.member.L, self.plate.T, -self.opline_weld.L / 2])
            weldHR22_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHR22_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHR22.place(weldHR22OriginL, weldHR22_uDir, weldHR22_wDir)

            self.weldHR22_Model = self.weldHR22.create_model()

            weldVL21OriginL = numpy.array([-self.plate_intercept, self.plate.T, self.opline_weld.L / 2])
            weldVL21_uDir = numpy.array([-1.0, 0.0, 0.0])
            weldVL21_wDir = numpy.array([0.0, 0.0, -1.0])
            self.weldVL21.place(weldVL21OriginL, weldVL21_uDir, weldVL21_wDir)

            self.weldVL21_Model = self.weldVL21.create_model()

            weldVR21OriginL = numpy.array(
                [-self.plate_intercept + self.member.L, self.plate.T, -self.opline_weld.L / 2])
            weldVR21_uDir = numpy.array([1.0, 0.0, 0.0])
            weldVR21_wDir = numpy.array([0.0, 0.0, 1.0])
            self.weldVR21.place(weldVR21OriginL, weldVR21_uDir, weldVR21_wDir)

            self.weldVR21_Model = self.weldVR21.create_model()

        elif self.Obj.sec_profile == 'Star Angles':

            weldHL11OriginL = numpy.array([-self.plate_intercept, 0.0, 0.0])
            weldHL11_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHL11_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHL11.place(weldHL11OriginL, weldHL11_uDir, weldHL11_wDir)

            self.weldHL11_Model = self.weldHL11.create_model()

            weldHL12OriginL = numpy.array([0.0, 0.0, -self.opline_weld.L])
            weldHL12_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHL12_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHL12.place(weldHL12OriginL, weldHL12_uDir, weldHL12_wDir)

            self.weldHL12_Model = self.weldHL12.create_model()

            weldHR11OriginL = numpy.array([-2 * self.plate_intercept + self.member.L, 0.0, 0.0])
            weldHR11_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHR11_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHR11.place(weldHR11OriginL, weldHR11_uDir, weldHR11_wDir)

            self.weldHR11_Model = self.weldHR11.create_model()

            weldHR12OriginL = numpy.array([-self.plate_intercept + self.member.L, 0.0, -self.opline_weld.L])
            weldHR12_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHR12_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHR12.place(weldHR12OriginL, weldHR12_uDir, weldHR12_wDir)

            self.weldHR12_Model = self.weldHR12.create_model()

            weldVL11OriginL = numpy.array([-self.plate_intercept, 0.0, -self.opline_weld.L])
            weldVL11_uDir = numpy.array([-1.0, 0.0, 0.0])
            weldVL11_wDir = numpy.array([0.0, 0.0, 1.0])
            self.weldVL11.place(weldVL11OriginL, weldVL11_uDir, weldVL11_wDir)

            self.weldVL11_Model = self.weldVL11.create_model()

            weldVR11OriginL = numpy.array([-self.plate_intercept + self.member.L, 0.0, 0.0])
            weldVR11_uDir = numpy.array([1.0, 0.0, 0.0])
            weldVR11_wDir = numpy.array([0.0, 0.0, -1.0])
            self.weldVR11.place(weldVR11OriginL, weldVR11_uDir, weldVR11_wDir)

            self.weldVR11_Model = self.weldVR11.create_model()

            weldHL21OriginL = numpy.array([0.0, self.plate.T, self.opline_weld.L])
            weldHL21_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHL21_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHL21.place(weldHL21OriginL, weldHL21_uDir, weldHL21_wDir)

            self.weldHL21_Model = self.weldHL21.create_model()

            weldHL22OriginL = numpy.array([- self.plate_intercept, self.plate.T, 0.0])
            weldHL22_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHL22_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHL22.place(weldHL22OriginL, weldHL22_uDir, weldHL22_wDir)

            self.weldHL22_Model = self.weldHL22.create_model()

            weldHR21OriginL = numpy.array([-self.plate_intercept + self.member.L, self.plate.T, self.opline_weld.L])
            weldHR21_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHR21_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHR21.place(weldHR21OriginL, weldHR21_uDir, weldHR21_wDir)

            self.weldHR21_Model = self.weldHR21.create_model()

            weldHR22OriginL = numpy.array([-2 * self.plate_intercept + self.member.L, self.plate.T, 0.0])
            weldHR22_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHR22_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHR22.place(weldHR22OriginL, weldHR22_uDir, weldHR22_wDir)

            self.weldHR22_Model = self.weldHR22.create_model()

            weldVL21OriginL = numpy.array([-self.plate_intercept, self.plate.T, self.opline_weld.L])
            weldVL21_uDir = numpy.array([-1.0, 0.0, 0.0])
            weldVL21_wDir = numpy.array([0.0, 0.0, -1.0])
            self.weldVL21.place(weldVL21OriginL, weldVL21_uDir, weldVL21_wDir)

            self.weldVL21_Model = self.weldVL21.create_model()

            weldVR21OriginL = numpy.array([-self.plate_intercept + self.member.L, self.plate.T, 0.0])
            weldVR21_uDir = numpy.array([1.0, 0.0, 0.0])
            weldVR21_wDir = numpy.array([0.0, 0.0, 1.0])
            self.weldVR21.place(weldVR21OriginL, weldVR21_uDir, weldVR21_wDir)

            self.weldVR21_Model = self.weldVR21.create_model()


    def get_members_models(self):

        if self.Obj.sec_profile == 'Angles':
            member = self.member1_Model

        else:
            member = BRepAlgoAPI_Fuse(self.member1_Model, self.member2_Model).Shape()

        return member

    def get_plates_models(self):
        plate = BRepAlgoAPI_Fuse(self.plate1_Model, self.plate2_Model).Shape()
        if (self.Obj.sec_profile == 'Back to Back Angles' or self.Obj.sec_profile == 'Back to Back Channels' or self.Obj.sec_profile == 'Star Angles') and self.inter_length > 1000:
            plate = BRepAlgoAPI_Fuse(plate, self.inter_conc_plates).Shape()
        return plate

    def get_end_plates_models(self):
        plate = self.plate1_Model
        # if (self.Obj.sec_profile == 'Back to Back Angles' or self.Obj.sec_profile == 'Back to Back Channels' or self.Obj.sec_profile == 'Star Angles') and self.inter_length > 1000:
        #     plate = BRepAlgoAPI_Fuse(plate, self.inter_conc_plates).Shape()
        return plate


    def get_welded_models(self):

        if self.Obj.sec_profile == 'Angles' or self.Obj.sec_profile == 'Channels':
            welded_sec = [self.weldHL11_Model, self.weldHL12_Model, self.weldHR11_Model, self.weldHR12_Model,
                          self.weldVL11_Model, self.weldVR11_Model]
        elif (self.Obj.sec_profile== 'Back to Back Angles' or self.Obj.sec_profile== 'Back to Back Channels' or self.Obj.sec_profile== 'Star Angles') and self.inter_length > 1000:
            welded_sec = [self.weldHL11_Model, self.weldHL12_Model, self.weldHR11_Model, self.weldHR12_Model,
                          self.weldVL11_Model, self.weldVR11_Model, self.weldHL21_Model, self.weldHL22_Model,
                          self.weldHR21_Model, self.weldHR22_Model, self.weldVL21_Model, self.weldVR21_Model,
                          self.inter_conc_welds]
        else:
            welded_sec = [self.weldHL11_Model, self.weldHL12_Model, self.weldHR11_Model, self.weldHR12_Model,
                          self.weldVL11_Model, self.weldVR11_Model, self.weldHL21_Model, self.weldHL22_Model,
                          self.weldHR21_Model, self.weldHR22_Model, self.weldVL21_Model, self.weldVR21_Model]
        welds = welded_sec[0]
        for comp in welded_sec[1:]:
            welds = BRepAlgoAPI_Fuse(comp, welds).Shape()
        return welds

    def get_models(self):
        mem = self.get_welded_models()
        plts = self.get_plates_models()
        wlds = self.get_welded_models()

        array = BRepAlgoAPI_Fuse(mem, plts).Shape()

        array = BRepAlgoAPI_Fuse(array, wlds).Shape()

        return array
class TensionChannelWeldCAD(TensionAngleWeldCAD):

    def createMemberGeometry(self):
        if self.Obj.sec_profile == 'Channels':
            member1OriginL = numpy.array([-self.plate_intercept, -self.member.B, self.opline_weld.L / 2])
            member1_uDir = numpy.array([0.0, -1.0, 0.0])
            member1_wDir = numpy.array([1.0, 0.0, 0.0])
            self.member1.place(member1OriginL, member1_uDir, member1_wDir)

            self.member1_Model = self.member1.create_model()

        elif self.Obj.sec_profile == 'Back to Back Channels':
            member1OriginL = numpy.array([-self.plate_intercept, -self.member.B, self.opline_weld.L / 2])
            member1_uDir = numpy.array([0.0, -1.0, 0.0])
            member1_wDir = numpy.array([1.0, 0.0, 0.0])
            self.member1.place(member1OriginL, member1_uDir, member1_wDir)

            self.member1_Model = self.member1.create_model()

            member2OriginL = numpy.array(
                [self.member.L - self.plate_intercept, self.plate.T + self.member.B, self.opline_weld.L / 2])
            member2_uDir = numpy.array([0.0, 1.0, 0.0])
            member2_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.member2.place(member2OriginL, member2_uDir, member2_wDir)

            self.member2_Model = self.member2.create_model()


    def get_members_models(self):

        if self.Obj.sec_profile == 'Channels':
            member = self.member1_Model
        elif self.Obj.sec_profile == 'Back to Back Channels':
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

    member_data = 'Star Angles'  # 'Back to Back Angles' #'Angles' #''Back to Back Channels'#'Channels' #  #
    loc = 'Long Leg'  # 'Short Leg'#
    weld_size = 6
    s = max(15, weld_size)

    if member_data == 'Channels' or member_data == 'Back to Back Channels':
        member = Channel(B=75, T=10.2, D=175, t=6, R1=0, R2=0, L=5000)
        plate = GassetPlate(L=560 + 50, H=210, T=16, degree=30)
        plate_intercept = plate.L - s - 50
        inline_weld = FilletWeld(b=weld_size, h=weld_size, L=plate_intercept)
        opline_weld = FilletWeld(b=weld_size, h=weld_size, L=member.D)

        tensionCAD = TensionChannelWeldCAD(member_data, member, plate, inline_weld, opline_weld)


    else:
        member = Angle(L=2000.0, A=70.0, B=20.0, T=5.0, R1=0.0, R2=0.0)
        plate = GassetPlate(L=540 + 50, H=255, T=5, degree=30)
        plate_intercept = plate.L - s - 50
        inline_weld = FilletWeld(b=weld_size, h=weld_size, L=plate_intercept)
        if loc == 'Long Leg':
            opline_weld = FilletWeld(b=weld_size, h=weld_size, L=member.A)
        else:
            opline_weld = FilletWeld(b=weld_size, h=weld_size, L=member.B)

        tensionCAD = TensionAngleWeldCAD(member_data, member, plate, inline_weld, opline_weld)

    tensionCAD.create_3DModel()
    plate = tensionCAD.get_plates_models()
    mem = tensionCAD.get_members_models()
    welds = tensionCAD.get_welded_models()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    display.DisplayShape(mem, update=True)
    display.DisplayShape(plate, color='BLUE', update=True)
    display.DisplayShape(welds, color='Red', update=True)

    start_display()
