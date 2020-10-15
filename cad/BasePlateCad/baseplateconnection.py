
"""
created on 09-03-2020

@author: Anand Swaroop

This file is for creating CAD model for cover baseplate bolted moment connection for connectivity Beam-Beam

"""

import numpy
import copy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse


class BasePlateCad(object):
    def __init__(self, BP, column, nut_bolt_array, bolthight, baseplate, shearkey_1, shearkey_2, weldAbvFlang, weldBelwFlang, weldSideWeb,
                 concrete, stiffener, grout, weld_stiffener_alongWeb_h, weld_stiffener_alongWeb_gh, weld_stiffener_alongWeb_v, stiffener_algflangeL,
                 stiffener_algflangeR, stiffener_acrsWeb, weld_stiffener_algflng_v, weld_stiffener_algflng_h, weld_stiffener_algflag_gh, weld_stiffener_acrsWeb_v, weld_stiffener_acrsWeb_h, weld_stiffener_acrsWeb_gh,
                  stiffener_insideflange, weld_stiffener_inflange, weld_stiffener_inflange_d):

        """

        :param column: column
        :param basebaseplate:  basebaseplate
        :param weldAbvFlang: Weld surface on the outer side of flange
        :param weldBelwFlang: Weld surface on the inner side of flange
        :param weldSideWeb: Weld surface on the sides of the web
        :param nut_bolt_array:  Bolt placement on the end baseplates
        :param alist: input and output values
        """
        self.BP = BP
        # self.BP.anchors_outside_flange = 6
        # self.BP.weld_type = "Groove" # "Fillet"  #
        self.extraspace = 5 #for stiffener inside flange
        # self.BP.stiffener_along_flange = 'Yes'
        # self.BP.stiffener_along_web = 'Yes'
        # self.BP.stiffener_across_web = 'Yes'
        # self.BP.stiffener_inside_flange = 'Yes'


        self.column = column
        self.nut_bolt_array = nut_bolt_array
        self.bolthight = bolthight
        self.baseplate = baseplate
        self.shearkey_1 = shearkey_1
        self.shearkey_2 = shearkey_2
        self.weldAbvFlang = weldAbvFlang
        self.weldBelwFlang = weldBelwFlang
        self.weldSideWeb = weldSideWeb
        self.concrete = concrete
        self.stiffener = stiffener
        self.grout = grout
        self.weld_stiffener_alongWeb_h = weld_stiffener_alongWeb_h
        self.weld_stiffener_alongWeb_gh = weld_stiffener_alongWeb_gh
        self.weld_stiffener_alongWeb_v = weld_stiffener_alongWeb_v
        self.stiffener_acrsWeb = stiffener_acrsWeb
        self.weld_stiffener_algflng_v = weld_stiffener_algflng_v
        self.weld_stiffener_algflng_h = weld_stiffener_algflng_h
        self.weld_stiffener_algflag_gh = weld_stiffener_algflag_gh
        self.weld_stiffener_acrsWeb_v = weld_stiffener_acrsWeb_v
        self.weld_stiffener_acrsWeb_h = weld_stiffener_acrsWeb_h
        self.weld_stiffener_acrsWeb_gh = weld_stiffener_acrsWeb_gh
        self.stiffener_insideflange = stiffener_insideflange
        self.weld_stiffener_inflange = weld_stiffener_inflange
        self.weld_stiffener_inflange_d = weld_stiffener_inflange_d

        self.stiffener_algflangeL1 = stiffener_algflangeL
        self.stiffener_algflangeR1 = stiffener_algflangeR

        self.stiffener_algflangeL2 = copy.deepcopy(stiffener_algflangeL)
        self.stiffener_algflangeR2 = copy.deepcopy(stiffener_algflangeR)

        self.stiffener_acrsWeb1 = copy.deepcopy(stiffener_acrsWeb)
        self.stiffener_acrsWeb2 = copy.deepcopy(stiffener_acrsWeb)


        # self.alist = None #alist
        # self.columnModel = None
        # self.baseplateModel = None
        # self.weldAbvFlang_11Model = None
        # self.weldAbvFlang_12Model = None
        #
        # self.weldBelwFlang_11Model = None
        # self.weldBelwFlang_12Model = None
        # self.weldBelwFlang_13Model = None
        # self.weldBelwFlang_14Model = None
        #
        # self.weldSideWeb_11Model = None
        # self.weldSideWeb_12Model = None

        # Weld above flange for left and right column
        self.weldAbvFlang_11 = weldAbvFlang  # column upper side
        self.weldAbvFlang_12 = copy.deepcopy(weldAbvFlang)  # column lower side

        self.weldBelwFlang_11 = weldBelwFlang  # column, upper, left
        self.weldBelwFlang_12 = copy.deepcopy(weldBelwFlang)  # column, upper, right
        self.weldBelwFlang_13 = copy.deepcopy(weldBelwFlang)  # column, lower, left
        self.weldBelwFlang_14 = copy.deepcopy(weldBelwFlang)  # column, lower, right

        self.weldSideWeb_11 = weldSideWeb  # column, left of Web
        self.weldSideWeb_12 = copy.deepcopy(weldSideWeb)  # column, right of Web

        self.stiffener1 = copy.deepcopy(self.stiffener)
        self.stiffener2 = copy.deepcopy(self.stiffener)
        self.stiffener3 = copy.deepcopy(self.stiffener)
        self.stiffener4 = copy.deepcopy(self.stiffener)

        self.weld_stiffener_alongWeb_h_11 = copy.deepcopy(self.weld_stiffener_alongWeb_h)
        self.weld_stiffener_alongWeb_h_21 = copy.deepcopy(self.weld_stiffener_alongWeb_h)
        self.weld_stiffener_alongWeb_h_12 = copy.deepcopy(self.weld_stiffener_alongWeb_h)
        self.weld_stiffener_alongWeb_h_22 = copy.deepcopy(self.weld_stiffener_alongWeb_h)

        self.weld_stiffener_alongWeb_h_31 = copy.deepcopy(self.weld_stiffener_alongWeb_h)
        self.weld_stiffener_alongWeb_h_41 = copy.deepcopy(self.weld_stiffener_alongWeb_h)
        self.weld_stiffener_alongWeb_h_32 = copy.deepcopy(self.weld_stiffener_alongWeb_h)
        self.weld_stiffener_alongWeb_h_42 = copy.deepcopy(self.weld_stiffener_alongWeb_h)

        self.weld_stiffener_alongWeb_gh1 = copy.deepcopy(self.weld_stiffener_alongWeb_gh)
        self.weld_stiffener_alongWeb_gh2 = copy.deepcopy(self.weld_stiffener_alongWeb_gh)
        self.weld_stiffener_alongWeb_gh3 = copy.deepcopy(self.weld_stiffener_alongWeb_gh)
        self.weld_stiffener_alongWeb_gh4 = copy.deepcopy(self.weld_stiffener_alongWeb_gh)

        self.weld_stiffener_alongWeb_v_1 = copy.deepcopy(self.weld_stiffener_alongWeb_v)
        self.weld_stiffener_alongWeb_v_2 = copy.deepcopy(self.weld_stiffener_alongWeb_v)
        self.weld_stiffener_alongWeb_v_3 = copy.deepcopy(self.weld_stiffener_alongWeb_v)
        self.weld_stiffener_alongWeb_v_4 = copy.deepcopy(self.weld_stiffener_alongWeb_v)

        self.weld_stiffener_algflng_v1 = copy.deepcopy(self.weld_stiffener_algflng_v)
        self.weld_stiffener_algflng_v2 = copy.deepcopy(self.weld_stiffener_algflng_v)
        self.weld_stiffener_algflng_v3 = copy.deepcopy(self.weld_stiffener_algflng_v)
        self.weld_stiffener_algflng_v4 = copy.deepcopy(self.weld_stiffener_algflng_v)

        self.weld_stiffener_algflng_h11 = copy.deepcopy(self.weld_stiffener_algflng_h)
        self.weld_stiffener_algflng_h12 = copy.deepcopy(self.weld_stiffener_algflng_h)
        self.weld_stiffener_algflng_h21 = copy.deepcopy(self.weld_stiffener_algflng_h)
        self.weld_stiffener_algflng_h22 = copy.deepcopy(self.weld_stiffener_algflng_h)
        self.weld_stiffener_algflng_h31 = copy.deepcopy(self.weld_stiffener_algflng_h)
        self.weld_stiffener_algflng_h32 = copy.deepcopy(self.weld_stiffener_algflng_h)
        self.weld_stiffener_algflng_h41 = copy.deepcopy(self.weld_stiffener_algflng_h)
        self.weld_stiffener_algflng_h42 = copy.deepcopy(self.weld_stiffener_algflng_h)

        self.weld_stiffener_algflag_gh1 = copy.deepcopy(self.weld_stiffener_algflag_gh)
        self.weld_stiffener_algflag_gh2 = copy.deepcopy(self.weld_stiffener_algflag_gh)
        self.weld_stiffener_algflag_gh3 = copy.deepcopy(self.weld_stiffener_algflag_gh)
        self.weld_stiffener_algflag_gh4 = copy.deepcopy(self.weld_stiffener_algflag_gh)

        self.weld_stiffener_acrsWeb_v1 = copy.deepcopy(self.weld_stiffener_acrsWeb_v)
        self.weld_stiffener_acrsWeb_v2 = copy.deepcopy(self.weld_stiffener_acrsWeb_v)

        self.weld_stiffener_acrsWeb_h1 = copy.deepcopy(self.weld_stiffener_acrsWeb_h)
        self.weld_stiffener_acrsWeb_h2 = copy.deepcopy(self.weld_stiffener_acrsWeb_h)
        self.weld_stiffener_acrsWeb_h3 = copy.deepcopy(self.weld_stiffener_acrsWeb_h)
        self.weld_stiffener_acrsWeb_h4 = copy.deepcopy(self.weld_stiffener_acrsWeb_h)

        self.weld_stiffener_acrsWeb_gh1 = copy.deepcopy(self.weld_stiffener_acrsWeb_gh)
        self.weld_stiffener_acrsWeb_gh2 = copy.deepcopy(self.weld_stiffener_acrsWeb_gh)

        self.stiffener_insideflange1 = copy.deepcopy(self.stiffener_insideflange)
        self.stiffener_insideflange2 = copy.deepcopy(self.stiffener_insideflange)
        # self.stiffener_insideflange3 = copy.deepcopy(self.stiffener_insideflange)
        # self.stiffener_insideflange4 = copy.deepcopy(self.stiffener_insideflange)

        self.weld_stiffener_inflange11 = copy.deepcopy(self.weld_stiffener_inflange)
        self.weld_stiffener_inflange12 = copy.deepcopy(self.weld_stiffener_inflange)
        self.weld_stiffener_inflange21 = copy.deepcopy(self.weld_stiffener_inflange)
        self.weld_stiffener_inflange22 = copy.deepcopy(self.weld_stiffener_inflange)

        self.weld_stiffener_inflange_d11 = copy.deepcopy(self.weld_stiffener_inflange_d)
        self.weld_stiffener_inflange_d22 = copy.deepcopy(self.weld_stiffener_inflange_d)
        # self.weld_stiffener_inflange5 = copy.deepcopy(self.weld_stiffener_inflange)
        # self.weld_stiffener_inflange6 = copy.deepcopy(self.weld_stiffener_inflange)
        # self.weld_stiffener_inflange7 = copy.deepcopy(self.weld_stiffener_inflange)
        # self.weld_stiffener_inflange8 = copy.deepcopy(self.weld_stiffener_inflange)


    def create_3DModel(self):
        """

        :return: CAD model of each of the followings.
        """

        self.createColumnGeometry()
        self.createBasePlateGeometry()
        self.createWeldGeometry()
        self.createConcreteGeometry()
        self.create_nut_bolt_array()
        self.createGroutGeometry()

    def createColumnGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        if self.BP.weld_type == 'Fillet Weld':
            columnOriginL = numpy.array([0.0, 0.0, 0.0])
            columnL_uDir = numpy.array([1.0, 0.0, 0.0])
            columnL_wDir = numpy.array([0.0, 0.0, 1.0])
            self.column.place(columnOriginL, columnL_uDir, columnL_wDir)

            self.columnModel = self.column.create_model()
        else:
            columnOriginL = numpy.array([0.0, 0.0, self.weldAbvFlang.h])
            columnL_uDir = numpy.array([1.0, 0.0, 0.0])
            columnL_wDir = numpy.array([0.0, 0.0, 1.0])
            self.column.place(columnOriginL, columnL_uDir, columnL_wDir)

            self.columnModel = self.column.create_model()

    def createBasePlateGeometry(self):
        baseplateOriginL = numpy.array([-self.baseplate.W / 2, 0.0, -self.baseplate.T / 2])
        baseplateL_uDir = numpy.array([0.0, 0.0, 1.0])
        baseplateL_wDir = numpy.array([1.0, 0.0, 0.0])
        self.baseplate.place(baseplateOriginL, baseplateL_uDir, baseplateL_wDir)

        self.baseplateModel = self.baseplate.create_model()

        if self.BP.shear_key_along_ColDepth == 'Yes':

            shearkey_1OriginL = numpy.array([-self.shearkey_1.W / 2, 0.0, -self.shearkey_1.T / 2 - self.baseplate.T])
            shearkey_1L_uDir = numpy.array([0.0, 0.0, 1.0])
            shearkey_1L_wDir = numpy.array([1.0, 0.0, 0.0])
            self.shearkey_1.place(shearkey_1OriginL, shearkey_1L_uDir, shearkey_1L_wDir)

            self.shearkey_1Model = self.shearkey_1.create_model()

        if self.BP.shear_key_along_ColWidth == 'Yes':
            shearkey_2OriginL = numpy.array([-self.shearkey_2.W / 2, 0.0, -self.shearkey_2.T / 2 - self.baseplate.T])
            shearkey_2L_uDir = numpy.array([0.0, 0.0, 1.0])
            shearkey_2L_wDir = numpy.array([1.0, 0.0, 0.0])
            self.shearkey_2.place(shearkey_2OriginL, shearkey_2L_uDir, shearkey_2L_wDir)

            self.shearkey_2Model = self.shearkey_2.create_model()

        if self.BP.stiffener_along_web == 'Yes':

            if 2 * self.BP.anchors_outside_flange == 4 or 2 * self.BP.anchors_outside_flange == 8:
                stiffener_gap = 0  # self.column.B * 0.4
                y_axis = self.column.D / 2 + self.stiffener.L / 2 + self.weld_stiffener_alongWeb_v.h
                if self.BP.weld_type == "Fillet":
                    z_axis = self.stiffener.W / 2  # + self.weld_stiffener_alongWeb_h.h
                else:
                    z_axis = self.stiffener.W / 2 + self.weld_stiffener_alongWeb_gh1.h  # + self.weld_stiffener_alongWeb_h.h
                stiffener1OriginL = numpy.array([self.stiffener.T / 2 + stiffener_gap, y_axis, z_axis])
                stiffener1L_uDir = numpy.array([0.0, -1.0, 0.0])
                stiffener1L_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.stiffener1.place(stiffener1OriginL, stiffener1L_uDir, stiffener1L_wDir)

                self.stiffener1Model = self.stiffener1.create_model()


                stiffener3OriginL = numpy.array(
                    [-self.stiffener.T / 2 + stiffener_gap, -(y_axis), z_axis])
                stiffener3L_uDir = numpy.array([0.0, 1.0, 0.0])
                stiffener3L_wDir = numpy.array([1.0, 0.0, 0.0])
                self.stiffener3.place(stiffener3OriginL, stiffener3L_uDir, stiffener3L_wDir)

                self.stiffener3Model = self.stiffener3.create_model()

            if 2 * self.BP.anchors_outside_flange == 6 or 2 * self.BP.anchors_outside_flange == 12:
                stiffener_gap =  self.column.B * 0.4
                y_axis = self.column.D / 2 + self.stiffener.L / 2 + self.weld_stiffener_alongWeb_v.h
                if self.BP.weld_type == "Fillet":
                    z_axis = self.stiffener.W / 2  # + self.weld_stiffener_alongWeb_h.h
                else:
                    z_axis = self.stiffener.W / 2 + self.weld_stiffener_alongWeb_gh1.h  # + self.weld_stiffener_alongWeb_h.h
                stiffener1OriginL = numpy.array([self.stiffener.T / 2 + stiffener_gap, y_axis, z_axis])
                stiffener1L_uDir = numpy.array([0.0, -1.0, 0.0])
                stiffener1L_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.stiffener1.place(stiffener1OriginL, stiffener1L_uDir, stiffener1L_wDir)

                self.stiffener1Model = self.stiffener1.create_model()

                stiffener2OriginL = numpy.array(
                    [self.stiffener.T / 2 - stiffener_gap, y_axis, z_axis])
                stiffener2L_uDir = numpy.array([0.0, -1.0, 0.0])
                stiffener2L_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.stiffener2.place(stiffener2OriginL, stiffener2L_uDir, stiffener2L_wDir)

                self.stiffener2Model = self.stiffener2.create_model()

                stiffener3OriginL = numpy.array(
                    [-self.stiffener.T / 2 + stiffener_gap, -(y_axis), z_axis])
                stiffener3L_uDir = numpy.array([0.0, 1.0, 0.0])
                stiffener3L_wDir = numpy.array([1.0, 0.0, 0.0])
                self.stiffener3.place(stiffener3OriginL, stiffener3L_uDir, stiffener3L_wDir)

                self.stiffener3Model = self.stiffener3.create_model()

                stiffener4OriginL = numpy.array(
                    [-self.stiffener.T / 2 - stiffener_gap, -(y_axis), z_axis])
                stiffener4L_uDir = numpy.array([0.0, 1.0, 0.0])
                stiffener4L_wDir = numpy.array([1.0, 0.0, 0.0])
                self.stiffener4.place(stiffener4OriginL, stiffener4L_uDir, stiffener4L_wDir)

                self.stiffener4Model = self.stiffener4.create_model()

        if self.BP.stiffener_along_flange == 'Yes':

            x_axis = self.column.B/2 + self.weld_stiffener_algflng_v.h
            y_axis = self.column.D / 2
            if self.BP.weld_type == "Fillet":
                z_axis = 0 # self.stiffener_algflangeL1.H / 2 + self.weld_stiffener_alongWeb_h.h
            else:
                z_axis = self.weld_stiffener_algflag_gh.h
            stiffener_algflangeL1OriginL = numpy.array([x_axis, y_axis - self.stiffener_algflangeL1.T, z_axis])
            stiffener_algflangeL1L_uDir = numpy.array([1.0, 0.0, 0.0])
            stiffener_algflangeL1L_wDir = numpy.array([0.0, 0.0, 1.0])
            self.stiffener_algflangeL1.place(stiffener_algflangeL1OriginL, stiffener_algflangeL1L_uDir, stiffener_algflangeL1L_wDir)

            self.stiffener_algflangeL1Model = self.stiffener_algflangeL1.create_model()

            stiffener_algflangeR1OriginL = numpy.array([-x_axis, y_axis, z_axis])
            stiffener_algflangeR1L_uDir = numpy.array([-1.0, 0.0, 0.0])
            stiffener_algflangeR1L_wDir = numpy.array([.0, 0.0, 1.0])
            self.stiffener_algflangeR1.place(stiffener_algflangeR1OriginL, stiffener_algflangeR1L_uDir, stiffener_algflangeR1L_wDir)

            self.stiffener_algflangeR1Model = self.stiffener_algflangeR1.create_model()

            stiffener_algflangeL2OriginL = numpy.array([-x_axis, -(y_axis) + self.stiffener_algflangeL1.T, z_axis])
            stiffener_algflangeL2L_uDir = numpy.array([-1.0, 0.0, 0.0])
            stiffener_algflangeL2L_wDir = numpy.array([0.0, 0.0, 1.0])
            self.stiffener_algflangeL2.place(stiffener_algflangeL2OriginL, stiffener_algflangeL2L_uDir, stiffener_algflangeL2L_wDir)

            self.stiffener_algflangeL2Model = self.stiffener_algflangeL2.create_model()

            stiffener_algflangeR2OriginL = numpy.array([x_axis, -(y_axis), z_axis])
            stiffener_algflangeR2L_uDir = numpy.array([1.0, 0.0, 0.0])
            stiffener_algflangeR2L_wDir = numpy.array([0.0, 0.0, 1.0])
            self.stiffener_algflangeR2.place(stiffener_algflangeR2OriginL, stiffener_algflangeR2L_uDir, stiffener_algflangeR2L_wDir)

            self.stiffener_algflangeR2Model = self.stiffener_algflangeR2.create_model()

        if self.BP.stiffener_across_web == 'Yes':

            # if self.BP.stiffener_along_web == 'Yes':
            stiffener_gap = 0 #self.column.B * 0.4
            x_axis = self.column.t/2 + self.stiffener_acrsWeb.L/2 + self.weld_stiffener_alongWeb_h.h  #todo: add weld ht here
            y_axis = self.stiffener_acrsWeb.T/2
            if self.BP.weld_type == "Fillet":
                z_axis = self.stiffener.W / 2 #+ self.weld_stiffener_alongWeb_h.h
            else:
                z_axis = self.stiffener.W / 2 + self.weld_stiffener_acrsWeb_gh.h
            stiffener_acrsWeb1OriginL = numpy.array([-x_axis, y_axis, z_axis])
            stiffener_acrsWeb1L_uDir = numpy.array([1.0, 0.0, 0.0])
            stiffener_acrsWeb1L_wDir = numpy.array([0.0, -1.0, 0.0])
            self.stiffener_acrsWeb1.place(stiffener_acrsWeb1OriginL, stiffener_acrsWeb1L_uDir, stiffener_acrsWeb1L_wDir)

            self.stiffener_acrsWeb1Model = self.stiffener_acrsWeb1.create_model()

            stiffener_acrsWeb2OriginL = numpy.array([x_axis, -(y_axis), z_axis])
            stiffener_acrsWeb2L_uDir = numpy.array([-1.0, 0.0, 0.0])
            stiffener_acrsWeb2L_wDir = numpy.array([0.0, 1.0, 0.0])
            self.stiffener_acrsWeb2.place(stiffener_acrsWeb2OriginL, stiffener_acrsWeb2L_uDir, stiffener_acrsWeb2L_wDir)

            self.stiffener_acrsWeb2Model = self.stiffener_acrsWeb2.create_model()

        if self.BP.stiffener_inside_flange == 'Yes':
            x_axis = self.stiffener_insideflange.W/2 + self.column.t/2 + self.weld_stiffener_inflange_d.h #+ self.column.R1 + self.extraspace
            y_axis = 0.0        #self.stiffener_acrsWeb.T/2 + self.stiffener_insideflange.L/2 + self.weld_stiffener_inflange.h
            z_axis = self.stiffener_acrsWeb.W + self.stiffener_insideflange.T/2

            stiffener_insideflange1OriginL = numpy.array([x_axis, y_axis, z_axis + self.stiffener_insideflange.T])
            stiffener_insideflange1L_uDir = numpy.array([0.0, 1.0, 0.0])
            stiffener_insideflange1L_wDir = numpy.array([0.0, 0.0, -1.0])
            self.stiffener_insideflange1.place(stiffener_insideflange1OriginL, stiffener_insideflange1L_uDir, stiffener_insideflange1L_wDir)

            self.stiffener_insideflange1Model = self.stiffener_insideflange1.create_model()

            stiffener_insideflange2OriginL = numpy.array([-x_axis, y_axis, z_axis])
            stiffener_insideflange2L_uDir = numpy.array([0.0, 1.0, 0.0])
            stiffener_insideflange2L_wDir = numpy.array([0.0, 0.0, 1.0])
            self.stiffener_insideflange2.place(stiffener_insideflange2OriginL, stiffener_insideflange2L_uDir, stiffener_insideflange2L_wDir)

            self.stiffener_insideflange2Model = self.stiffener_insideflange2.create_model()


    def createWeldGeometry(self):

        # # weld above flange
        if self.BP.weld_type == 'Fillet Weld':
            weldAbvFlangOrigin_11 = numpy.array([self.column.B / 2, -self.column.D / 2, 0.0])
            uDirAbv_11 = numpy.array([0, -1.0, 0])
            wDirAbv_11 = numpy.array([-1.0, 0, 0])
            self.weldAbvFlang_11.place(weldAbvFlangOrigin_11, uDirAbv_11, wDirAbv_11)

            weldAbvFlangOrigin_12 = numpy.array([-self.column.B / 2, self.column.D / 2, 0.0])
            uDirAbv_12 = numpy.array([0, 1.0, 0])
            wDirAbv_12 = numpy.array([1.0, 0, 0])
            self.weldAbvFlang_12.place(weldAbvFlangOrigin_12, uDirAbv_12, wDirAbv_12)

            # weld below flange
            weldBelwFlangOrigin_11 = numpy.array([self.column.R2 - self.column.B / 2, -(self.column.D / 2 - self.column.T),  0.0])
            uDirBelw_11 = numpy.array([0, 1.0, 0])
            wDirBelw_11 = numpy.array([1.0, 0, 0])
            self.weldBelwFlang_11.place(weldBelwFlangOrigin_11, uDirBelw_11, wDirBelw_11)

            weldBelwFlangOrigin_12 = numpy.array(
                [self.column.R1 + self.column.t / 2,  -(self.column.D / 2 - self.column.T),  0.0])
            uDirBelw_12 = numpy.array([0, 1.0, 0])
            wDirBelw_12 = numpy.array([1.0, 0, 0])
            self.weldBelwFlang_12.place(weldBelwFlangOrigin_12, uDirBelw_12, wDirBelw_12)

            weldBelwFlangOrigin_13 = numpy.array(
                [-self.column.R1 - self.column.t / 2, (self.column.D / 2  - self.column.T), 0.0])
            uDirBelw_13 = numpy.array([0, -1.0, 0])
            wDirBelw_13 = numpy.array([-1.0, 0, 0])
            self.weldBelwFlang_13.place(weldBelwFlangOrigin_13, uDirBelw_13, wDirBelw_13)

            weldBelwFlangOrigin_14 = numpy.array(
                [-self.column.R2 + self.column.B / 2, (self.column.D / 2  - self.column.T), 0.0])
            uDirBelw_14 = numpy.array([0, -1.0, 0])
            wDirBelw_14 = numpy.array([-1.0, 0, 0])
            self.weldBelwFlang_14.place(weldBelwFlangOrigin_14, uDirBelw_14, wDirBelw_14)


            # Weld side web
            weldSideWebOrigin_11 = numpy.array([-self.column.t / 2, self.weldSideWeb_11.L / 2, 0.0])
            uDirWeb_11 = numpy.array([0, 0.0, 1.0])
            wDirWeb_11 = numpy.array([0, -1.0, 0.0])
            self.weldSideWeb_11.place(weldSideWebOrigin_11, uDirWeb_11, wDirWeb_11)

            weldSideWebOrigin_12 = numpy.array([self.column.t / 2, -self.weldSideWeb_12.L / 2, 0.0])
            uDirWeb_12 = numpy.array([0, 0.0, 1.0])
            wDirWeb_12 = numpy.array([0, 1.0, 0.0])
            self.weldSideWeb_12.place(weldSideWebOrigin_12, uDirWeb_12, wDirWeb_12)

            self.weldAbvFlang_11Model = self.weldAbvFlang_11.create_model()
            self.weldAbvFlang_12Model = self.weldAbvFlang_12.create_model()

            self.weldBelwFlang_11Model = self.weldBelwFlang_11.create_model()
            self.weldBelwFlang_12Model = self.weldBelwFlang_12.create_model()
            self.weldBelwFlang_13Model = self.weldBelwFlang_13.create_model()
            self.weldBelwFlang_14Model = self.weldBelwFlang_14.create_model()

            self.weldSideWeb_11Model = self.weldSideWeb_11.create_model()
            self.weldSideWeb_12Model = self.weldSideWeb_12.create_model()

        else:
            weldAbvFlangOrigin_11 = numpy.array([self.column.B / 2, -self.column.D / 2 + self.weldAbvFlang.b/2, self.weldAbvFlang.h/2])
            uDirAbv_11 = numpy.array([0, -1.0, 0.0])
            wDirAbv_11 = numpy.array([-1.0, 0, 0])
            self.weldAbvFlang_11.place(weldAbvFlangOrigin_11, uDirAbv_11, wDirAbv_11)

            self.weldAbvFlang_11Model = self.weldAbvFlang_11.create_model()

            weldAbvFlangOrigin_12 = numpy.array([-self.column.B / 2, self.column.D / 2 - self.weldAbvFlang.b/2, self.weldAbvFlang.h/2])
            uDirAbv_12 = numpy.array([0, 1.0, 0.0])
            wDirAbv_12 = numpy.array([1.0, 0, 0])
            self.weldAbvFlang_12.place(weldAbvFlangOrigin_12, uDirAbv_12, wDirAbv_12)

            self.weldAbvFlang_12Model = self.weldAbvFlang_12.create_model()

            weldSideWebOrigin_11 = numpy.array([-self.column.t / 2 + self.weldSideWeb.b/2, self.weldSideWeb_11.L / 2, self.weldAbvFlang.h/2])
            uDirWeb_11 = numpy.array([1.0, 0.0, 0.0])
            wDirWeb_11 = numpy.array([0, -1.0, 0.0])
            self.weldSideWeb_11.place(weldSideWebOrigin_11, uDirWeb_11, wDirWeb_11)

            self.weldSideWeb_11Model = self.weldSideWeb_11.create_model()


        if self.BP.stiffener_along_web == 'Yes':
            if 2 * self.BP.anchors_outside_flange == 4 or 2 * self.BP.anchors_outside_flange == 8:
                if self.BP.weld_type == "Fillet":
                    x_axis =  self.stiffener.T/2
                    y_axis = self.column.D / 2 + self.stiffener.L + self.weld_stiffener_alongWeb_v.h
                    z_axis = 0.0
                    stiffenerweldOrigin_h_11 = numpy.array([-x_axis, y_axis, z_axis])
                    uDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
                    wDirAbv_11 = numpy.array([0.0, -1.0, 0])
                    self.weld_stiffener_alongWeb_h_11.place(stiffenerweldOrigin_h_11, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_h_11Model = self.weld_stiffener_alongWeb_h_11.create_model()

                    stiffenerweldOrigin_h_21 = numpy.array([-x_axis, -y_axis + self.weld_stiffener_alongWeb_h_21.L, z_axis])
                    uDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
                    wDirAbv_11 = numpy.array([0.0, -1.0, 0])
                    self.weld_stiffener_alongWeb_h_21.place(stiffenerweldOrigin_h_21, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_h_21Model = self.weld_stiffener_alongWeb_h_21.create_model()

                    stiffenerweldOrigin_h_12 = numpy.array([ x_axis, y_axis - self.weld_stiffener_alongWeb_h_21.L, z_axis])
                    uDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
                    wDirAbv_11 = numpy.array([0.0, 1.0, 0])
                    self.weld_stiffener_alongWeb_h_12.place(stiffenerweldOrigin_h_12, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_h_12Model = self.weld_stiffener_alongWeb_h_12.create_model()

                    stiffenerweldOrigin_h_22 = numpy.array([ x_axis, -y_axis, z_axis])
                    uDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
                    wDirAbv_11 = numpy.array([0.0, 1.0, 0])
                    self.weld_stiffener_alongWeb_h_22.place(stiffenerweldOrigin_h_22, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_h_22Model = self.weld_stiffener_alongWeb_h_22.create_model()

                else:
                    stiffener_gap = 0.0
                    x_axis = 0.0
                    y_axis = self.column.D / 2 + self.stiffener.L + self.weld_stiffener_alongWeb_v.h
                    z_axis = self.weld_stiffener_alongWeb_gh.h/2

                    stiffenerweldOrigin_h_11 = numpy.array([-x_axis + stiffener_gap, y_axis, z_axis])
                    uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
                    wDirAbv_11 = numpy.array([0.0, -1.0, 0])
                    self.weld_stiffener_alongWeb_gh1.place(stiffenerweldOrigin_h_11, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_gh1Model = self.weld_stiffener_alongWeb_gh1.create_model()

                    stiffenerweldOrigin_h_21 = numpy.array(
                        [-x_axis + stiffener_gap, -y_axis + self.weld_stiffener_alongWeb_gh2.L, z_axis])
                    uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
                    wDirAbv_11 = numpy.array([0.0, -1.0, 0])
                    self.weld_stiffener_alongWeb_gh2.place(stiffenerweldOrigin_h_21, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_gh2Model = self.weld_stiffener_alongWeb_gh2.create_model()


                x_axis = self.stiffener.T / 2
                y_axis = self.column.D / 2 + self.stiffener.L + self.weld_stiffener_alongWeb_v.h
                if self.BP.weld_type == "Fillet":
                    z_axis = self.stiffener.R22
                else:
                    z_axis =  self.stiffener.R22 + self.weld_stiffener_alongWeb_gh.h
                stiffenerweldOrigin_v_1 = numpy.array([ 0.0, y_axis - self.stiffener.L - self.weld_stiffener_alongWeb_v.h/2, z_axis])
                uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
                wDirAbv_11 = numpy.array([0.0, 0, 1.0])
                self.weld_stiffener_alongWeb_v_1.place(stiffenerweldOrigin_v_1, uDirAbv_11, wDirAbv_11)

                self.weld_stiffener_alongWeb_v_1Model = self.weld_stiffener_alongWeb_v_1.create_model()

                stiffenerweldOrigin_v_2 = numpy.array([ 0.0, -y_axis + self.stiffener.L + self.weld_stiffener_alongWeb_v.h/2, z_axis])
                uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
                wDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
                self.weld_stiffener_alongWeb_v_2.place(stiffenerweldOrigin_v_2, uDirAbv_11, wDirAbv_11)

                self.weld_stiffener_alongWeb_v_2Model = self.weld_stiffener_alongWeb_v_2.create_model()

            if 2 * self.BP.anchors_outside_flange == 6 or 2 * self.BP.anchors_outside_flange == 12:
                if self.BP.weld_type == "Fillet":
                    stiffener_gap = self.column.B * 0.4
                    x_axis = self.stiffener.T / 2
                    y_axis = self.column.D / 2 + self.stiffener.L + self.weld_stiffener_alongWeb_v.h
                    z_axis = 0.0

                    stiffenerweldOrigin_h_11 = numpy.array([-x_axis + stiffener_gap, y_axis, z_axis])
                    uDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
                    wDirAbv_11 = numpy.array([0.0, -1.0, 0])
                    self.weld_stiffener_alongWeb_h_11.place(stiffenerweldOrigin_h_11, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_h_11Model = self.weld_stiffener_alongWeb_h_11.create_model()

                    stiffenerweldOrigin_h_21 = numpy.array([-x_axis + stiffener_gap, -y_axis + self.weld_stiffener_alongWeb_h_21.L, z_axis])
                    uDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
                    wDirAbv_11 = numpy.array([0.0, -1.0, 0])
                    self.weld_stiffener_alongWeb_h_21.place(stiffenerweldOrigin_h_21, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_h_21Model = self.weld_stiffener_alongWeb_h_21.create_model()

                    stiffenerweldOrigin_h_12 = numpy.array([x_axis + stiffener_gap, y_axis - self.weld_stiffener_alongWeb_h_21.L, z_axis])
                    uDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
                    wDirAbv_11 = numpy.array([0.0, 1.0, 0])
                    self.weld_stiffener_alongWeb_h_12.place(stiffenerweldOrigin_h_12, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_h_12Model = self.weld_stiffener_alongWeb_h_12.create_model()

                    stiffenerweldOrigin_h_22 = numpy.array([x_axis + stiffener_gap, -y_axis, z_axis])
                    uDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
                    wDirAbv_11 = numpy.array([0.0, 1.0, 0])
                    self.weld_stiffener_alongWeb_h_22.place(stiffenerweldOrigin_h_22, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_h_22Model = self.weld_stiffener_alongWeb_h_22.create_model()

                    stiffenerweldOrigin_h_31 = numpy.array([-x_axis - stiffener_gap, y_axis, z_axis])
                    uDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
                    wDirAbv_11 = numpy.array([0.0, -1.0, 0])
                    self.weld_stiffener_alongWeb_h_31.place(stiffenerweldOrigin_h_31, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_h_31Model = self.weld_stiffener_alongWeb_h_31.create_model()

                    stiffenerweldOrigin_h_41 = numpy.array([-x_axis - stiffener_gap, -y_axis + self.weld_stiffener_alongWeb_h_41.L, z_axis])
                    uDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
                    wDirAbv_11 = numpy.array([0.0, -1.0, 0])
                    self.weld_stiffener_alongWeb_h_41.place(stiffenerweldOrigin_h_41, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_h_41Model = self.weld_stiffener_alongWeb_h_41.create_model()

                    stiffenerweldOrigin_h_32 = numpy.array([x_axis - stiffener_gap, y_axis - self.weld_stiffener_alongWeb_h_21.L, z_axis])
                    uDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
                    wDirAbv_11 = numpy.array([0.0, 1.0, 0])
                    self.weld_stiffener_alongWeb_h_32.place(stiffenerweldOrigin_h_32, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_h_32Model = self.weld_stiffener_alongWeb_h_32.create_model()

                    stiffenerweldOrigin_h_42 = numpy.array([x_axis - stiffener_gap, -y_axis, z_axis])
                    uDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
                    wDirAbv_11 = numpy.array([0.0, 1.0, 0])
                    self.weld_stiffener_alongWeb_h_42.place(stiffenerweldOrigin_h_42, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_h_42Model = self.weld_stiffener_alongWeb_h_42.create_model()

                else:
                    stiffener_gap = self.column.B * 0.4
                    x_axis = 0.0
                    y_axis = self.column.D / 2 + self.stiffener.L + self.weld_stiffener_alongWeb_v.h
                    z_axis = self.weld_stiffener_alongWeb_gh.h/2

                    stiffenerweldOrigin_h_11 = numpy.array([-x_axis + stiffener_gap, y_axis, z_axis])
                    uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
                    wDirAbv_11 = numpy.array([0.0, -1.0, 0])
                    self.weld_stiffener_alongWeb_gh1.place(stiffenerweldOrigin_h_11, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_gh1Model = self.weld_stiffener_alongWeb_gh1.create_model()

                    stiffenerweldOrigin_h_21 = numpy.array(
                        [-x_axis + stiffener_gap, -y_axis + self.weld_stiffener_alongWeb_gh2.L, z_axis])
                    uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
                    wDirAbv_11 = numpy.array([0.0, -1.0, 0])
                    self.weld_stiffener_alongWeb_gh2.place(stiffenerweldOrigin_h_21, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_gh2Model = self.weld_stiffener_alongWeb_gh2.create_model()

                    stiffenerweldOrigin_h_31 = numpy.array([-x_axis - stiffener_gap, y_axis, z_axis])
                    uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
                    wDirAbv_11 = numpy.array([0.0, -1.0, 0])
                    self.weld_stiffener_alongWeb_gh3.place(stiffenerweldOrigin_h_31, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_gh3Model = self.weld_stiffener_alongWeb_gh3.create_model()

                    stiffenerweldOrigin_h_41 = numpy.array(
                        [-x_axis - stiffener_gap, -y_axis + self.weld_stiffener_alongWeb_gh4.L, z_axis])
                    uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
                    wDirAbv_11 = numpy.array([0.0, -1.0, 0])
                    self.weld_stiffener_alongWeb_gh4.place(stiffenerweldOrigin_h_41, uDirAbv_11, wDirAbv_11)

                    self.weld_stiffener_alongWeb_gh4Model = self.weld_stiffener_alongWeb_gh4.create_model()

                stiffener_gap = self.column.B * 0.4
                x_axis = self.stiffener.T / 2
                y_axis = self.column.D / 2 + self.stiffener.L + self.weld_stiffener_alongWeb_v.h
                if self.BP.weld_type == "Fillet":
                    z_axis = self.stiffener.R22
                else:
                    z_axis =  self.stiffener.R22 + self.weld_stiffener_alongWeb_gh.h
                stiffenerweldOrigin_v_1 = numpy.array(
                    [stiffener_gap, y_axis - self.stiffener.L - self.weld_stiffener_alongWeb_v.h / 2, z_axis])
                uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
                wDirAbv_11 = numpy.array([0.0, 0, 1.0])
                self.weld_stiffener_alongWeb_v_1.place(stiffenerweldOrigin_v_1, uDirAbv_11, wDirAbv_11)

                self.weld_stiffener_alongWeb_v_1Model = self.weld_stiffener_alongWeb_v_1.create_model()

                stiffenerweldOrigin_v_2 = numpy.array(
                    [stiffener_gap, -y_axis + self.stiffener.L + self.weld_stiffener_alongWeb_v.h / 2, z_axis])
                uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
                wDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
                self.weld_stiffener_alongWeb_v_2.place(stiffenerweldOrigin_v_2, uDirAbv_11, wDirAbv_11)

                self.weld_stiffener_alongWeb_v_2Model = self.weld_stiffener_alongWeb_v_2.create_model()

                stiffenerweldOrigin_v_3 = numpy.array(
                    [-stiffener_gap, y_axis - self.stiffener.L - self.weld_stiffener_alongWeb_v.h / 2, z_axis])
                uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
                wDirAbv_11 = numpy.array([0.0, 0, 1.0])
                self.weld_stiffener_alongWeb_v_3.place(stiffenerweldOrigin_v_3, uDirAbv_11, wDirAbv_11)

                self.weld_stiffener_alongWeb_v_3Model = self.weld_stiffener_alongWeb_v_3.create_model()

                stiffenerweldOrigin_v_4 = numpy.array(
                    [-stiffener_gap, -y_axis + self.stiffener.L + self.weld_stiffener_alongWeb_v.h / 2, z_axis])
                uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
                wDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
                self.weld_stiffener_alongWeb_v_4.place(stiffenerweldOrigin_v_4, uDirAbv_11, wDirAbv_11)

                self.weld_stiffener_alongWeb_v_4Model = self.weld_stiffener_alongWeb_v_4.create_model()


        if self.BP.stiffener_along_flange == 'Yes':
            x_axis = self.column.B / 2 + self.weld_stiffener_algflng_v.h/2  # todo: add web length here
            z_axis = 0  # self.stiffener_algflangeL1.H / 2 + self.weld_stiffener_alongWeb_h.h
            y_axis = self.column.D / 2 - self.weld_stiffener_algflng_v.b/2
            if self.BP.weld_type == "Fillet":
                z_axis = 0  # self.stiffener_algflangeL1.H / 2 + self.weld_stiffener_alongWeb_h.h
            else:
                z_axis = self.weld_stiffener_acrsWeb_gh.h
            weld_stiffener_algflng_v1OriginL = numpy.array([x_axis, y_axis, z_axis])
            weld_stiffener_algflng_v1L_uDir = numpy.array([0.0, 1.0, 0.0])
            weld_stiffener_algflng_v1L_wDir = numpy.array([0.0, 0.0, 1.0])
            self.weld_stiffener_algflng_v1.place(weld_stiffener_algflng_v1OriginL, weld_stiffener_algflng_v1L_uDir,
                                             weld_stiffener_algflng_v1L_wDir)

            self.weld_stiffener_algflng_v1Model = self.weld_stiffener_algflng_v1.create_model()

            weld_stiffener_algflng_v3OriginL = numpy.array([-x_axis, y_axis, z_axis])
            weld_stiffener_algflng_v3L_uDir = numpy.array([0.0, 1.0, 0.0])
            weld_stiffener_algflng_v3L_wDir = numpy.array([.0, 0.0, 1.0])
            self.weld_stiffener_algflng_v3.place(weld_stiffener_algflng_v3OriginL, weld_stiffener_algflng_v3L_uDir,
                                             weld_stiffener_algflng_v3L_wDir)

            self.weld_stiffener_algflng_v3Model = self.weld_stiffener_algflng_v3.create_model()

            weld_stiffener_algflng_v2OriginL = numpy.array([-x_axis, -(y_axis), z_axis])
            weld_stiffener_algflng_v2L_uDir = numpy.array([0.0, 1.0, 0.0])
            weld_stiffener_algflng_v2L_wDir = numpy.array([0.0, 0.0, 1.0])
            self.weld_stiffener_algflng_v2.place(weld_stiffener_algflng_v2OriginL, weld_stiffener_algflng_v2L_uDir,
                                             weld_stiffener_algflng_v2L_wDir)

            self.weld_stiffener_algflng_v2Model = self.weld_stiffener_algflng_v2.create_model()

            weld_stiffener_algflng_v4OriginL = numpy.array([x_axis, -(y_axis), z_axis])
            weld_stiffener_algflng_v4L_uDir = numpy.array([0.0, 1.0, 0.0])
            weld_stiffener_algflng_v4L_wDir = numpy.array([0.0, 0.0, 1.0])
            self.weld_stiffener_algflng_v4.place(weld_stiffener_algflng_v4OriginL, weld_stiffener_algflng_v4L_uDir,
                                             weld_stiffener_algflng_v4L_wDir)

            self.weld_stiffener_algflng_v4Model = self.weld_stiffener_algflng_v4.create_model()


            if self.BP.weld_type == "Fillet":
                #Fillet weld for stiffeners across flange
                x_axis = self.column.B / 2 + self.weld_stiffener_algflng_v.h  # todo: add web length here
                z_axis = 0  # self.stiffener_algflangeL1.H / 2 + self.weld_stiffener_alongWeb_h.h
                y_axis = self.column.D / 2 #- self.weld_stiffener_algflng_v.b/2
                weld_stiffener_algflng_h11OriginL = numpy.array([x_axis, y_axis, z_axis])
                weld_stiffener_algflng_h11L_uDir = numpy.array([0.0, 1.0, 0.0])
                weld_stiffener_algflng_h11L_wDir = numpy.array([1.0, 0.0, 0.0])
                self.weld_stiffener_algflng_h11.place(weld_stiffener_algflng_h11OriginL, weld_stiffener_algflng_h11L_uDir,
                                                 weld_stiffener_algflng_h11L_wDir)

                self.weld_stiffener_algflng_h11Model = self.weld_stiffener_algflng_h11.create_model()

                weld_stiffener_algflng_h12OriginL = numpy.array([x_axis + self.weld_stiffener_algflng_h.L, y_axis - self.stiffener_algflangeL1.T, z_axis])
                weld_stiffener_algflng_h12L_uDir = numpy.array([0.0, -1.0, 0.0])
                weld_stiffener_algflng_h12L_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.weld_stiffener_algflng_h12.place(weld_stiffener_algflng_h12OriginL, weld_stiffener_algflng_h12L_uDir,
                                                 weld_stiffener_algflng_h12L_wDir)

                self.weld_stiffener_algflng_h12Model = self.weld_stiffener_algflng_h12.create_model()

                weld_stiffener_algflng_h21OriginL = numpy.array([-x_axis - self.weld_stiffener_algflng_h.L, y_axis, z_axis])
                weld_stiffener_algflng_h21L_uDir = numpy.array([0.0, 1.0, 0.0])
                weld_stiffener_algflng_h21L_wDir = numpy.array([1.0, 0.0, 0.0])
                self.weld_stiffener_algflng_h21.place(weld_stiffener_algflng_h21OriginL, weld_stiffener_algflng_h21L_uDir,
                                                 weld_stiffener_algflng_h21L_wDir)

                self.weld_stiffener_algflng_h21Model = self.weld_stiffener_algflng_h21.create_model()

                weld_stiffener_algflng_h22OriginL = numpy.array([-x_axis, y_axis - self.stiffener_algflangeL1.T, z_axis])
                weld_stiffener_algflng_h22L_uDir = numpy.array([0.0, -1.0, 0.0])
                weld_stiffener_algflng_h22L_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.weld_stiffener_algflng_h22.place(weld_stiffener_algflng_h22OriginL, weld_stiffener_algflng_h22L_uDir,
                                                 weld_stiffener_algflng_h22L_wDir)

                self.weld_stiffener_algflng_h22Model = self.weld_stiffener_algflng_h22.create_model()

                weld_stiffener_algflng_h31OriginL = numpy.array([-x_axis, -(y_axis), z_axis])
                weld_stiffener_algflng_h31L_uDir = numpy.array([0.0, -1.0, 0.0])
                weld_stiffener_algflng_h31L_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.weld_stiffener_algflng_h31.place(weld_stiffener_algflng_h31OriginL, weld_stiffener_algflng_h31L_uDir,
                                                 weld_stiffener_algflng_h31L_wDir)

                self.weld_stiffener_algflng_h31Model = self.weld_stiffener_algflng_h31.create_model()

                weld_stiffener_algflng_h32OriginL = numpy.array([-x_axis - self.weld_stiffener_algflng_h.L , -y_axis + self.stiffener_algflangeL1.T , z_axis])
                weld_stiffener_algflng_h32L_uDir = numpy.array([0.0, 1.0, 0.0])
                weld_stiffener_algflng_h32L_wDir = numpy.array([1.0, 0.0, 0.0])
                self.weld_stiffener_algflng_h32.place(weld_stiffener_algflng_h32OriginL, weld_stiffener_algflng_h32L_uDir,
                                                 weld_stiffener_algflng_h32L_wDir)

                self.weld_stiffener_algflng_h32Model = self.weld_stiffener_algflng_h32.create_model()

                weld_stiffener_algflng_h41OriginL = numpy.array([x_axis + self.weld_stiffener_algflng_h.L, -(y_axis), z_axis])
                weld_stiffener_algflng_h41L_uDir = numpy.array([0.0, -1.0, 0.0])
                weld_stiffener_algflng_h41L_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.weld_stiffener_algflng_h41.place(weld_stiffener_algflng_h41OriginL, weld_stiffener_algflng_h41L_uDir,
                                                 weld_stiffener_algflng_h41L_wDir)

                self.weld_stiffener_algflng_h41Model = self.weld_stiffener_algflng_h41.create_model()

                weld_stiffener_algflng_h42OriginL = numpy.array([x_axis, -y_axis + self.stiffener_algflangeL1.T, z_axis])
                weld_stiffener_algflng_h42L_uDir = numpy.array([0.0, 1.0, 0.0])
                weld_stiffener_algflng_h42L_wDir = numpy.array([1.0, 0.0, 0.0])
                self.weld_stiffener_algflng_h42.place(weld_stiffener_algflng_h42OriginL, weld_stiffener_algflng_h42L_uDir,
                                                 weld_stiffener_algflng_h42L_wDir)

                self.weld_stiffener_algflng_h42Model = self.weld_stiffener_algflng_h42.create_model()

            else: #"Groove"
                x_axis = self.column.B / 2 + self.weld_stiffener_algflng_v.h + self.stiffener_algflangeL1.L  # todo: add web length here
                z_axis = self.weld_stiffener_algflag_gh.h/2  # self.stiffener_algflangeL1.H / 2 + self.weld_stiffener_alongWeb_h.h
                y_axis = self.column.D / 2 - self.weld_stiffener_algflag_gh.b/2
                weld_stiffener_algflag_gh1OriginL = numpy.array([x_axis, y_axis, z_axis])
                weld_stiffener_algflag_gh1L_uDir = numpy.array([0.0, -1.0, 0.0])
                weld_stiffener_algflag_gh1L_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.weld_stiffener_algflag_gh1.place(weld_stiffener_algflag_gh1OriginL, weld_stiffener_algflag_gh1L_uDir,
                                                 weld_stiffener_algflag_gh1L_wDir)

                self.weld_stiffener_algflag_gh1Model = self.weld_stiffener_algflag_gh1.create_model()

                weld_stiffener_algflag_gh2OriginL = numpy.array([-x_axis , y_axis, z_axis])
                weld_stiffener_algflag_gh2L_uDir = numpy.array([0.0, 1.0, 0.0])
                weld_stiffener_algflag_gh2L_wDir = numpy.array([1.0, 0.0, 0.0])
                self.weld_stiffener_algflag_gh2.place(weld_stiffener_algflag_gh2OriginL, weld_stiffener_algflag_gh2L_uDir,
                                                      weld_stiffener_algflag_gh2L_wDir)

                self.weld_stiffener_algflag_gh2Model = self.weld_stiffener_algflag_gh2.create_model()

                weld_stiffener_algflag_gh3OriginL = numpy.array([-x_axis, -(y_axis), z_axis])
                weld_stiffener_algflag_gh3L_uDir = numpy.array([0.0, 1.0, 0.0])
                weld_stiffener_algflag_gh3L_wDir = numpy.array([1.0, 0.0, 0.0])
                self.weld_stiffener_algflag_gh3.place(weld_stiffener_algflag_gh3OriginL, weld_stiffener_algflag_gh3L_uDir,
                                                      weld_stiffener_algflag_gh3L_wDir)

                self.weld_stiffener_algflag_gh3Model = self.weld_stiffener_algflag_gh3.create_model()

                weld_stiffener_algflag_gh4OriginL = numpy.array([x_axis, -(y_axis), z_axis])
                weld_stiffener_algflag_gh4L_uDir = numpy.array([0.0, -1.0, 0.0])
                weld_stiffener_algflag_gh4L_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.weld_stiffener_algflag_gh4.place(weld_stiffener_algflag_gh4OriginL, weld_stiffener_algflag_gh4L_uDir,
                                                      weld_stiffener_algflag_gh4L_wDir)

                self.weld_stiffener_algflag_gh4Model = self.weld_stiffener_algflag_gh4.create_model()

        if self.BP.stiffener_across_web == 'Yes':
            stiffener_gap = 0 #self.column.B * 0.4
            x_axis = self.column.t/2 + self.weld_stiffener_acrsWeb_v.h/2  #todo: add weld ht here
            y_axis = 0.0
            if self.BP.weld_type == "Fillet":
                z_axis = self.stiffener_acrsWeb.R22    #self.stiffener.W / 2 #+ self.weld_stiffener_alongWeb_h.h
            else:
                z_axis = self.stiffener_acrsWeb.R22 + self.weld_stiffener_acrsWeb_gh.h

            weld_stiffener_acrsWeb_v1OriginL = numpy.array([-x_axis, -y_axis, z_axis])
            weld_stiffener_acrsWeb_v1L_uDir = numpy.array([0.0, 1.0, 0.0])
            weld_stiffener_acrsWeb_v1L_wDir = numpy.array([0.0, 0.0, 1.0])
            self.weld_stiffener_acrsWeb_v1.place(weld_stiffener_acrsWeb_v1OriginL, weld_stiffener_acrsWeb_v1L_uDir, weld_stiffener_acrsWeb_v1L_wDir)

            self.weld_stiffener_acrsWeb_v1Model = self.weld_stiffener_acrsWeb_v1.create_model()

            weld_stiffener_acrsWeb_v2OriginL = numpy.array([x_axis, -(y_axis), z_axis])
            weld_stiffener_acrsWeb_v2L_uDir = numpy.array([0.0, 1.0, 0.0])
            weld_stiffener_acrsWeb_v2L_wDir = numpy.array([0.0, 0.0, 1.0])
            self.weld_stiffener_acrsWeb_v2.place(weld_stiffener_acrsWeb_v2OriginL, weld_stiffener_acrsWeb_v2L_uDir, weld_stiffener_acrsWeb_v2L_wDir)

            self.weld_stiffener_acrsWeb_v2Model = self.weld_stiffener_acrsWeb_v2.create_model()


            #horizonrtal fillet welds for stiffner across web
            if self.BP.weld_type == "Fillet":
                x_axis = self.column.t/2 + self.weld_stiffener_acrsWeb_v.h + self.stiffener_acrsWeb.R22
                z_axis = 0.0
                y_axis = self.stiffener_acrsWeb.T/2
                weld_stiffener_acrsWeb_h1OriginL = numpy.array([-x_axis - self.weld_stiffener_acrsWeb_h.L, y_axis, z_axis])
                weld_stiffener_acrsWeb_h1L_uDir = numpy.array([0.0, 1.0, 0.0])
                weld_stiffener_acrsWeb_h1L_wDir = numpy.array([1.0, 0.0, 0.0])
                self.weld_stiffener_acrsWeb_h1.place(weld_stiffener_acrsWeb_h1OriginL, weld_stiffener_acrsWeb_h1L_uDir, weld_stiffener_acrsWeb_h1L_wDir)

                self.weld_stiffener_acrsWeb_h1Model = self.weld_stiffener_acrsWeb_h1.create_model()

                weld_stiffener_acrsWeb_h2OriginL = numpy.array([x_axis, (y_axis), z_axis])
                weld_stiffener_acrsWeb_h2L_uDir = numpy.array([0.0, 1.0, 0.0])
                weld_stiffener_acrsWeb_h2L_wDir = numpy.array([1.0, 0.0, 0.0])
                self.weld_stiffener_acrsWeb_h2.place(weld_stiffener_acrsWeb_h2OriginL, weld_stiffener_acrsWeb_h2L_uDir, weld_stiffener_acrsWeb_h2L_wDir)

                self.weld_stiffener_acrsWeb_h2Model = self.weld_stiffener_acrsWeb_h2.create_model()

                weld_stiffener_acrsWeb_h3OriginL = numpy.array([-x_axis, -y_axis, z_axis])
                weld_stiffener_acrsWeb_h3L_uDir = numpy.array([0.0, -1.0, 0.0])
                weld_stiffener_acrsWeb_h3L_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.weld_stiffener_acrsWeb_h3.place(weld_stiffener_acrsWeb_h3OriginL, weld_stiffener_acrsWeb_h3L_uDir, weld_stiffener_acrsWeb_h3L_wDir)

                self.weld_stiffener_acrsWeb_h3Model = self.weld_stiffener_acrsWeb_h3.create_model()

                weld_stiffener_acrsWeb_h4OriginL = numpy.array([x_axis + self.weld_stiffener_acrsWeb_h.L, -(y_axis), z_axis])
                weld_stiffener_acrsWeb_h4L_uDir = numpy.array([0.0, -1.0, 0.0])
                weld_stiffener_acrsWeb_h4L_wDir = numpy.array([-1.0, 0.0, 0.0])
                self.weld_stiffener_acrsWeb_h4.place(weld_stiffener_acrsWeb_h4OriginL, weld_stiffener_acrsWeb_h4L_uDir, weld_stiffener_acrsWeb_h4L_wDir)

                self.weld_stiffener_acrsWeb_h4Model = self.weld_stiffener_acrsWeb_h4.create_model()

            else: # "Groove"
                x_axis = self.column.t / 2 + self.weld_stiffener_acrsWeb_v.h + self.stiffener_acrsWeb.R22
                z_axis = self.weld_stiffener_acrsWeb_gh.h/2
                y_axis = 0.0
                weld_stiffener_acrsWeb_gh1OriginL = numpy.array([-x_axis - self.weld_stiffener_acrsWeb_h.L, y_axis, z_axis])
                weld_stiffener_acrsWeb_gh1L_uDir = numpy.array([0.0, 1.0, 0.0])
                weld_stiffener_acrsWeb_gh1L_wDir = numpy.array([1.0, 0.0, 0.0])
                self.weld_stiffener_acrsWeb_gh1.place(weld_stiffener_acrsWeb_gh1OriginL, weld_stiffener_acrsWeb_gh1L_uDir,
                                                     weld_stiffener_acrsWeb_gh1L_wDir)

                self.weld_stiffener_acrsWeb_gh1Model = self.weld_stiffener_acrsWeb_gh1.create_model()

                weld_stiffener_acrsWeb_gh2OriginL = numpy.array([x_axis, (y_axis), z_axis])
                weld_stiffener_acrsWeb_gh2L_uDir = numpy.array([0.0, 1.0, 0.0])
                weld_stiffener_acrsWeb_gh2L_wDir = numpy.array([1.0, 0.0, 0.0])
                self.weld_stiffener_acrsWeb_gh2.place(weld_stiffener_acrsWeb_gh2OriginL, weld_stiffener_acrsWeb_gh2L_uDir,
                                                     weld_stiffener_acrsWeb_gh2L_wDir)

                self.weld_stiffener_acrsWeb_gh2Model = self.weld_stiffener_acrsWeb_gh2.create_model()


        if self.BP.stiffener_inside_flange == 'Yes':
            x_axis =  self.column.t/2 + self.stiffener_insideflange.R22 + self.weld_stiffener_inflange_d.h #self.column.R1 + self.extraspace
            y_axis = self.stiffener_insideflange.L/2 + self.weld_stiffener_inflange.h/2        #self.stiffener_acrsWeb.T/2 + self.stiffener_insideflange.L/2 + self.weld_stiffener_inflange.h
            z_axis = self.stiffener_acrsWeb.W + self.weld_stiffener_inflange.b

            weld_stiffener_inflange11OriginL = numpy.array([x_axis, y_axis, z_axis])
            weld_stiffener_inflange11L_uDir = numpy.array([0.0, 0.0, 1.0])
            weld_stiffener_inflange11L_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weld_stiffener_inflange11.place(weld_stiffener_inflange11OriginL, weld_stiffener_inflange11L_uDir, weld_stiffener_inflange11L_wDir)

            self.weld_stiffener_inflange11Model = self.weld_stiffener_inflange11.create_model()

            weld_stiffener_inflange21OriginL = numpy.array([-x_axis, y_axis, z_axis])
            weld_stiffener_inflange21L_uDir = numpy.array([0.0, 0.0, 1.0])
            weld_stiffener_inflange21L_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weld_stiffener_inflange21.place(weld_stiffener_inflange21OriginL, weld_stiffener_inflange21L_uDir, weld_stiffener_inflange21L_wDir)

            self.weld_stiffener_inflange21Model = self.weld_stiffener_inflange21.create_model()

            weld_stiffener_inflange12OriginL = numpy.array([x_axis, -y_axis, z_axis])
            weld_stiffener_inflange12L_uDir = numpy.array([0.0, 0.0, 1.0])
            weld_stiffener_inflange12L_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weld_stiffener_inflange12.place(weld_stiffener_inflange12OriginL, weld_stiffener_inflange12L_uDir, weld_stiffener_inflange12L_wDir)

            self.weld_stiffener_inflange12Model = self.weld_stiffener_inflange12.create_model()

            weld_stiffener_inflange22OriginL = numpy.array([-x_axis, -y_axis, z_axis])
            weld_stiffener_inflange22L_uDir = numpy.array([0.0, 0.0, 1.0])
            weld_stiffener_inflange22L_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.weld_stiffener_inflange22.place(weld_stiffener_inflange22OriginL, weld_stiffener_inflange22L_uDir, weld_stiffener_inflange22L_wDir)

            self.weld_stiffener_inflange22Model = self.weld_stiffener_inflange22.create_model()


            x_axis = self.column.t/2 + self.weld_stiffener_inflange_d.h/2
            y_axis = -self.weld_stiffener_inflange_d.L/2        #self.stiffener_acrsWeb.T/2 + self.stiffener_insideflange.L/2 + self.weld_stiffener_inflange.h
            z_axis = self.stiffener_acrsWeb.W + self.weld_stiffener_inflange.b

            weld_stiffener_inflange_d11OriginL = numpy.array([x_axis, y_axis, z_axis])
            weld_stiffener_inflange_d11L_uDir = numpy.array([0.0, 0.0, 1.0])
            weld_stiffener_inflange_d11L_wDir = numpy.array([0.0, 1.0, 0.0])
            self.weld_stiffener_inflange_d11.place(weld_stiffener_inflange_d11OriginL, weld_stiffener_inflange_d11L_uDir, weld_stiffener_inflange_d11L_wDir)

            self.weld_stiffener_inflange_d11Model = self.weld_stiffener_inflange_d11.create_model()

            weld_stiffener_inflange_d22OriginL = numpy.array([-x_axis, y_axis, z_axis])
            weld_stiffener_inflange_d22L_uDir = numpy.array([0.0, 0.0, 1.0])
            weld_stiffener_inflange_d22L_wDir = numpy.array([0.0, 1.0, 0.0])
            self.weld_stiffener_inflange_d22.place(weld_stiffener_inflange_d22OriginL, weld_stiffener_inflange_d22L_uDir, weld_stiffener_inflange_d22L_wDir)

            self.weld_stiffener_inflange_d22Model = self.weld_stiffener_inflange_d22.create_model()

    def create_nut_bolt_array(self):
        """

        :return: Geometric Orientation of this component
        """
        # nutboltArrayOrigin = self.baseplate.sec_origin + numpy.array([0.0, 0.0, self.baseplate.T /2+ 100])
        nutboltArrayOrigin = numpy.array([-self.baseplate.W / 2, self.baseplate.L / 2, self.bolthight])
        gaugeDir = numpy.array([1.0, 0, 0])
        pitchDir = numpy.array([0, -1.0, 0])
        boltDir = numpy.array([0, 0, 1.0])
        self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        self.nutBoltArrayModels = self.nut_bolt_array.create_model()

    def createGroutGeometry(self):
        """
        :return: Geometric Orientaion of grout
        """
        groutOriginL = numpy.array([-self.grout.W / 2, 0.0, -self.baseplate.T - self.grout.T / 2])
        groutL_uDir = numpy.array([0.0, 0.0, 1.0])
        groutL_wDir = numpy.array([1.0, 0.0, 0.0])
        self.grout.place(groutOriginL, groutL_uDir, groutL_wDir)

        self.groutModel = self.grout.create_model()

    def createConcreteGeometry(self):
        """

        :return: Geometric Orientation of concrete
        """
        concreteOrigin = numpy.array(
            [-self.concrete.W / 2, 0.0, -self.baseplate.T - self.grout.T - self.concrete.T / 2])
        # concrete_uDir = numpy.array([1.0, 0.0, 0.0])
        # concrete_wDir = numpy.array([0.0, 0.0, 1.0])
        concrete_uDir = numpy.array([0.0, 0.0, 1.0])
        concrete_wDir = numpy.array([1.0, 0.0, 0.0])
        self.concrete.place(concreteOrigin, concrete_uDir, concrete_wDir)

        self.concreteModel = self.concrete.create_model()

    def get_column_model(self):
        column = self.columnModel
        return column

    def get_nut_bolt_array_models(self):
        nut_bolts = self.nut_bolt_array.get_models()
        array = nut_bolts[0]
        for comp in nut_bolts:
            array = BRepAlgoAPI_Fuse(comp, array).Shape()

        return array

    def get_welded_models(self):
        """

        :return: CAD model for all the fillet welds
        """

        # welded_sec = [self.weldAbvFlang_11Model, self.weldAbvFlang_12Model, self.weldBelwFlang_11Model, self.weldBelwFlang_12Model,
        #               self.weldBelwFlang_13Model, self.weldBelwFlang_14Model, self.weldSideWeb_11Model, self.weldSideWeb_12Model]

        # welded_sec = [self.weldAbvFlang_11Model, self.weldAbvFlang_12Model, self.weldSideWeb_11Model, self.gussetweld_1Model, self.gussetweld_2Model, self.weld_stiffener_alongWeb_h_1Model, self.weld_stiffener_alongWeb_h_2Model, self.weld_stiffener_alongWeb_v_1Model, self.weld_stiffener_alongWeb_v_2Model]
        if self.BP.weld_type == 'Fillet Weld':
            welded_sec = [self.weldAbvFlang_11Model, self.weldAbvFlang_12Model, self.weldBelwFlang_11Model, self.weldBelwFlang_12Model,
                          self.weldBelwFlang_13Model, self.weldBelwFlang_14Model, self.weldSideWeb_11Model, self.weldSideWeb_12Model]
        else:
            welded_sec = [self.weldAbvFlang_11Model, self.weldAbvFlang_12Model, self.weldSideWeb_11Model]
        if self.BP.stiffener_along_flange == 'Yes':
            if self.BP.weld_type == "Fillet":
                sec = [self.weld_stiffener_algflng_v1Model, self.weld_stiffener_algflng_v2Model, self.weld_stiffener_algflng_v3Model, self.weld_stiffener_algflng_v4Model,
                              self.weld_stiffener_algflng_h11Model, self.weld_stiffener_algflng_h12Model, self.weld_stiffener_algflng_h21Model, self.weld_stiffener_algflng_h22Model,
                              self.weld_stiffener_algflng_h31Model, self.weld_stiffener_algflng_h32Model, self.weld_stiffener_algflng_h41Model, self.weld_stiffener_algflng_h42Model,]
            else:
                sec = [self.weld_stiffener_algflng_v1Model, self.weld_stiffener_algflng_v2Model,
                              self.weld_stiffener_algflng_v3Model, self.weld_stiffener_algflng_v4Model,
                              self.weld_stiffener_algflag_gh1Model, self.weld_stiffener_algflag_gh2Model,
                       self.weld_stiffener_algflag_gh3Model, self.weld_stiffener_algflag_gh4Model]
            welded_sec.extend(sec)
        if self.BP.stiffener_along_web == 'Yes':
            if 2 * self.BP.anchors_outside_flange == 4 or 2 * self.BP.anchors_outside_flange == 8:
                if self.BP.weld_type == "Fillet":
                    sec = [self.weld_stiffener_alongWeb_v_1Model, self.weld_stiffener_alongWeb_v_2Model,
                                  self.weld_stiffener_alongWeb_h_11Model, self.weld_stiffener_alongWeb_h_21Model,
                                  self.weld_stiffener_alongWeb_h_12Model, self.weld_stiffener_alongWeb_h_22Model]
                else:
                    sec = [self.weld_stiffener_alongWeb_v_1Model, self.weld_stiffener_alongWeb_v_2Model,
                                  self.weld_stiffener_alongWeb_gh1Model, self.weld_stiffener_alongWeb_gh2Model]

            if 2 * self.BP.anchors_outside_flange == 6 or 2 * self.BP.anchors_outside_flange == 12:
                if self.BP.weld_type == "Fillet":
                    sec = [self.weld_stiffener_alongWeb_v_1Model, self.weld_stiffener_alongWeb_v_2Model,
                                  self.weld_stiffener_alongWeb_h_11Model, self.weld_stiffener_alongWeb_h_21Model,
                                  self.weld_stiffener_alongWeb_h_12Model, self.weld_stiffener_alongWeb_h_22Model,
                                  self.weld_stiffener_alongWeb_v_3Model, self.weld_stiffener_alongWeb_v_4Model,
                                  self.weld_stiffener_alongWeb_h_31Model, self.weld_stiffener_alongWeb_h_41Model,
                                  self.weld_stiffener_alongWeb_h_32Model, self.weld_stiffener_alongWeb_h_42Model]

                else:
                    sec = [self.weld_stiffener_alongWeb_v_1Model, self.weld_stiffener_alongWeb_v_2Model,
                                  self.weld_stiffener_alongWeb_gh1Model, self.weld_stiffener_alongWeb_gh2Model,
                                  self.weld_stiffener_alongWeb_gh3Model, self.weld_stiffener_alongWeb_gh4Model,
                                  self.weld_stiffener_alongWeb_v_3Model, self.weld_stiffener_alongWeb_v_4Model]
            welded_sec.extend(sec)

        if self.BP.stiffener_across_web == 'Yes':
            if self.BP.weld_type == "Fillet":
                sec = [self.weld_stiffener_acrsWeb_v1Model, self.weld_stiffener_acrsWeb_v2Model, self.weld_stiffener_acrsWeb_h1Model,
                              self.weld_stiffener_acrsWeb_gh2Model, self.weld_stiffener_acrsWeb_h3Model, self.weld_stiffener_acrsWeb_h4Model]
            else:
                sec = [self.weld_stiffener_acrsWeb_v1Model, self.weld_stiffener_acrsWeb_v2Model,
                              self.weld_stiffener_acrsWeb_gh1Model, self.weld_stiffener_acrsWeb_gh2Model]
            welded_sec.extend(sec)

        if self.BP.stiffener_inside_flange == 'Yes':
            sec = [self.weld_stiffener_inflange11Model, self.weld_stiffener_inflange12Model, self.weld_stiffener_inflange21Model, self.weld_stiffener_inflange22Model, self.weld_stiffener_inflange_d11Model, self.weld_stiffener_inflange_d22Model]
            welded_sec.extend(sec)

        welds = welded_sec[0]

        for comp in welded_sec[1:]:
            welds = BRepAlgoAPI_Fuse(comp, welds).Shape()

        return welds

    def get_plate_connector_models(self):

        # if self.BP.stiffener_along_flange == 'Yes':
        # plate_list = [self.baseplateModel, self.gusset1Model, self.gusset2Model, self.stiffener1Model,
        #               self.stiffener2Model, self.stiffener3Model, self.stiffener4Model]

        plate_list = [self.baseplateModel]
        if self.BP.shear_key_along_ColDepth == 'Yes':
            list = [self.shearkey_1Model]
            plate_list.extend(list)

        if self.BP.shear_key_along_ColWidth == 'Yes':
            list = [self.shearkey_2Model]
            plate_list.extend(list)

        if self.BP.stiffener_along_flange == 'Yes':
            list = [self.stiffener_algflangeL1Model, self.stiffener_algflangeR1Model, self.stiffener_algflangeL2Model,
                          self.stiffener_algflangeR2Model]
            plate_list.extend(list)
        if self.BP.stiffener_along_web == 'Yes':
            if 2 * self.BP.anchors_outside_flange == 4 or 2 * self.BP.anchors_outside_flange == 8:
                list = [self.stiffener1Model, self.stiffener3Model]
                plate_list.extend(list)
            if 2 * self.BP.anchors_outside_flange == 6 or 2 * self.BP.anchors_outside_flange == 12:
                list = [self.stiffener1Model, self.stiffener2Model, self.stiffener3Model, self.stiffener4Model]
                plate_list.extend(list)
        if self.BP.stiffener_across_web == 'Yes':
            list = [self.stiffener_acrsWeb1Model, self.stiffener_acrsWeb2Model]
            plate_list.extend(list)
        if self.BP.stiffener_inside_flange == 'Yes':
            list = [self.stiffener_insideflange1Model,self.stiffener_insideflange2Model]
            plate_list.extend(list)

        plate = plate_list[0]

        for item in plate_list[1:]:
            plate = BRepAlgoAPI_Fuse(plate, item).Shape()

        # else:
        #     plate = self.baseplateModel

        return plate

    def get_grout_models(self):
        grout = self.groutModel

        return grout

    def get_concrete_models(self):
        conc = self.concreteModel
        return conc

    def get_connector_models(self):
        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()

        CAD_list = [plate_connectors, welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD

    def get_models(self):
        column = self.get_column_model()
        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()
        conc = self.get_concrete_models()
        grt = self.get_grout_models()

        CAD_list = [column, plate_connectors, welds, nut_bolt_array, conc, grt]  # , welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD


class HollowBasePlateCad(object):
    def __init__(self, BP, sec, weld_sec, nut_bolt_array, bolthight, baseplate, concrete, grout, stiff_alg_l, stiff_alg_b, weld_stiff_l_v,
                 weld_stiff_l_h, weld_stiff_b_v, weld_stiff_b_h, shearkey_1, shearkey_2):
        """

        """

        self.BP = BP
        self.stiffener_l = True
        self.stiffener_b = True
        self.column = sec
        self.weld_sec = weld_sec
        self.nut_bolt_array = nut_bolt_array
        self.bolthight = bolthight
        self.baseplate = baseplate
        self.concrete = concrete
        self.grout = grout
        self.stiff_alg_l = stiff_alg_l
        self.stiff_alg_b = stiff_alg_b
        self.weld_stiff_l_v = weld_stiff_l_v
        self.weld_stiff_l_h = weld_stiff_l_h
        self.weld_stiff_b_v = weld_stiff_b_v
        self.weld_stiff_b_h = weld_stiff_b_h

        self.stiff_alg_l1 = copy.deepcopy(self.stiff_alg_l)
        self.stiff_alg_b1 = copy.deepcopy(self.stiff_alg_b)
        self.stiff_alg_l2 = copy.deepcopy(self.stiff_alg_l)
        self.stiff_alg_b2 = copy.deepcopy(self.stiff_alg_b)

        self.weld_stiff_l_v1 = copy.deepcopy(self.weld_stiff_l_v)
        self.weld_stiff_l_v2 = copy.deepcopy(self.weld_stiff_l_v)
        self.weld_stiff_l_h1 = copy.deepcopy(self.weld_stiff_l_h)
        self.weld_stiff_l_h2 = copy.deepcopy(self.weld_stiff_l_h)

        self.weld_stiff_b_v1 = copy.deepcopy(self.weld_stiff_b_v)
        self.weld_stiff_b_v2 = copy.deepcopy(self.weld_stiff_b_v)
        self.weld_stiff_b_h1 = copy.deepcopy(self.weld_stiff_b_h)
        self.weld_stiff_b_h2 = copy.deepcopy(self.weld_stiff_b_h)

        self.shearkey_1 = shearkey_1
        self.shearkey_2 = shearkey_2

    def create_3DModel(self):
        """

        """
        self.createcolumnGeometry()
        self.createBasePlateGeometry()
        self.createWeldGeometry()
        self.createConcreteGeometry()
        self.create_nut_bolt_array()
        self.createGroutGeometry()

    def createcolumnGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        columnOriginL = numpy.array([0.0, 0.0, self.weld_sec.H + self.column.H/2])
        columnL_uDir = numpy.array([1.0, 0.0, 0.0])
        columnL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.column.place(columnOriginL, columnL_uDir, columnL_wDir)

        self.columnModel = self.column.create_model()

    def createBasePlateGeometry(self):
        baseplateOriginL = numpy.array([-self.baseplate.W / 2, 0.0, -self.baseplate.T / 2])
        baseplateL_uDir = numpy.array([0.0, 0.0, 1.0])
        baseplateL_wDir = numpy.array([1.0, 0.0, 0.0])
        self.baseplate.place(baseplateOriginL, baseplateL_uDir, baseplateL_wDir)

        self.baseplateModel = self.baseplate.create_model()

        if self.BP.shear_key_along_ColDepth == 'Yes':

            shearkey_1OriginL = numpy.array([-self.shearkey_1.W / 2, 0.0, -self.shearkey_1.T / 2 - self.baseplate.T])
            shearkey_1L_uDir = numpy.array([0.0, 0.0, 1.0])
            shearkey_1L_wDir = numpy.array([1.0, 0.0, 0.0])
            self.shearkey_1.place(shearkey_1OriginL, shearkey_1L_uDir, shearkey_1L_wDir)

            self.shearkey_1Model = self.shearkey_1.create_model()

        if self.BP.shear_key_along_ColWidth == 'Yes':
            shearkey_2OriginL = numpy.array([-self.shearkey_2.W / 2, 0.0, -self.shearkey_2.T / 2 - self.baseplate.T])
            shearkey_2L_uDir = numpy.array([0.0, 0.0, 1.0])
            shearkey_2L_wDir = numpy.array([1.0, 0.0, 0.0])
            self.shearkey_2.place(shearkey_2OriginL, shearkey_2L_uDir, shearkey_2L_wDir)

            self.shearkey_2Model = self.shearkey_2.create_model()


        if self.stiffener_l == True:

            if self.BP.dp_column_designation[1:4] == 'SHS' or self.BP.dp_column_designation[1:4] == 'RHS':
                D = self.column.W
                B = self.column.L
            else:
                D = self.column.r*2
                B = self.column.r*2

            x_axis = self.stiff_alg_l.T/2
            y_axis = D/2 + self.stiff_alg_l.L / 2 + self.weld_stiff_l_v.h
            z_axis = self.stiff_alg_l.W / 2 + self.weld_stiff_l_h.h # + self.weld_stiffener_alongWeb_h.h
            stiff_alg_l1OriginL = numpy.array([x_axis, y_axis, z_axis])
            stiff_alg_l1L_uDir = numpy.array([0.0, -1.0, 0.0])
            stiff_alg_l1L_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.stiff_alg_l1.place(stiff_alg_l1OriginL, stiff_alg_l1L_uDir, stiff_alg_l1L_wDir)

            self.stiff_alg_l1Model = self.stiff_alg_l1.create_model()


            stiff_alg_l2OriginL = numpy.array([-x_axis, -(y_axis), z_axis])
            stiff_alg_l2L_uDir = numpy.array([0.0, 1.0, 0.0])
            stiff_alg_l2L_wDir = numpy.array([1.0, 0.0, 0.0])
            self.stiff_alg_l2.place(stiff_alg_l2OriginL, stiff_alg_l2L_uDir, stiff_alg_l2L_wDir)

            self.stiff_alg_l2Model = self.stiff_alg_l2.create_model()

        if self.stiffener_b == True:
            if self.BP.dp_column_designation[1:4] == 'SHS' or self.BP.dp_column_designation[1:4] == 'RHS':
                D = self.column.W
                B = self.column.L
            else:
                D = self.column.r*2
                B = self.column.r*2

            x_axis = B/2 + self.stiff_alg_b.L / 2 + self.weld_stiff_b_v.h  # todo: add weld ht here
            y_axis = self.stiff_alg_b.T / 2
            z_axis = self.stiff_alg_b2.W / 2 +  self.weld_stiff_b_h.h
            stiff_alg_b1OriginL = numpy.array([-x_axis, y_axis, z_axis])
            stiff_alg_b1L_uDir = numpy.array([1.0, 0.0, 0.0])
            stiff_alg_b1L_wDir = numpy.array([0.0, -1.0, 0.0])
            self.stiff_alg_b1.place(stiff_alg_b1OriginL, stiff_alg_b1L_uDir, stiff_alg_b1L_wDir)

            self.stiff_alg_b1Model = self.stiff_alg_b1.create_model()

            stiff_alg_b2OriginL = numpy.array([x_axis, -(y_axis), z_axis])
            stiff_alg_b2L_uDir = numpy.array([-1.0, 0.0, 0.0])
            stiff_alg_b2L_wDir = numpy.array([0.0, 1.0, 0.0])
            self.stiff_alg_b2.place(stiff_alg_b2OriginL, stiff_alg_b2L_uDir, stiff_alg_b2L_wDir)

            self.stiff_alg_b2Model = self.stiff_alg_b2.create_model()

    def createWeldGeometry(self):
        weld_secOriginL = numpy.array([0.0, 0.0, self.weld_sec.H/2])
        weld_secL_uDir = numpy.array([1.0, 0.0, 0.0])
        weld_secL_wDir = numpy.array([0.0, 0.0, 1.0])

        self.weld_sec.place(weld_secOriginL, weld_secL_uDir, weld_secL_wDir)

        self.weld_secModel = self.weld_sec.create_model()

        if self.stiffener_l == True:
            if self.BP.dp_column_designation[1:4] == 'SHS' or self.BP.dp_column_designation[1:4] == 'RHS':
                D = self.column.W
                B = self.column.L
            else:
                D = self.column.r*2
                B = self.column.r*2

            x_axis = 0.0
            y_axis = D/2 + self. stiff_alg_l.L + self.weld_stiff_l_v.h
            z_axis = self.weld_stiff_l_v.h/2

            stiffenerweldOrigin_h_11 = numpy.array([-x_axis , y_axis, z_axis])
            uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
            wDirAbv_11 = numpy.array([0.0, -1.0, 0])
            self.weld_stiff_l_h1.place(stiffenerweldOrigin_h_11, uDirAbv_11, wDirAbv_11)

            self.weld_stiff_l_h1Model = self.weld_stiff_l_h1.create_model()

            stiffenerweldOrigin_h_21 = numpy.array(
                [-x_axis, -y_axis + self.weld_stiff_l_h2.L, z_axis])
            uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
            wDirAbv_11 = numpy.array([0.0, -1.0, 0])
            self.weld_stiff_l_h2.place(stiffenerweldOrigin_h_21, uDirAbv_11, wDirAbv_11)

            self.weld_stiff_l_h2Model = self.weld_stiff_l_h2.create_model()

            x_axis = self. stiff_alg_l.T / 2
            y_axis = D/2 + self. stiff_alg_l.L + self.weld_stiff_l_v.h
            z_axis = self. stiff_alg_l.R22 + self.weld_stiff_l_v.h
            stiffenerweldOrigin_v_1 = numpy.array(
                [0.0, y_axis - self. stiff_alg_l.L - self.weld_stiff_l_v.h / 2, z_axis])
            uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
            wDirAbv_11 = numpy.array([0.0, 0, 1.0])
            self.weld_stiff_l_v1.place(stiffenerweldOrigin_v_1, uDirAbv_11, wDirAbv_11)

            self.weld_stiff_l_v1Model = self.weld_stiff_l_v1.create_model()

            stiffenerweldOrigin_v_2 = numpy.array(
                [0.0, -y_axis + self. stiff_alg_l.L + self.weld_stiff_l_v.h / 2, z_axis])
            uDirAbv_11 = numpy.array([1.0, 0.0, 0.0])
            wDirAbv_11 = numpy.array([0.0, 0.0, 1.0])
            self.weld_stiff_l_v2.place(stiffenerweldOrigin_v_2, uDirAbv_11, wDirAbv_11)

            self.weld_stiff_l_v2Model = self.weld_stiff_l_v2.create_model()

        if self.stiffener_b == True:
            if self.BP.dp_column_designation[1:4] == 'SHS' or self.BP.dp_column_designation[1:4] == 'RHS':
                D = self.column.W
                B = self.column.L
            else:
                D = self.column.r*2
                B = self.column.r*2
            x_axis = B/2 + self.weld_stiff_b_v.h/2  #todo: add weld ht here
            y_axis = 0.0
            z_axis = self.stiff_alg_b.R22 + self.weld_stiff_b_h.h

            weld_stiff_b_v1OriginL = numpy.array([-x_axis, -y_axis, z_axis])
            weld_stiff_b_v1L_uDir = numpy.array([0.0, 1.0, 0.0])
            weld_stiff_b_v1L_wDir = numpy.array([0.0, 0.0, 1.0])
            self.weld_stiff_b_v1.place(weld_stiff_b_v1OriginL, weld_stiff_b_v1L_uDir, weld_stiff_b_v1L_wDir)

            self.weld_stiff_b_v1Model = self.weld_stiff_b_v1.create_model()

            weld_stiff_b_v2OriginL = numpy.array([x_axis, -(y_axis), z_axis])
            weld_stiff_b_v2L_uDir = numpy.array([0.0, 1.0, 0.0])
            weld_stiff_b_v2L_wDir = numpy.array([0.0, 0.0, 1.0])
            self.weld_stiff_b_v2.place(weld_stiff_b_v2OriginL, weld_stiff_b_v2L_uDir, weld_stiff_b_v2L_wDir)

            self.weld_stiff_b_v2Model = self.weld_stiff_b_v2.create_model()

            x_axis = B/2 + self.weld_stiff_b_v.h + self.stiff_alg_b.R22
            z_axis = self.weld_stiff_b_h.h / 2
            y_axis = 0.0
            weld_stiff_b_h1OriginL = numpy.array([-x_axis - self.weld_stiff_b_h.L, y_axis, z_axis])
            weld_stiff_b_h1L_uDir = numpy.array([0.0, 1.0, 0.0])
            weld_stiff_b_h1L_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weld_stiff_b_h1.place(weld_stiff_b_h1OriginL, weld_stiff_b_h1L_uDir,
                                                  weld_stiff_b_h1L_wDir)

            self.weld_stiff_b_h1Model = self.weld_stiff_b_h1.create_model()

            weld_stiff_b_h2OriginL = numpy.array([x_axis, (y_axis), z_axis])
            weld_stiff_b_h2L_uDir = numpy.array([0.0, 1.0, 0.0])
            weld_stiff_b_h2L_wDir = numpy.array([1.0, 0.0, 0.0])
            self.weld_stiff_b_h2.place(weld_stiff_b_h2OriginL, weld_stiff_b_h2L_uDir,
                                                  weld_stiff_b_h2L_wDir)

            self.weld_stiff_b_h2Model = self.weld_stiff_b_h2.create_model()

    def create_nut_bolt_array(self):
        """

        :return: Geometric Orientation of this component
        """
        # nutboltArrayOrigin = self.baseplate.sec_origin + numpy.array([0.0, 0.0, self.baseplate.T /2+ 100])
        nutboltArrayOrigin = numpy.array([-self.baseplate.W / 2, self.baseplate.L / 2, self.bolthight])
        gaugeDir = numpy.array([1.0, 0, 0])
        pitchDir = numpy.array([0, -1.0, 0])
        boltDir = numpy.array([0, 0, 1.0])
        self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        self.nutBoltArrayModels = self.nut_bolt_array.create_model()

    def createGroutGeometry(self):
        """
        :return: Geometric Orientaion of grout
        """
        groutOriginL = numpy.array([-self.grout.W / 2, 0.0, -self.baseplate.T - self.grout.T / 2])
        groutL_uDir = numpy.array([0.0, 0.0, 1.0])
        groutL_wDir = numpy.array([1.0, 0.0, 0.0])
        self.grout.place(groutOriginL, groutL_uDir, groutL_wDir)

        self.groutModel = self.grout.create_model()

    def createConcreteGeometry(self):
        """

        :return: Geometric Orientation of concrete
        """
        concreteOrigin = numpy.array(
            [-self.concrete.W / 2, 0.0, -self.baseplate.T - self.grout.T - self.concrete.T / 2])
        concrete_uDir = numpy.array([0.0, 0.0, 1.0])
        concrete_wDir = numpy.array([1.0, 0.0, 0.0])
        self.concrete.place(concreteOrigin, concrete_uDir, concrete_wDir)

        self.concreteModel = self.concrete.create_model()

    def get_column_model(self):
        column = self.columnModel
        return column

    def get_nut_bolt_array_models(self):
        nut_bolts = self.nut_bolt_array.get_models()
        array = nut_bolts[0]
        for comp in nut_bolts:
            array = BRepAlgoAPI_Fuse(comp, array).Shape()

        return array

    def get_welded_models(self):
        """

        :return: CAD model for all the fillet welds
        """
        weld_sec = [self.weld_secModel]
        if self.stiffener_l == True:
            sec = [ self.weld_stiff_l_v1Model,  self.weld_stiff_l_v2Model,  self.weld_stiff_l_h1Model,  self.weld_stiff_l_h2Model]
            weld_sec.extend(sec)

        if self.stiffener_b == True:
            sec = [self.weld_stiff_b_v1Model, self.weld_stiff_b_v2Model, self.weld_stiff_b_h1Model, self.weld_stiff_b_h2Model]
            weld_sec.extend(sec)

        weld = weld_sec[0]

        for item in weld_sec[1:]:
            weld = BRepAlgoAPI_Fuse(weld, item).Shape()

        return weld

    def get_plate_connector_models(self):
        plate = self.baseplateModel

        if self.stiffener_l == True:
            plate = BRepAlgoAPI_Fuse(plate, self.stiff_alg_l1Model).Shape()
            plate = BRepAlgoAPI_Fuse(plate, self.stiff_alg_l2Model).Shape()

        if self.stiffener_b == True:
            plate = BRepAlgoAPI_Fuse(plate, self.stiff_alg_b1Model).Shape()
            plate = BRepAlgoAPI_Fuse(plate, self.stiff_alg_b2Model).Shape()

        if self.shearkey_1 == True:
            plate = BRepAlgoAPI_Fuse(plate, self.shearkey_1Model).Shape()

        if self.shearkey_2 == True:
            plate = BRepAlgoAPI_Fuse(plate, self.shearkey_2Model).Shape()

        return plate

    def get_grout_models(self):
        grout = self.groutModel

        return grout

    def get_concrete_models(self):
        conc = self.concreteModel
        return conc

    def get_connector_models(self):
        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()

        CAD_list = [plate_connectors, welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD

    def get_models(self):
        column = self.get_column_model()
        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()
        conc = self.get_concrete_models()
        grt = self.get_grout_models()

        CAD_list = [column, welds, plate_connectors, nut_bolt_array, conc, grt]  # , welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD

if __name__ == '__main__':

    from cad.items.bolt import Bolt
    from cad.items.nut import Nut
    from cad.items.plate import Plate
    from cad.items.ISection import ISection
    from cad.items.filletweld import FilletWeld
    from cad.items.groove_weld import GrooveWeld
    from cad.items.concrete import Concrete
    from cad.BasePlateCad.test_nb import NutBoltArray
    from cad.items.anchor_bolt import *
    from cad.items.nut import Nut
    from cad.items.stiffener_plate import StiffenerPlate
    from cad.items.stiffener_flange import Stiffener_flange
    from cad.items.grout import Grout
    from cad.items.rect_hollow import RectHollow
    from cad.items.circular_hollow import CircularHollow

    import OCC.Core.V3d
    from OCC.Core.Quantity import Quantity_NOC_SADDLEBROWN, Quantity_NOC_BLUE1
    from OCC.Core.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
    from utilities import osdag_display_shape
    # from cad.common_logic import CommonDesignLogic
    from OCC.Core.Quantity import Quantity_NOC_GRAY25 as GRAY

    from OCC.gp import gp_Pnt
    # from OCC.Core.Graphic3d import Quantity_NOC_GRAY as GRAY
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    filletWeldcolm = False
    numberOfBolts = 4
    hollow_sec = True
    Isec = False

    if Isec == True:
        column = ISection(B=250, T=13.7, D=450, t=9.8, R1=15.0, R2=7.5, alpha=94, length=1500, notchObj=None)
        baseplate = Plate(L=700, W=500, T=45)

        if filletWeldcolm ==  True:
            weldAbvFlang = FilletWeld(b=10, h=10, L=250)
            weldBelwFlang = FilletWeld(b=10, h=10, L=100)
            weldSideWeb = FilletWeld(b=10, h=10, L=420)
        else:
            weldAbvFlang = GrooveWeld(b= column.T, h=10, L=column.B)
            weldBelwFlang = GrooveWeld(b= column.T, h=10, L=column.B)
            weldSideWeb = GrooveWeld(b=column.t, h=10, L=column.D)

        # concrete = Concrete(L= baseplate.W*1.5, W= baseplate.L*1.5, T= baseplate.T*10)
        concrete = Plate(L=baseplate.L * 1.5, W=baseplate.W * 1.5, T=baseplate.T * 10)
        grout = Grout(L=baseplate.L + 200, W=baseplate.W + 200, T=50)

        gusset = StiffenerPlate(L=baseplate.W, W=200, T=14, L11=(baseplate.W - (column.B + 100)) / 2, L12=200 - 100,
                                R11=(baseplate.W - (column.B + 100)) / 2, R12=200 - 100)

        stiffener = StiffenerPlate(L=(baseplate.L - column.D - 2 * gusset.T) / 2 - 10, W=gusset.W, T=gusset.T,
                                   L11=(baseplate.L - column.D - 2 * gusset.T) / 2 - 50, L12=gusset.W - 100, R21 = 15, R22 = 15)    #todo: add L21 and L22 as max(15, weldsize + 3)

        stiffener_acrsWeb = StiffenerPlate(L=(baseplate.L - column.D - 2 * gusset.T) / 2 - 10, W=gusset.W, T=gusset.T,
                                   L11=(baseplate.L - column.D - 2 * gusset.T) / 2 - 50, L12=gusset.W - 100, R21 = 15, R22 = 15)    #todo: add L21 and L22 as max(15, weldsize + 3)

        stiffener_algflangeL = Stiffener_flange(H= gusset.W, L = (baseplate.W-column.B)/2 - 10, T = column.T +5, t_f = column.T, L_h= 50, L_v = 100, to_left = True)
        stiffener_algflangeR = Stiffener_flange(H=gusset.W, L=(baseplate.W - column.B) / 2 - 10, T=column.T + 5,
                                               t_f=column.T, L_h=50, L_v=100, to_left=False)
        stiffener_algflange_tapperLength = (stiffener_algflangeR.T - column.T) * 5

        stiffener_insideflange = StiffenerPlate(L= (column.D - 2*column.T - 2 * 6), W= (column.B- column.t - 2*column.R1 - 2 * 5)/2, T =12, R21 = column.R1 + 5, R22= column.R1 + 5, L21 = column.R1 + 5, L22= column.R1 + 5)  #self.extraspace=5

        weld_stiffener_algflng_v = GrooveWeld(b= column.T, h = 10, L = stiffener_algflangeL.H)
        weld_stiffener_algflng_h = FilletWeld(b= 10, h= 10, L= stiffener_algflangeL.L)    #Todo: create another weld for inner side of the stiffener
        weld_stiffener_algflag_gh = GrooveWeld(b= stiffener_algflangeR.T, h = 10, L= stiffener_algflangeL.L - stiffener_algflange_tapperLength )

        weld_stiffener_acrsWeb_v = GrooveWeld(b= stiffener_acrsWeb.T, h = 10, L = stiffener_acrsWeb.W - stiffener_acrsWeb.R22)
        weld_stiffener_acrsWeb_h = FilletWeld(b= 10, h= 10, L = stiffener_acrsWeb.L - stiffener_acrsWeb.R22)
        weld_stiffener_acrsWeb_gh = GrooveWeld(b= stiffener_acrsWeb.T, h = 10, L = stiffener_acrsWeb.L - stiffener_acrsWeb.R22)

        gussetweld = GrooveWeld(b=gusset.T, h = 10, L= gusset.L)
        weld_stiffener_alongWeb_h = FilletWeld(b= 10, h= 10, L=stiffener.L - stiffener.R22)
        weld_stiffener_alongWeb_v = GrooveWeld(b= stiffener.T, h=10, L=stiffener.W - stiffener.R22)
        weld_stiffener_alongWeb_gh = GrooveWeld(b= stiffener.T, h=10, L=stiffener.L - stiffener.R22)

        weld_stiffener_inflange = GrooveWeld(b= stiffener_insideflange.T, h = 6, L = stiffener_insideflange.W - stiffener_insideflange.R22)
        weld_stiffener_inflange_d = GrooveWeld(b= stiffener_insideflange.T, h = 6, L = stiffener_insideflange.L - stiffener_insideflange.R22 - 2*weld_stiffener_inflange.h)

        type = 'gusset'  # 'no_gusset'

        # Todo: Make this class in another file

        ex_length = (50 + 24 + baseplate.T)  # nut.T = 24
        # bolt = AnchorBolt_A(l=250, c=125, a=75, r=12, ex=ex_length)
        # bolt = AnchorBolt_B(l= 250, c= 125, a= 75, r= 12, ex=ex_length)
        bolt = AnchorBolt_Endplate(l= 250, c= 125, a= 75, r= 12, ex=ex_length)
        nut = Nut(R=bolt.r * 3, T=24, H=30, innerR1=bolt.r)
        nutSpace = bolt.c + baseplate.T
        bolthight = nut.T + 50

        nut_bolt_array = NutBoltArray(column, baseplate,  nut, bolt, numberOfBolts, nutSpace)

        basePlate = BasePlateCad(type, column, nut_bolt_array, bolthight, baseplate, weldAbvFlang, weldBelwFlang, weldSideWeb,
                                 concrete, gusset, stiffener, grout, gussetweld, weld_stiffener_alongWeb_h, weld_stiffener_alongWeb_gh, weld_stiffener_alongWeb_v,
                                 stiffener_algflangeL, stiffener_algflangeR, stiffener_acrsWeb, weld_stiffener_algflng_v, weld_stiffener_algflng_h, weld_stiffener_algflag_gh,
                                 weld_stiffener_acrsWeb_v, weld_stiffener_acrsWeb_h, weld_stiffener_acrsWeb_gh, stiffener_insideflange, weld_stiffener_inflange)

    if hollow_sec == True:
        rect_hollow = False
        # circ_hollow = False
        if rect_hollow == True:
            sec = RectHollow(L= 50, W= 100, H=1000, T=4)
            weld_sec = RectHollow(L= sec.L, W= sec.W, H= 10, T= sec.T)

            baseplate = Plate(L=375, W=325, T=18)

            stiff_alg_l = StiffenerPlate(L= (baseplate.L - sec.W)/2 - 10, W= 187.5, T= 4, L11=(baseplate.L - sec.W)/2 - 10 - 50, L12=187.5 - 100, R21=15, R22=15)
            stiff_alg_b = StiffenerPlate(L= (baseplate.W - sec.L)/2 - 10, W= 187.5, T= 4, L11=(baseplate.L - sec.W)/2 - 10 - 50, L12=187.5 - 100, R21=15, R22=15)
            weld_stiff_l_v = GrooveWeld(b=stiff_alg_l.T, h=10, L=stiff_alg_l.W - stiff_alg_l.R22)
            weld_stiff_l_h = GrooveWeld(b=stiff_alg_l.T, h=10, L=stiff_alg_l.L - stiff_alg_l.R22)
            weld_stiff_b_v = GrooveWeld(b=stiff_alg_b.T, h=10, L=stiff_alg_b.W - stiff_alg_b.R22)
            weld_stiff_b_h = GrooveWeld(b=stiff_alg_b.T, h=10, L=stiff_alg_b.L - stiff_alg_b.R22)

            ex_length = 114.5  # (50 + 24 + baseplate.T)  # nut.T = 24
            # bolt = AnchorBolt_A(l=250, c=125, a=75, r=12, ex=ex_length)
            # bolt = AnchorBolt_B(l= 250, c= 125, a= 75, r= 12, ex=ex_length)
            bolt = AnchorBolt_Endplate(l=314.5, c=125, a=75, r=10, ex=ex_length)
            nut = Nut(R=bolt.r * 3, T=24, H=30, innerR1=bolt.r)
            nutSpace = bolt.c + baseplate.T
            bolthight = nut.T + 50
            type = 'rect'

            concrete = Plate(L=baseplate.L * 1.5, W=baseplate.W * 1.5, T=bolt.l * 1.2)
            grout = Grout(L=baseplate.L * 1.5, W=baseplate.W * 1.5, T=50)

            column = ISection(B=250, T=13.7, D=450, t=9.8, R1=15.0, R2=7.5, alpha=94, length=1500, notchObj=None)
        else:
            sec = CircularHollow(r = 200/2, T=12, H= 1500)
            weld_sec = CircularHollow(r = sec.r, T= sec.T, H= 10)

            baseplate = Plate(L=375, W=325, T=18)

            stiff_alg_l = StiffenerPlate(L= baseplate.L/2 - sec.r -10, W= 187.5, T= 4, L11=baseplate.L/2 - sec.r -10 - 50, L12=187.5 - 100, R21=15, R22=15)
            stiff_alg_b = StiffenerPlate(L= baseplate.W/2 - sec.r -10, W= 187.5, T= 4, L11=baseplate.L/2 - sec.r -10 - 50, L12=187.5 - 100, R21=15, R22=15)
            weld_stiff_l_v = GrooveWeld(b=stiff_alg_l.T, h=10, L=stiff_alg_l.W - stiff_alg_l.R22)
            weld_stiff_l_h = GrooveWeld(b=stiff_alg_l.T, h=10, L=stiff_alg_l.L - stiff_alg_l.R22)
            weld_stiff_b_v = GrooveWeld(b=stiff_alg_b.T, h=10, L=stiff_alg_b.W - stiff_alg_b.R22)
            weld_stiff_b_h = GrooveWeld(b=stiff_alg_b.T, h=10, L=stiff_alg_b.L - stiff_alg_b.R22)

            ex_length = 114.5 #(50 + 24 + baseplate.T)  # nut.T = 24
            # bolt = AnchorBolt_A(l=250, c=125, a=75, r=12, ex=ex_length)
            # bolt = AnchorBolt_B(l= 250, c= 125, a= 75, r= 12, ex=ex_length)
            bolt = AnchorBolt_Endplate(l= 314.5, c= 125, a= 75, r= 10, ex=ex_length)
            nut = Nut(R=bolt.r * 3, T=24, H=30, innerR1=bolt.r)
            nutSpace = bolt.c + baseplate.T
            bolthight = nut.T + 50
            type = 'rect'

            concrete = Plate(L=baseplate.L * 1.5, W=baseplate.W * 1.5, T=bolt.l * 1.2)
            grout = Grout(L=baseplate.L * 1.5, W=baseplate.W *1.5, T=50)

            column = ISection(B=250, T=13.7, D=450, t=9.8, R1=15.0, R2=7.5, alpha=94, length=1500, notchObj=None)
        nut_bolt_array = NutBoltArray(column, baseplate, nut, bolt, numberOfBolts, nutSpace)

        basePlate = HollowBasePlateCad(type, sec, weld_sec, nut_bolt_array, bolthight, baseplate, concrete, grout, stiff_alg_l, stiff_alg_b, weld_stiff_l_v, weld_stiff_l_h, weld_stiff_b_v, weld_stiff_b_h)


    basePlate.create_3DModel()
    prism = basePlate.get_models()
    column = basePlate.get_column_model()
    plate = basePlate.get_plate_connector_models()
    weld = basePlate.get_welded_models()
    nut_bolt = basePlate.get_nut_bolt_array_models()
    conc = basePlate.get_concrete_models()
    grt = basePlate.get_grout_models()

    # Point = gp_Pnt(0.0, 0.0, 0.0)
    # display.DisplayMessage(Point, "Origin")

    # p2 = gp_Pnt(0.0, -baseplate.W/2, -baseplate.T/2)
    # display.DisplayMessage(p2, "BasePlate")

    # display.DisplayShape(prism, update=True)
    display.DisplayShape(column, update=True)
    display.DisplayColoredShape(plate, color='BLUE', update=True)
    display.DisplayColoredShape(weld, color='RED', update=True)
    display.DisplayColoredShape(nut_bolt, color='YELLOW', update=True)
    display.DisplayShape(conc, color= GRAY,transparency=0.5, update=True)
    display.DisplayShape(grt, color= GRAY,update=True)

    display.View_Iso()
    # # display.View_Top()
    # # display.View_Right()
    # display.View_Front()

    display.DisableAntiAliasing()
    start_display()


# display.ExportToImage("/home/rahul/Osdag_workspace/3DtestbasePlatw.png")

# display = CommonDesignLogic.display
# display.EraseAll()
# display.View_Iso()
# display.FitAll()
# display.DisableAntiAliasing()
#
# if bgcolor == "gradient_bg":
#
#     display.set_bg_gradient_color([51, 51, 102], [150, 150, 170])
# else:
#     display.set_bg_gradient_color([255, 255, 255], [255, 255, 255])
#
# osdag_display_shape(self.display, basePlate.get_models(), update=True, color='Blue')