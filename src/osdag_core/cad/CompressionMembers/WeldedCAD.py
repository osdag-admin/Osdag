"""
Initialized on 23-04-2020
Comenced on
@author: Anand Swaroop
"""

import numpy
import copy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse

class StrutAngleWeldCAD(object):
    def __init__(self, Obj, member, plate, inline_weld_toe, inline_weld_heel, opline_weld, weld_plate_array):

        self.Obj = Obj
        self.member = member
        self.plate = plate
        self.inline_weld_toe = inline_weld_toe
        self.inline_weld_heel = inline_weld_heel
        self.opline_weld = opline_weld
        self.intermittentConnection = weld_plate_array

        # self.Obj.loc = 'Long Leg'#'Short Leg'

        self.plate1 = copy.deepcopy(self.plate)
        self.plate2 = copy.deepcopy(self.plate)

        self.member1 = copy.deepcopy(self.member)
        self.member2 = copy.deepcopy(self.member)

        self.weldHL11 = copy.deepcopy(self.inline_weld_heel)
        self.weldHL12 = copy.deepcopy(self.inline_weld_toe)
        self.weldHR11 = copy.deepcopy(self.inline_weld_heel)
        self.weldHR12 = copy.deepcopy(self.inline_weld_toe)

        self.weldVL11 = copy.deepcopy(self.opline_weld)
        self.weldVR11 = copy.deepcopy(self.opline_weld)

        self.weldHL21 = copy.deepcopy(self.inline_weld_heel)
        self.weldHL22 = copy.deepcopy(self.inline_weld_toe)
        self.weldHR21 = copy.deepcopy(self.inline_weld_heel)
        self.weldHR22 = copy.deepcopy(self.inline_weld_toe)

        self.weldVL21 = copy.deepcopy(self.opline_weld)
        self.weldVR21 = copy.deepcopy(self.opline_weld)

        self.s = max(15, self.inline_weld_toe.h)
        self.plate_intercept = self.inline_weld_heel.L
        self.inter_length = self.member.L - 2 * (self.plate.L - 50)

    def create_3DModel(self):

        self.createMemberGeometry()
        self.createPlateGeometry()
        self.createWeldGeometry()

    def createMemberGeometry(self):

        if self.Obj.loc == 'Long Leg':
            if 'Angles' in self.Obj.sec_profile and 'Back to Back' not in self.Obj.sec_profile and 'Star' not in self.Obj.sec_profile:
                member1OriginL = numpy.array([-self.plate_intercept, 0.0, self.opline_weld.L / 2])
                member1_uDir = numpy.array([0.0, -1.0, 0.0])
                member1_wDir = numpy.array([1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

            elif 'Back to Back Angles' in self.Obj.sec_profile:
                # Member 1 — same as always
                member1OriginL = numpy.array([-self.plate_intercept, 0.0, self.opline_weld.L / 2])
                member1_uDir = numpy.array([0.0, -1.0, 0.0])
                member1_wDir = numpy.array([1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)
                self.member1_Model = self.member1.create_model()

                # Member 2 — z is NEGATIVE (opposite side of gusset)
                member2OriginL = numpy.array(
                    [self.member.L - self.plate_intercept, self.plate.T, self.opline_weld.L / 2])
                member2_uDir = numpy.array([0.0, 1.0, 0.0])
                member2_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.member2.place(member2OriginL, member2_uDir, member2_wDir)
                self.member2_Model = self.member2.create_model()

            elif 'Star Angles' in self.Obj.sec_profile:
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
                # Default fallback for single Angles
                member1OriginL = numpy.array([-self.plate_intercept, 0.0, self.opline_weld.L / 2])
                member1_uDir = numpy.array([0.0, -1.0, 0.0])
                member1_wDir = numpy.array([1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

        else:
            if 'Angles' in self.Obj.sec_profile and 'Back to Back' not in self.Obj.sec_profile and 'Star' not in self.Obj.sec_profile:
                member1OriginL = numpy.array([-self.plate_intercept + self.member.L, 0.0, self.opline_weld.L / 2])
                member1_uDir = numpy.array([0.0, 0.0, -1.0])
                member1_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

            elif 'Back to Back Angles' in self.Obj.sec_profile:
                member1OriginL = numpy.array([-self.plate_intercept + self.member.L, 0.0, self.opline_weld.L / 2])
                member1_uDir = numpy.array([0.0, 0.0, -1.0])
                member1_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)
                self.member1_Model = self.member1.create_model()

                # Member 2 — z is NEGATIVE (opposite side of gusset)
                member2OriginL = numpy.array(
                    [-self.plate_intercept, self.plate.T, -self.opline_weld.L / 2])
                member2_uDir = numpy.array([0.0, 0.0, -1.0])
                member2_wDir = numpy.array([1.0, 0.0, 0.0])
                self.member2.place(member2OriginL, member2_uDir, member2_wDir)
                self.member2_Model = self.member2.create_model()


            elif 'Star Angles' in self.Obj.sec_profile:
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
            else:
                # Default fallback for single Angles
                member1OriginL = numpy.array([-self.plate_intercept + self.member.L, 0.0, self.opline_weld.L / 2])
                member1_uDir = numpy.array([0.0, 0.0, -1.0])
                member1_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.member1.place(member1OriginL, member1_uDir, member1_wDir)

                self.member1_Model = self.member1.create_model()

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

        if (('Back to Back Angles' in self.Obj.sec_profile
             or 'Back to Back Channels' in self.Obj.sec_profile
             or 'Star Angles' in self.Obj.sec_profile)
                and self.inter_length > 1000):

            ic_weld_size = self.intermittentConnection.weld.h \
                if hasattr(self.intermittentConnection, 'weld') \
                else 0.0
            ic_plate_width = self.intermittentConnection.plate.W \
                if hasattr(self.intermittentConnection, 'plate') \
                else 0.0

            if ic_weld_size > 0 and ic_plate_width > 0:
                ic_origin = numpy.array([0.0, 0.0, 0.0])
                ic_uDir = numpy.array([1.0, 0.0, 0.0])
                ic_vDir = numpy.array([0.0, 1.0, 0.0])
                ic_wDir = numpy.array([0.0, 0.0, 1.0])
                self.intermittentConnection.place(ic_origin, ic_uDir, ic_vDir, ic_wDir)
                self.intermittentConnection_Model = self.intermittentConnection.create_model()
                self.inter_conc_welds = self.intermittentConnection.get_welded_models()
                self.inter_conc_plates = self.intermittentConnection.get_plate_models()
            else:
                # Intermittent data not available — treat as if inter_length <= 1000
                self.inter_length = 0

    def createWeldGeometry(self):
        if ('Angles' in self.Obj.sec_profile
                or 'Channels' in self.Obj.sec_profile):

            # Left end — TOP flange (HEEL, longer)
            weldHL11OriginL = numpy.array([
                -self.plate_intercept, 0.0, self.opline_weld.L / 2
            ])
            weldHL11_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHL11_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHL11.place(weldHL11OriginL, weldHL11_uDir, weldHL11_wDir)
            self.weldHL11_Model = self.weldHL11.create_model()

            # Left end — BOTTOM flange (TOE, shorter)
            weldHL12OriginL = numpy.array([
                -self.plate_intercept + self.inline_weld_toe.L,
                0.0,
                -self.opline_weld.L / 2
            ])
            weldHL12_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHL12_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHL12.place(weldHL12OriginL, weldHL12_uDir, weldHL12_wDir)
            self.weldHL12_Model = self.weldHL12.create_model()

            # Right end — TOP flange (HEEL, longer)
            weldHR11OriginL = numpy.array([
                -self.plate_intercept + self.member.L - self.inline_weld_heel.L,
                0.0,
                self.opline_weld.L / 2
            ])
            weldHR11_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHR11_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHR11.place(weldHR11OriginL, weldHR11_uDir, weldHR11_wDir)
            self.weldHR11_Model = self.weldHR11.create_model()

            # Right end — BOTTOM flange (TOE, shorter)
            weldHR12OriginL = numpy.array([
                -self.plate_intercept + self.member.L,
                0.0,
                -self.opline_weld.L / 2
            ])
            weldHR12_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHR12_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHR12.place(weldHR12OriginL, weldHR12_uDir, weldHR12_wDir)
            self.weldHR12_Model = self.weldHR12.create_model()

            # Left transverse (opline) weld
            weldVL11OriginL = numpy.array([
                -self.plate_intercept, 0.0, -self.opline_weld.L / 2
            ])
            weldVL11_uDir = numpy.array([-1.0, 0.0, 0.0])
            weldVL11_wDir = numpy.array([0.0, 0.0, 1.0])
            self.weldVL11.place(weldVL11OriginL, weldVL11_uDir, weldVL11_wDir)
            self.weldVL11_Model = self.weldVL11.create_model()

            # Right transverse (opline) weld
            weldVR11OriginL = numpy.array([
                -self.plate_intercept + self.member.L,
                0.0,
                self.opline_weld.L / 2
            ])
            weldVR11_uDir = numpy.array([1.0, 0.0, 0.0])
            weldVR11_wDir = numpy.array([0.0, 0.0, -1.0])
            self.weldVR11.place(weldVR11OriginL, weldVR11_uDir, weldVR11_wDir)
            self.weldVR11_Model = self.weldVR11.create_model()

        elif 'Star Angles' in self.Obj.sec_profile:

            # ---- Member 1, near face (y = 0) ----

            # Left end — TOP (HEEL)
            weldHL11OriginL = numpy.array([
                -self.plate_intercept, 0.0, 0.0
            ])
            weldHL11_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHL11_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHL11.place(weldHL11OriginL, weldHL11_uDir, weldHL11_wDir)
            self.weldHL11_Model = self.weldHL11.create_model()

            # Left end — BOTTOM (TOE)
            weldHL12OriginL = numpy.array([
                -self.plate_intercept + self.inline_weld_toe.L,
                0.0,
                -self.opline_weld.L
            ])
            weldHL12_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHL12_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHL12.place(weldHL12OriginL, weldHL12_uDir, weldHL12_wDir)
            self.weldHL12_Model = self.weldHL12.create_model()

            # Right end — TOP (HEEL)
            weldHR11OriginL = numpy.array([
                -self.plate_intercept + self.member.L - self.inline_weld_heel.L,
                0.0,
                0.0
            ])
            weldHR11_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHR11_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHR11.place(weldHR11OriginL, weldHR11_uDir, weldHR11_wDir)
            self.weldHR11_Model = self.weldHR11.create_model()

            # Right end — BOTTOM (TOE)
            weldHR12OriginL = numpy.array([
                -self.plate_intercept + self.member.L,
                0.0,
                -self.opline_weld.L
            ])
            weldHR12_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHR12_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHR12.place(weldHR12OriginL, weldHR12_uDir, weldHR12_wDir)
            self.weldHR12_Model = self.weldHR12.create_model()

            # Left opline (member 1)
            weldVL11OriginL = numpy.array([
                -self.plate_intercept, 0.0, -self.opline_weld.L
            ])
            weldVL11_uDir = numpy.array([-1.0, 0.0, 0.0])
            weldVL11_wDir = numpy.array([0.0, 0.0, 1.0])
            self.weldVL11.place(weldVL11OriginL, weldVL11_uDir, weldVL11_wDir)
            self.weldVL11_Model = self.weldVL11.create_model()

            # Right opline (member 1)
            weldVR11OriginL = numpy.array([
                -self.plate_intercept + self.member.L, 0.0, 0.0
            ])
            weldVR11_uDir = numpy.array([1.0, 0.0, 0.0])
            weldVR11_wDir = numpy.array([0.0, 0.0, -1.0])
            self.weldVR11.place(weldVR11OriginL, weldVR11_uDir, weldVR11_wDir)
            self.weldVR11_Model = self.weldVR11.create_model()

            # ---- Member 2, far face (y = plate.T), reversed in x ----
            # Heel end of member 2 is at the LEFT side of the gusset.

            # Left end — TOP (HEEL, mirrored)
            weldHL21OriginL = numpy.array([
                -self.plate_intercept + self.inline_weld_heel.L,
                self.plate.T + self.inline_weld_toe.h,
                self.opline_weld.L
            ])
            weldHL21_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHL21_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHL21.place(weldHL21OriginL, weldHL21_uDir, weldHL21_wDir)
            self.weldHL21_Model = self.weldHL21.create_model()

            # Left end — BOTTOM (TOE, mirrored)
            weldHL22OriginL = numpy.array([
                -self.plate_intercept, self.plate.T, 0.0
            ])
            weldHL22_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHL22_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHL22.place(weldHL22OriginL, weldHL22_uDir, weldHL22_wDir)
            self.weldHL22_Model = self.weldHL22.create_model()

            # Right end — TOP (HEEL, mirrored)
            weldHR21OriginL = numpy.array([
                -self.plate_intercept + self.member.L,
                self.plate.T + self.inline_weld_toe.h,
                self.opline_weld.L
            ])
            weldHR21_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHR21_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHR21.place(weldHR21OriginL, weldHR21_uDir, weldHR21_wDir)
            self.weldHR21_Model = self.weldHR21.create_model()

            # Right end — BOTTOM (TOE, mirrored)
            weldHR22OriginL = numpy.array([
                -self.plate_intercept + self.member.L - self.inline_weld_heel.L,
                self.plate.T,
                0.0
            ])
            weldHR22_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHR22_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHR22.place(weldHR22OriginL, weldHR22_uDir, weldHR22_wDir)
            self.weldHR22_Model = self.weldHR22.create_model()

            # Left opline (member 2)
            weldVL21OriginL = numpy.array([
                -self.plate_intercept, self.plate.T, self.opline_weld.L
            ])
            weldVL21_uDir = numpy.array([-1.0, 0.0, 0.0])
            weldVL21_wDir = numpy.array([0.0, 0.0, -1.0])
            self.weldVL21.place(weldVL21OriginL, weldVL21_uDir, weldVL21_wDir)
            self.weldVL21_Model = self.weldVL21.create_model()

            # Right opline (member 2)
            weldVR21OriginL = numpy.array([
                -self.plate_intercept + self.member.L, self.plate.T, 0.0
            ])
            weldVR21_uDir = numpy.array([1.0, 0.0, 0.0])
            weldVR21_wDir = numpy.array([0.0, 0.0, 1.0])
            self.weldVR21.place(weldVR21OriginL, weldVR21_uDir, weldVR21_wDir)
            self.weldVR21_Model = self.weldVR21.create_model()

        if ('Back to Back Angles' in self.Obj.sec_profile
                or 'Back to Back Channels' in self.Obj.sec_profile):
            # Left end — TOP (HEEL, reversed member 2)
            weldHL21OriginL = numpy.array([
                -self.plate_intercept + self.inline_weld_heel.L,
                self.plate.T,
                self.opline_weld.L / 2
            ])
            weldHL21_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHL21_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHL21.place(weldHL21OriginL, weldHL21_uDir, weldHL21_wDir)
            self.weldHL21_Model = self.weldHL21.create_model()

            # Left end — BOTTOM (TOE, reversed member 2)
            weldHL22OriginL = numpy.array([
                -self.plate_intercept,
                self.plate.T,
                -self.opline_weld.L / 2
            ])
            weldHL22_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHL22_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHL22.place(weldHL22OriginL, weldHL22_uDir, weldHL22_wDir)
            self.weldHL22_Model = self.weldHL22.create_model()

            # Right end — TOP (HEEL, reversed member 2 toe side)
            weldHR21OriginL = numpy.array([
                -self.plate_intercept + self.member.L,
                self.plate.T,
                self.opline_weld.L / 2
            ])
            weldHR21_uDir = numpy.array([0.0, 0.0, 1.0])
            weldHR21_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weldHR21.place(weldHR21OriginL, weldHR21_uDir, weldHR21_wDir)
            self.weldHR21_Model = self.weldHR21.create_model()

            # Right end — BOTTOM (TOE, reversed member 2 toe side)
            weldHR22OriginL = numpy.array([
                -self.plate_intercept + self.member.L - self.inline_weld_toe.L,
                self.plate.T,
                -self.opline_weld.L / 2
            ])
            weldHR22_uDir = numpy.array([0.0, 0.0, -1.0])
            weldHR22_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weldHR22.place(weldHR22OriginL, weldHR22_uDir, weldHR22_wDir)
            self.weldHR22_Model = self.weldHR22.create_model()

            # Left opline (member 2)
            weldVL21OriginL = numpy.array([
                -self.plate_intercept,
                self.plate.T,
                self.opline_weld.L / 2
            ])
            weldVL21_uDir = numpy.array([-1.0, 0.0, 0.0])
            weldVL21_wDir = numpy.array([0.0, 0.0, -1.0])
            self.weldVL21.place(weldVL21OriginL, weldVL21_uDir, weldVL21_wDir)
            self.weldVL21_Model = self.weldVL21.create_model()

            # Right opline (member 2)
            weldVR21OriginL = numpy.array([
                -self.plate_intercept + self.member.L,
                self.plate.T,
                -self.opline_weld.L / 2
            ])
            weldVR21_uDir = numpy.array([1.0, 0.0, 0.0])
            weldVR21_wDir = numpy.array([0.0, 0.0, 1.0])
            self.weldVR21.place(weldVR21OriginL, weldVR21_uDir, weldVR21_wDir)
            self.weldVR21_Model = self.weldVR21.create_model()


    def get_members_models(self):

        if 'Angles' in self.Obj.sec_profile and 'Back to Back' not in self.Obj.sec_profile and 'Star' not in self.Obj.sec_profile:
            member = self.member1_Model
        elif hasattr(self, 'member2_Model'):
            member = BRepAlgoAPI_Fuse(self.member1_Model, self.member2_Model).Shape()
        else:
            member = self.member1_Model

        return member

    def get_only_members_models(self):

        if 'Angles' in self.Obj.sec_profile and 'Back to Back' not in self.Obj.sec_profile and 'Star' not in self.Obj.sec_profile:
            member = self.member1_Model
        elif hasattr(self, 'member2_Model'):
            member = BRepAlgoAPI_Fuse(self.member1_Model, self.member2_Model).Shape()
        else:
            member = self.member1_Model

        return member


    def get_plates_models(self):
        plate = BRepAlgoAPI_Fuse(self.plate1_Model, self.plate2_Model).Shape()
        if ('Back to Back Angles' in self.Obj.sec_profile or 'Back to Back Channels' in self.Obj.sec_profile or 'Star Angles' in self.Obj.sec_profile) and self.inter_length > 1000:
            plate = BRepAlgoAPI_Fuse(plate, self.inter_conc_plates).Shape()
        return plate

    def get_end_plates_models(self):
        plate = self.plate1_Model
        # if (self.Obj.sec_profile == 'Back to Back Angles' or self.Obj.sec_profile == 'Back to Back Channels' or self.Obj.sec_profile == 'Star Angles') and self.inter_length > 1000:
        #     plate = BRepAlgoAPI_Fuse(plate, self.inter_conc_plates).Shape()
        return plate


    def get_welded_models(self):

        if ('Angles' in self.Obj.sec_profile and 'Back to Back' not in self.Obj.sec_profile) or 'Channels' in self.Obj.sec_profile:
            welded_sec = [self.weldHL11_Model, self.weldHL12_Model, self.weldHR11_Model, self.weldHR12_Model,
                          self.weldVL11_Model, self.weldVR11_Model]
        elif ('Back to Back Angles' in self.Obj.sec_profile or 'Back to Back Channels' in self.Obj.sec_profile or 'Star Angles' in self.Obj.sec_profile) and self.inter_length > 1000 and hasattr(self, 'inter_conc_welds'):
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
class StrutChannelWeldCAD(StrutAngleWeldCAD):

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

