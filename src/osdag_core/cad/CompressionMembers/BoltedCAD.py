"""
Initialized on 12-01-2026
@author: Osdag Team
"""

import numpy
import copy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut


class StrutAngleBoltCAD(object):
    def __init__(self, Obj, member, plate, nut_bolt_array, intermittentConnection):
        """
        :param member: Angle or Channel
        :param plate: Plate
        :param input: input parameters
        :param memb_data: data of the members
        """

        self.Obj = Obj
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

        # Check if plate has attributes directly or in a dictionary
        if hasattr(self.Obj.plate, 'bolt_line'):
            self.col = self.Obj.plate.bolt_line
            self.end = self.Obj.plate.end_dist_provided
            self.pitch = self.Obj.plate.pitch_provided
        else:
            # Fallback for manual assignment if attributes are missing
            # This logic might need to be adjusted based on how parameters are passed
            self.col = getattr(self.Obj, 'bolt_cols', 1) # Default to 1 if not found
            self.end = getattr(self.Obj, 'end_dist', 30)
            self.pitch = getattr(self.Obj, 'pitch', 50)
            
        self.plate_intercept = 2 * self.end + (self.col - 1) * self.pitch
        self.inter_length = self.member.L - 2*(self.end + (self.col -1) * self.pitch)
        # print(self.inter_length)

    def create_3DModel(self):

        self.createMemberGeometry()
        self.createPlateGeometry()
        self.create_nut_bolt_array()

    def createMemberGeometry(self):

        if self.Obj.loc == 'Long Leg':
            if self.Obj.sec_profile == 'Angles':
                member1OriginL = numpy.array([-self.plate_intercept, 0.0, self.member.A / 2])
                member1_uDir = numpy.array([0.0, -1.0, 0.0])
                member1_wDir = numpy.array([1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

            elif self.Obj.sec_profile == 'Back to Back Angles':
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
                member1OriginL = numpy.array([-self.plate_intercept + self.member.L, 0.0, self.member.B / 2])
                member1_uDir = numpy.array([0.0, 0.0, -1.0])
                member1_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

            elif self.Obj.sec_profile == 'Back to Back Angles':
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

        if (self.Obj.sec_profile == 'Back to Back Angles' or self.Obj.sec_profile == 'Back to Back Channels' or self.Obj.sec_profile == 'Star Angles') and self.inter_length > 1000:
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
        if self.Obj.sec_profile == 'Channels' or self.Obj.sec_profile == 'Back to Back Channels':
            self.member.A = self.member.D
            self.member.T = self.member.t
        # nutboltArrayOrigin = self.baseplate.sec_origin + numpy.array([0.0, 0.0, self.baseplate.T /2+ 100])

        if self.Obj.sec_profile == 'Star Angles':
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
            if self.Obj.sec_profile in ['Back to Back Angles', 'Angles']:
                if self.Obj.loc == 'Long Leg':
                    self.placement = self.member.A / 2
                else:
                    self.placement = self.member.B / 2
            else:
                self.placement = self.member.A/2
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
        if self.Obj.sec_profile == 'Star Angles':
            plate = BRepAlgoAPI_Fuse(self.plate1_Model,self.nutboltArrayLModels).Shape()
        else:
            plate = BRepAlgoAPI_Fuse(self.plate1_Model, self.nutboltArrayLModels).Shape()

        # if (self.Obj.sec_profile == 'Back to Back Angles' or self.Obj.sec_profile == 'Back to Back Channels' or self.Obj.sec_profile == 'Star Angles') and self.inter_length > 1000:
        #     plate = BRepAlgoAPI_Fuse(plate, self.inter_conc_plates).Shape()
        return plate

    def get_nut_bolt_array_models(self):

        if self.Obj.sec_profile == 'Star Angles':
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

        if (self.Obj.sec_profile == 'Back to Back Angles' or self.Obj.sec_profile == 'Back to Back Channels' or self.Obj.sec_profile == 'Star Angles') and self.inter_length > 1000:
            array = BRepAlgoAPI_Fuse(array, self.inter_conc_bolts).Shape()

        return array

    def get_end_nut_bolt_array_models(self):

        if self.Obj.sec_profile == 'Star Angles':
            nut_bolts = [self.nutboltArrayLModels, self.nutboltArrayL_SAModels]
            array = nut_bolts[0]
            for comp in nut_bolts:
                array = BRepAlgoAPI_Fuse(comp, array).Shape()
        else:
            array =  self.nutboltArrayLModels

        return array

    def get_only_members_models(self):
        mem = self.get_members_models()
        nut_bolts = self.get_nut_bolt_array_models()

        array = BRepAlgoAPI_Cut(mem, nut_bolts).Shape()

        return array

    def get_models(self):
        mem = self.get_members_models()
        plts = self.get_plates_models()
        nut_bolts = self.get_nut_bolt_array_models()

        array = BRepAlgoAPI_Fuse(mem, plts).Shape()

        array = BRepAlgoAPI_Fuse(array, nut_bolts).Shape()

        return array


class StrutChannelBoltCAD(StrutAngleBoltCAD):

    def createMemberGeometry(self):
        if self.Obj.sec_profile == 'Channels':
            member1OriginL = numpy.array([-self.plate_intercept, -self.member.B, self.member.D / 2])
            member1_uDir = numpy.array([0.0, -1.0, 0.0])
            member1_wDir = numpy.array([1.0, 0.0, 0.0])
            self.member1.place(member1OriginL, member1_uDir, member1_wDir)

            self.member1_Model = self.member1.create_model()

        elif self.Obj.sec_profile == 'Back to Back Channels':
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

        if self.Obj.sec_profile == 'Channels':
            member = self.member1_Model
        elif self.Obj.sec_profile == 'Back to Back Channels':
            member = BRepAlgoAPI_Fuse(self.member1_Model, self.member2_Model).Shape()

        return member
