"""
created on 14-04-2020

"""

import numpy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from cad.items.plate import Plate
import copy


class CCSpliceCoverPlateWeldedCAD(object):
    def __init__(self, C, column, flangePlate, innerFlangePlate, webPlate, flangePlateWeldL, flangePlateWeldW,
                 innerflangePlateWeldL, innerflangePlateWeldW, webPlateWeldL, webPlateWeldW):

        self.C = C
        self.column = column
        self.flangePlate = flangePlate
        self.innerFlangePlate = innerFlangePlate
        self.webPlate = webPlate
        self.flangePlateWeldL = flangePlateWeldL
        self.flangePlateWeldW = flangePlateWeldW
        self.webPlateWeldL = webPlateWeldL
        self.webPlateWeldW = webPlateWeldW
        self.innerflangePlateWeldL = innerflangePlateWeldL
        self.innerflangePlateWeldW = innerflangePlateWeldW

        self.gap = float(self.C.flange_plate.gap)
        self.flangespace = float(self.C.flangespace)
        self.webspace = float(self.C.webspace)

        self.column1 = copy.deepcopy(self.column)
        self.column2 = copy.deepcopy(self.column)

        self.flangePlate1 = copy.deepcopy(self.flangePlate)
        self.flangePlate2 = copy.deepcopy(self.flangePlate)

        self.innerFlangePlate1 = copy.deepcopy(self.innerFlangePlate)
        self.innerFlangePlate2 = copy.deepcopy(self.innerFlangePlate)
        self.innerFlangePlate3 = copy.deepcopy(self.innerFlangePlate)
        self.innerFlangePlate4 = copy.deepcopy(self.innerFlangePlate)

        self.webPlate1 = copy.deepcopy(self.webPlate)
        self.webPlate2 = copy.deepcopy(self.webPlate)

        # nuber top to bottom
        self.flangePlateWeldL11 = copy.deepcopy(self.flangePlateWeldL)
        self.flangePlateWeldL12 = copy.deepcopy(self.flangePlateWeldL)
        self.flangePlateWeldL21 = copy.deepcopy(self.flangePlateWeldL)
        self.flangePlateWeldL22 = copy.deepcopy(self.flangePlateWeldL)

        self.flangePlateWeldW11 = copy.deepcopy(self.flangePlateWeldW)
        self.flangePlateWeldW12 = copy.deepcopy(self.flangePlateWeldW)
        self.flangePlateWeldW21 = copy.deepcopy(self.flangePlateWeldW)
        self.flangePlateWeldW22 = copy.deepcopy(self.flangePlateWeldW)

        # Todo: update numbering
        self.webPlateWeldL11 = copy.deepcopy(self.webPlateWeldL)
        self.webPlateWeldL12 = copy.deepcopy(self.webPlateWeldL)
        self.webPlateWeldL21 = copy.deepcopy(self.webPlateWeldL)
        self.webPlateWeldL22 = copy.deepcopy(self.webPlateWeldL)

        self.webPlateWeldW11 = copy.deepcopy(self.webPlateWeldW)
        self.webPlateWeldW12 = copy.deepcopy(self.webPlateWeldW)
        self.webPlateWeldW21 = copy.deepcopy(self.webPlateWeldW)
        self.webPlateWeldW22 = copy.deepcopy(self.webPlateWeldW)

        # numbering is clock wise starting from right side top plate
        self.innerflangePlateWeldL11 = copy.deepcopy(self.innerflangePlateWeldL)
        self.innerflangePlateWeldL12 = copy.deepcopy(self.innerflangePlateWeldL)
        self.innerflangePlateWeldL21 = copy.deepcopy(self.innerflangePlateWeldL)
        self.innerflangePlateWeldL22 = copy.deepcopy(self.innerflangePlateWeldL)
        self.innerflangePlateWeldL31 = copy.deepcopy(self.innerflangePlateWeldL)
        self.innerflangePlateWeldL32 = copy.deepcopy(self.innerflangePlateWeldL)
        self.innerflangePlateWeldL41 = copy.deepcopy(self.innerflangePlateWeldL)
        self.innerflangePlateWeldL42 = copy.deepcopy(self.innerflangePlateWeldL)

        self.innerflangePlateWeldW11 = copy.deepcopy(self.innerflangePlateWeldW)
        self.innerflangePlateWeldW12 = copy.deepcopy(self.innerflangePlateWeldW)
        self.innerflangePlateWeldW21 = copy.deepcopy(self.innerflangePlateWeldW)
        self.innerflangePlateWeldW22 = copy.deepcopy(self.innerflangePlateWeldW)
        self.innerflangePlateWeldW31 = copy.deepcopy(self.innerflangePlateWeldW)
        self.innerflangePlateWeldW32 = copy.deepcopy(self.innerflangePlateWeldW)
        self.innerflangePlateWeldW41 = copy.deepcopy(self.innerflangePlateWeldW)
        self.innerflangePlateWeldW42 = copy.deepcopy(self.innerflangePlateWeldW)

        self.weldCutPlate = Plate(L=self.column.D + 4 * self.flangePlate.T, W=self.column.B + 2 * self.flangePlate.T,
                                  T=self.gap)

    def create_3DModel(self):
        '''
        :return:  CAD model of each of the followings. Debugging each command below would give give clear picture
        '''

        self.createColumnGeometry()
        self.createPlateGeometry()
        self.createWeldedGeometry()


    def createColumnGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        column1Origin = numpy.array([0.0, 0.0, self.gap / 2])
        column1_uDir = numpy.array([1.0, 0.0, 0.0])
        column1_wDir = numpy.array([0.0, 0.0, 1.0])
        self.column1.place(column1Origin, column1_uDir, column1_wDir)

        self.column1Model = self.column1.create_model()

        column2Origin = numpy.array([0.0, 0.0, -self.gap / 2])
        column2_uDir = numpy.array([1.0, 0.0, 0.0])
        column2_wDir = numpy.array([0.0, 0.0, -1.0])
        self.column2.place(column2Origin, column2_uDir, column2_wDir)

        self.column2Model = self.column2.create_model()

    def createPlateGeometry(self):
        flangePlate1Origin = numpy.array([-self.flangePlate.W / 2, (self.column.D + self.flangePlate.T) / 2, 0.0])
        flangePlate1_uDir = numpy.array([0.0, 1.0, 0.0])
        flangePlate1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.flangePlate1.place(flangePlate1Origin, flangePlate1_uDir, flangePlate1_wDir)

        self.flangePlate1Model = self.flangePlate1.create_model()

        flangePlate2Origin = numpy.array([-self.flangePlate.W / 2, -(self.column.D + self.flangePlate.T) / 2, 0.0])
        flangePlate2_uDir = numpy.array([0.0, 1.0, 0.0])
        flangePlate2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.flangePlate2.place(flangePlate2Origin, flangePlate2_uDir, flangePlate2_wDir)

        self.flangePlate2Model = self.flangePlate2.create_model()

        webPlate1Origin = numpy.array([(self.column.t + self.webPlate.T) / 2, -self.webPlate.W / 2, 0.0])
        webPlate1_uDir = numpy.array([1.0, 0.0, 0.0])
        webPlate1_wDir = numpy.array([0.0, 1.0, 0.0])
        self.webPlate1.place(webPlate1Origin, webPlate1_uDir, webPlate1_wDir)

        self.webPlate1Model = self.webPlate1.create_model()

        webPlate2Origin = numpy.array([-(self.column.t + self.webPlate.T) / 2, -self.webPlate.W / 2, 0.0])
        webPlate2_uDir = numpy.array([1.0, 0.0, 0.0])
        webPlate2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.webPlate2.place(webPlate2Origin, webPlate2_uDir, webPlate2_wDir)

        self.webPlate2Model = self.webPlate2.create_model()

        if self.C.preference != 'Outside':
            innerFlangePlatespacing = self.flangespace + self.column.t / 2 + self.column.R1
            innerFlangePlate1Origin = numpy.array(
                [innerFlangePlatespacing, (self.column.D - self.innerFlangePlate.T) / 2 - self.column.T, 0.0])
            innerFlangePlate1_uDir = numpy.array([0.0, 1.0, 0.0])
            innerFlangePlate1_wDir = numpy.array([1.0, 0.0, 0.0])
            self.innerFlangePlate1.place(innerFlangePlate1Origin, innerFlangePlate1_uDir, innerFlangePlate1_wDir)

            self.innerFlangePlate1Model = self.innerFlangePlate1.create_model()

            innerFlangePlate2Origin = numpy.array(
                [innerFlangePlatespacing, -(self.column.D - self.innerFlangePlate.T) / 2 + self.column.T, 0.0])
            innerFlangePlate2_uDir = numpy.array([0.0, 1.0, 0.0])
            innerFlangePlate2_wDir = numpy.array([1.0, 0.0, 0.0])
            self.innerFlangePlate2.place(innerFlangePlate2Origin, innerFlangePlate2_uDir, innerFlangePlate2_wDir)

            self.innerFlangePlate2Model = self.innerFlangePlate2.create_model()

            innerFlangePlate3Origin = numpy.array(
                [-innerFlangePlatespacing, -(self.column.D - -- self.innerFlangePlate.T) / 2 + self.column.T, 0.0])
            innerFlangePlate3_uDir = numpy.array([0.0, 1.0, 0.0])
            innerFlangePlate3_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.innerFlangePlate3.place(innerFlangePlate3Origin, innerFlangePlate3_uDir, innerFlangePlate3_wDir)

            self.innerFlangePlate3Model = self.innerFlangePlate3.create_model()

            innerFlangePlate4Origin = numpy.array(
                [-innerFlangePlatespacing, (self.column.D - self.innerFlangePlate.T) / 2 - self.column.T, 0.0])
            innerFlangePlate4_uDir = numpy.array([0.0, 1.0, 0.0])
            innerFlangePlate4_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.innerFlangePlate4.place(innerFlangePlate4Origin, innerFlangePlate4_uDir, innerFlangePlate4_wDir)

            self.innerFlangePlate4Model = self.innerFlangePlate4.create_model()

    def createWeldedGeometry(self):

        # Flangeplate1
        flangePlateWeldL11Origin = numpy.array(
            [self.flangePlate.W / 2, (self.column.D) / 2, self.flangePlateWeldL.L / 2])
        flangePlateWeldL11_uDir = numpy.array([0.0, 1.0, 0.0])
        flangePlateWeldL11_wDir = numpy.array([0.0, 0.0, -1.0])
        self.flangePlateWeldL11.place(flangePlateWeldL11Origin, flangePlateWeldL11_uDir, flangePlateWeldL11_wDir)

        self.flangePlateWeldL11Model = self.flangePlateWeldL11.create_model()

        flangePlateWeldL12Origin = numpy.array(
            [-self.flangePlate.W / 2, (self.column.D) / 2, -self.flangePlateWeldL.L / 2])
        flangePlateWeldL12_uDir = numpy.array([0.0, 1.0, 0.0])
        flangePlateWeldL12_wDir = numpy.array([0.0, 0.0, 1.0])
        self.flangePlateWeldL12.place(flangePlateWeldL12Origin, flangePlateWeldL12_uDir, flangePlateWeldL12_wDir)

        self.flangePlateWeldL12Model = self.flangePlateWeldL12.create_model()

        flangePlateWeldW11Origin = numpy.array(
            [-self.flangePlate.W / 2, (self.column.D) / 2, self.flangePlateWeldL.L / 2])
        flangePlateWeldW11_uDir = numpy.array([0.0, 1.0, 0.0])
        flangePlateWeldW11_wDir = numpy.array([1.0, 0.0, 0.0])
        self.flangePlateWeldW11.place(flangePlateWeldW11Origin, flangePlateWeldW11_uDir, flangePlateWeldW11_wDir)

        self.flangePlateWeldW11Model = self.flangePlateWeldW11.create_model()

        flangePlateWeldW12Origin = numpy.array(
            [self.flangePlate.W / 2, (self.column.D) / 2, -self.flangePlateWeldL.L / 2])
        flangePlateWeldW12_uDir = numpy.array([0.0, 1.0, 0.0])
        flangePlateWeldW12_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.flangePlateWeldW12.place(flangePlateWeldW12Origin, flangePlateWeldW12_uDir, flangePlateWeldW12_wDir)

        self.flangePlateWeldW12Model = self.flangePlateWeldW12.create_model()

        # FlangePlate2
        flangePlateWeldL21Origin = numpy.array(
            [self.flangePlate.W / 2, -(self.column.D) / 2, -self.flangePlateWeldL.L / 2])
        flangePlateWeldL21_uDir = numpy.array([0.0, -1.0, 0.0])
        flangePlateWeldL21_wDir = numpy.array([0.0, 0.0, 1.0])
        self.flangePlateWeldL21.place(flangePlateWeldL21Origin, flangePlateWeldL21_uDir, flangePlateWeldL21_wDir)

        self.flangePlateWeldL21Model = self.flangePlateWeldL21.create_model()

        flangePlateWeldL22Origin = numpy.array(
            [-self.flangePlate.W / 2, -(self.column.D) / 2, self.flangePlateWeldL.L / 2])
        flangePlateWeldL22_uDir = numpy.array([0.0, -1.0, 0.0])
        flangePlateWeldL22_wDir = numpy.array([0.0, 0.0, -1.0])
        self.flangePlateWeldL22.place(flangePlateWeldL22Origin, flangePlateWeldL22_uDir, flangePlateWeldL22_wDir)

        self.flangePlateWeldL22Model = self.flangePlateWeldL22.create_model()

        flangePlateWeldW21Origin = numpy.array(
            [self.flangePlate.W / 2, -(self.column.D) / 2, self.flangePlateWeldL.L / 2])
        flangePlateWeldW21_uDir = numpy.array([0.0, -1.0, 0.0])
        flangePlateWeldW21_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.flangePlateWeldW21.place(flangePlateWeldW21Origin, flangePlateWeldW21_uDir, flangePlateWeldW21_wDir)

        self.flangePlateWeldW21Model = self.flangePlateWeldW21.create_model()

        flangePlateWeldW22Origin = numpy.array(
            [-self.flangePlate.W / 2, -(self.column.D) / 2, -self.flangePlateWeldL.L / 2])
        flangePlateWeldW22_uDir = numpy.array([0.0, -1.0, 0.0])
        flangePlateWeldW22_wDir = numpy.array([1.0, 0.0, 0.0])
        self.flangePlateWeldW22.place(flangePlateWeldW22Origin, flangePlateWeldW22_uDir, flangePlateWeldW22_wDir)

        self.flangePlateWeldW22Model = self.flangePlateWeldW22.create_model()

        # Webplate1 (right side)
        webPlateWeldL11Origin = numpy.array([(self.column.t) / 2, self.webPlate.W / 2, -self.webPlate.L / 2])
        webPlateWeldL11_uDir = numpy.array([1.0, 0.0, 0.0])
        webPlateWeldL11_wDir = numpy.array([0.0, 0.0, 1.0])
        self.webPlateWeldL11.place(webPlateWeldL11Origin, webPlateWeldL11_uDir, webPlateWeldL11_wDir)

        self.webPlateWeldL11Model = self.webPlateWeldL11.create_model()

        webPlateWeldL12Origin = numpy.array([(self.column.t) / 2, -self.webPlate.W / 2, -self.webPlate.L / 2])
        webPlateWeldL12_uDir = numpy.array([0.0, -1.0, 0.0])
        webPlateWeldL12_wDir = numpy.array([0.0, 0.0, 1.0])
        self.webPlateWeldL12.place(webPlateWeldL12Origin, webPlateWeldL12_uDir, webPlateWeldL12_wDir)

        self.webPlateWeldL12Model = self.webPlateWeldL12.create_model()

        webPlateWeldW11Origin = numpy.array([(self.column.t) / 2, self.webPlate.W / 2, self.webPlate.L / 2])
        webPlateWeldW11_uDir = numpy.array([1.0, 0.0, 0.0])
        webPlateWeldW11_wDir = numpy.array([0.0, -1.0, 0.0])
        self.webPlateWeldW11.place(webPlateWeldW11Origin, webPlateWeldW11_uDir, webPlateWeldW11_wDir)

        self.webPlateWeldW11Model = self.webPlateWeldW11.create_model()

        webPlateWeldW12Origin = numpy.array([(self.column.t) / 2, -self.webPlate.W / 2, -self.webPlate.L / 2])
        webPlateWeldW12_uDir = numpy.array([1.0, 0.0, 0.0])
        webPlateWeldW12_wDir = numpy.array([0.0, 1.0, 0.0])
        self.webPlateWeldW12.place(webPlateWeldW12Origin, webPlateWeldW12_uDir, webPlateWeldW12_wDir)

        self.webPlateWeldW12Model = self.webPlateWeldW12.create_model()

        # Webplate2
        webPlateWeldL21Origin = numpy.array([-(self.column.t) / 2, -self.webPlate.W / 2, -self.webPlate.L / 2])
        webPlateWeldL21_uDir = numpy.array([-1.0, 0.0, 0.0])
        webPlateWeldL21_wDir = numpy.array([0.0, 0.0, 1.0])
        self.webPlateWeldL21.place(webPlateWeldL21Origin, webPlateWeldL21_uDir, webPlateWeldL21_wDir)

        self.webPlateWeldL21Model = self.webPlateWeldL21.create_model()

        webPlateWeldL22Origin = numpy.array([-(self.column.t) / 2, self.webPlate.W / 2, self.webPlate.L / 2])
        webPlateWeldL22_uDir = numpy.array([-1.0, 0.0, 0.0])
        webPlateWeldL22_wDir = numpy.array([0.0, 0.0, -1.0])
        self.webPlateWeldL22.place(webPlateWeldL22Origin, webPlateWeldL22_uDir, webPlateWeldL22_wDir)

        self.webPlateWeldL22Model = self.webPlateWeldL22.create_model()

        webPlateWeldW21Origin = numpy.array([-(self.column.t) / 2, -self.webPlate.W / 2, self.webPlate.L / 2])
        webPlateWeldW21_uDir = numpy.array([-1.0, 0.0, 0.0])
        webPlateWeldW21_wDir = numpy.array([0.0, 1.0, 0.0])
        self.webPlateWeldW21.place(webPlateWeldW21Origin, webPlateWeldW21_uDir, webPlateWeldW21_wDir)

        self.webPlateWeldW21Model = self.webPlateWeldW21.create_model()

        webPlateWeldW22Origin = numpy.array([-(self.column.t) / 2, self.webPlate.W / 2, -self.webPlate.L / 2])
        webPlateWeldW22_uDir = numpy.array([-1.0, 0.0, 0.0])
        webPlateWeldW22_wDir = numpy.array([0.0, -1.0, 0.0])
        self.webPlateWeldW22.place(webPlateWeldW22Origin, webPlateWeldW22_uDir, webPlateWeldW22_wDir)

        self.webPlateWeldW22Model = self.webPlateWeldW22.create_model()

        if self.C.preference != 'Outside':
            # innerplate1 (right top)
            innerFlangePlatespacing = self.flangespace + self.column.t / 2 + self.column.R1
            innerflangePlateWeldL11Origin = numpy.array(
                [innerFlangePlatespacing + self.innerFlangePlate.W, (self.column.D) / 2 - self.column.T,
                 -self.innerFlangePlate.L / 2])
            innerflangePlateWeldL11_uDir = numpy.array([0.0, -1.0, 0.0])
            innerflangePlateWeldL11_wDir = numpy.array([0.0, 0.0, 1.0])
            self.innerflangePlateWeldL11.place(innerflangePlateWeldL11Origin, innerflangePlateWeldL11_uDir,
                                               innerflangePlateWeldL11_wDir)

            self.innerflangePlateWeldL11Model = self.innerflangePlateWeldL11.create_model()

            innerflangePlateWeldL12Origin = numpy.array(
                [innerFlangePlatespacing, (self.column.D) / 2 - self.column.T, self.innerFlangePlate.L / 2])
            innerflangePlateWeldL12_uDir = numpy.array([0.0, -1.0, 0.0])
            innerflangePlateWeldL12_wDir = numpy.array([0.0, 0.0, -1.0])
            self.innerflangePlateWeldL12.place(innerflangePlateWeldL12Origin, innerflangePlateWeldL12_uDir,
                                               innerflangePlateWeldL12_wDir)

            self.innerflangePlateWeldL12Model = self.innerflangePlateWeldL12.create_model()

            innerflangePlateWeldW11Origin = numpy.array(
                [innerFlangePlatespacing + self.innerFlangePlate.W, (self.column.D) / 2 - self.column.T,
                 self.innerFlangePlate.L / 2])
            innerflangePlateWeldW11_uDir = numpy.array([0.0, -1.0, 0.0])
            innerflangePlateWeldW11_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.innerflangePlateWeldW11.place(innerflangePlateWeldW11Origin, innerflangePlateWeldW11_uDir,
                                               innerflangePlateWeldW11_wDir)

            self.innerflangePlateWeldW11Model = self.innerflangePlateWeldW11.create_model()

            innerflangePlateWeldW12Origin = numpy.array(
                [innerFlangePlatespacing, (self.column.D) / 2 - self.column.T, -self.innerFlangePlate.L / 2])
            innerflangePlateWeldW12_uDir = numpy.array([0.0, -1.0, 0.0])
            innerflangePlateWeldW12_wDir = numpy.array([1.0, 0.0, 0.0])
            self.innerflangePlateWeldW12.place(innerflangePlateWeldW12Origin, innerflangePlateWeldW12_uDir,
                                               innerflangePlateWeldW12_wDir)

            self.innerflangePlateWeldW12Model = self.innerflangePlateWeldW12.create_model()

            # innerplate2 (top left)
            innerflangePlateWeldL21Origin = numpy.array(
                [-innerFlangePlatespacing, (self.column.D) / 2 - self.column.T, -self.innerFlangePlate.L / 2])
            innerflangePlateWeldL21_uDir = numpy.array([0.0, -1.0, 0.0])
            innerflangePlateWeldL21_wDir = numpy.array([0.0, 0.0, 1.0])
            self.innerflangePlateWeldL21.place(innerflangePlateWeldL21Origin, innerflangePlateWeldL21_uDir,
                                               innerflangePlateWeldL21_wDir)

            self.innerflangePlateWeldL21Model = self.innerflangePlateWeldL21.create_model()

            innerflangePlateWeldL22Origin = numpy.array(
                [-innerFlangePlatespacing - self.innerFlangePlate.W, (self.column.D) / 2 - self.column.T,
                 self.innerFlangePlate.L / 2])
            innerflangePlateWeldL22_uDir = numpy.array([0.0, -1.0, 0.0])
            innerflangePlateWeldL22_wDir = numpy.array([0.0, 0.0, -1.0])
            self.innerflangePlateWeldL22.place(innerflangePlateWeldL22Origin, innerflangePlateWeldL22_uDir,
                                               innerflangePlateWeldL22_wDir)

            self.innerflangePlateWeldL22Model = self.innerflangePlateWeldL22.create_model()

            innerflangePlateWeldW21Origin = numpy.array(
                [-innerFlangePlatespacing, (self.column.D) / 2 - self.column.T, self.innerFlangePlate.L / 2])
            innerflangePlateWeldW21_uDir = numpy.array([0.0, -1.0, 0.0])
            innerflangePlateWeldW21_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.innerflangePlateWeldW21.place(innerflangePlateWeldW21Origin, innerflangePlateWeldW21_uDir,
                                               innerflangePlateWeldW21_wDir)

            self.innerflangePlateWeldW21Model = self.innerflangePlateWeldW21.create_model()

            innerflangePlateWeldW22Origin = numpy.array(
                [-innerFlangePlatespacing - self.innerFlangePlate.W, (self.column.D) / 2 - self.column.T,
                 -self.innerFlangePlate.L / 2])
            innerflangePlateWeldW22_uDir = numpy.array([0.0, -1.0, 0.0])
            innerflangePlateWeldW22_wDir = numpy.array([1.0, 0.0, 0.0])
            self.innerflangePlateWeldW22.place(innerflangePlateWeldW22Origin, innerflangePlateWeldW22_uDir,
                                               innerflangePlateWeldW22_wDir)

            self.innerflangePlateWeldW22Model = self.innerflangePlateWeldW22.create_model()

            # innerplate3 (Right bottom)
            innerflangePlateWeldL31Origin = numpy.array(
                [innerFlangePlatespacing + self.innerFlangePlate.W, -(self.column.D) / 2 + self.column.T,
                 self.innerFlangePlate.L / 2])
            innerflangePlateWeldL31_uDir = numpy.array([0.0, 1.0, 0.0])
            innerflangePlateWeldL31_wDir = numpy.array([0.0, 0.0, -1.0])
            self.innerflangePlateWeldL31.place(innerflangePlateWeldL31Origin, innerflangePlateWeldL31_uDir,
                                               innerflangePlateWeldL31_wDir)

            self.innerflangePlateWeldL31Model = self.innerflangePlateWeldL31.create_model()

            innerflangePlateWeldL32Origin = numpy.array(
                [innerFlangePlatespacing, -(self.column.D) / 2 + self.column.T, -self.innerFlangePlate.L / 2])
            innerflangePlateWeldL32_uDir = numpy.array([0.0, 1.0, 0.0])
            innerflangePlateWeldL32_wDir = numpy.array([0.0, 0.0, 1.0])
            self.innerflangePlateWeldL32.place(innerflangePlateWeldL32Origin, innerflangePlateWeldL32_uDir,
                                               innerflangePlateWeldL32_wDir)

            self.innerflangePlateWeldL32Model = self.innerflangePlateWeldL32.create_model()

            innerflangePlateWeldW31Origin = numpy.array(
                [innerFlangePlatespacing, -(self.column.D) / 2 + self.column.T, self.innerFlangePlate.L / 2])
            innerflangePlateWeldW31_uDir = numpy.array([0.0, 1.0, 0.0])
            innerflangePlateWeldW31_wDir = numpy.array([1.0, 0.0, 0.0])
            self.innerflangePlateWeldW31.place(innerflangePlateWeldW31Origin, innerflangePlateWeldW31_uDir,
                                               innerflangePlateWeldW31_wDir)

            self.innerflangePlateWeldW31Model = self.innerflangePlateWeldW31.create_model()

            innerflangePlateWeldW32Origin = numpy.array(
                [innerFlangePlatespacing + self.innerFlangePlate.W, -(self.column.D) / 2 + self.column.T,
                 -self.innerFlangePlate.L / 2])
            innerflangePlateWeldW32_uDir = numpy.array([0.0, 1.0, 0.0])
            innerflangePlateWeldW32_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.innerflangePlateWeldW32.place(innerflangePlateWeldW32Origin, innerflangePlateWeldW32_uDir,
                                               innerflangePlateWeldW32_wDir)

            self.innerflangePlateWeldW32Model = self.innerflangePlateWeldW32.create_model()

            # innetplate4 (left bottom)
            innerflangePlateWeldL41Origin = numpy.array(
                [-innerFlangePlatespacing, -(self.column.D) / 2 + self.column.T, self.innerFlangePlate.L / 2])
            innerflangePlateWeldL41_uDir = numpy.array([0.0, 1.0, 0.0])
            innerflangePlateWeldL41_wDir = numpy.array([0.0, 0.0, -1.0])
            self.innerflangePlateWeldL41.place(innerflangePlateWeldL41Origin, innerflangePlateWeldL41_uDir,
                                               innerflangePlateWeldL41_wDir)

            self.innerflangePlateWeldL41Model = self.innerflangePlateWeldL41.create_model()

            innerflangePlateWeldL42Origin = numpy.array(
                [-innerFlangePlatespacing - self.innerFlangePlate.W, -(self.column.D) / 2 + self.column.T,
                 -self.innerFlangePlate.L / 2])
            innerflangePlateWeldL42_uDir = numpy.array([0.0, 1.0, 0.0])
            innerflangePlateWeldL42_wDir = numpy.array([0.0, 0.0, 1.0])
            self.innerflangePlateWeldL42.place(innerflangePlateWeldL42Origin, innerflangePlateWeldL42_uDir,
                                               innerflangePlateWeldL42_wDir)

            self.innerflangePlateWeldL42Model = self.innerflangePlateWeldL42.create_model()

            innerflangePlateWeldW41Origin = numpy.array(
                [-innerFlangePlatespacing - self.innerFlangePlate.W, -(self.column.D) / 2 + self.column.T,
                 self.innerFlangePlate.L / 2])
            innerflangePlateWeldW41_uDir = numpy.array([0.0, 1.0, 0.0])
            innerflangePlateWeldW41_wDir = numpy.array([1.0, 0.0, 0.0])
            self.innerflangePlateWeldW41.place(innerflangePlateWeldW41Origin, innerflangePlateWeldW41_uDir,
                                               innerflangePlateWeldW41_wDir)

            self.innerflangePlateWeldW41Model = self.innerflangePlateWeldW41.create_model()

            innerflangePlateWeldW42Origin = numpy.array(
                [-innerFlangePlatespacing, -(self.column.D) / 2 + self.column.T, -self.innerFlangePlate.L / 2])
            innerflangePlateWeldW42_uDir = numpy.array([0.0, 1.0, 0.0])
            innerflangePlateWeldW42_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.innerflangePlateWeldW42.place(innerflangePlateWeldW42Origin, innerflangePlateWeldW42_uDir,
                                               innerflangePlateWeldW42_wDir)

            self.innerflangePlateWeldW42Model = self.innerflangePlateWeldW42.create_model()

        # to cut the welds
        weldCutPlateOrigin = numpy.array([-self.weldCutPlate.W / 2, 0.0, 0.0])
        weldCutPlate_uDir = numpy.array([0.0, 0.0, 1.0])
        weldCutPlate_wDir = numpy.array([1.0, 0.0, 0.0])
        self.weldCutPlate.place(weldCutPlateOrigin, weldCutPlate_uDir, weldCutPlate_wDir)

        self.weldCutPlateModel = self.weldCutPlate.create_model()

    def get_column_models(self):
        """

        :return: CAD mode for the columns
        """
        columns = BRepAlgoAPI_Fuse(self.column1Model, self.column2Model).Shape()

        return columns

    def get_plate_models(self):
        """
        :return: CAD model for all the plates
        """


        if self.C.preference != 'Outside':
            plates_sec = [self.flangePlate1Model, self.flangePlate2Model, self.innerFlangePlate1Model,
                          self.innerFlangePlate2Model, self.innerFlangePlate3Model, self.innerFlangePlate4Model,
                          self.webPlate1Model, self.webPlate2Model]
        else:
            plates_sec = [self.flangePlate1Model, self.flangePlate2Model,
                          self.webPlate1Model, self.webPlate2Model]

        plates = plates_sec[0]

        for comp in plates_sec[1:]:
            plates = BRepAlgoAPI_Fuse(comp, plates).Shape()

        return plates

    def get_welded_modules(self):
        """
        :return: CAD model for all the welds
        """
        if self.C.preference != 'Outside':
            welded_sec = [self.flangePlateWeldL11Model, self.flangePlateWeldL12Model, self.flangePlateWeldL21Model,
                          self.flangePlateWeldL22Model, self.flangePlateWeldW11Model, self.flangePlateWeldW12Model,
                          self.flangePlateWeldW21Model, self.flangePlateWeldW22Model, \
                          self.webPlateWeldL11Model, self.webPlateWeldL12Model, self.webPlateWeldL21Model,
                          self.webPlateWeldL22Model, self.webPlateWeldW11Model, self.webPlateWeldW12Model,
                          self.webPlateWeldW21Model, self.webPlateWeldW22Model, \
                          self.innerflangePlateWeldL11Model, self.innerflangePlateWeldL12Model,
                          self.innerflangePlateWeldL21Model, self.innerflangePlateWeldL22Model,
                          self.innerflangePlateWeldL31Model, self.innerflangePlateWeldL32Model,
                          self.innerflangePlateWeldL41Model, self.innerflangePlateWeldL42Model, \
                          self.innerflangePlateWeldW11Model, self.innerflangePlateWeldW12Model,
                          self.innerflangePlateWeldW21Model, self.innerflangePlateWeldW22Model,
                          self.innerflangePlateWeldW31Model, self.innerflangePlateWeldW32Model,
                          self.innerflangePlateWeldW41Model, self.innerflangePlateWeldW42Model]
        else:
            welded_sec = [self.flangePlateWeldL11Model, self.flangePlateWeldL12Model, self.flangePlateWeldL21Model,
                          self.flangePlateWeldL22Model, self.flangePlateWeldW11Model, self.flangePlateWeldW12Model,
                          self.flangePlateWeldW21Model, self.flangePlateWeldW22Model, \
                          self.webPlateWeldL11Model, self.webPlateWeldL12Model, self.webPlateWeldL21Model,
                          self.webPlateWeldL22Model, self.webPlateWeldW11Model, self.webPlateWeldW12Model,
                          self.webPlateWeldW21Model, self.webPlateWeldW22Model]

        welds = welded_sec[0]

        for comp in welded_sec[1:]:
            welds = BRepAlgoAPI_Fuse(comp, welds).Shape()

        welds = BRepAlgoAPI_Cut(welds, self.weldCutPlateModel).Shape()

        return welds
        # return self.innerflangePlateWeldW42Model

    def get_models(self):
        columns = self.get_column_models()
        plate_conectors = self.get_plate_models()
        welds = self.get_welded_modules()

        CAD = BRepAlgoAPI_Fuse(columns, plate_conectors).Shape()
        CAD = BRepAlgoAPI_Fuse(CAD, welds).Shape()

        return CAD

if __name__ == '__main__':
    from cad.items.ISection import ISection
    from cad.items.plate import Plate
    from cad.items.filletweld import FilletWeld

    import OCC.Core.V3d

    from OCC.gp import gp_Pnt
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    column = ISection(B=250, T=13.5, D=450, t=9.8, R1=15, R2=75, alpha=94, length=1000, notchObj=None)
    flangePlate = Plate(L=550, W=210, T=14)
    innerFlangePlate = Plate(L=550, W=80, T=14)
    webPlate = Plate(L=365, W=170, T=8)
    gap = 10

    flangePlateWeldL = FilletWeld(h=5, b=5, L=flangePlate.L)
    flangePlateWeldW = FilletWeld(h=5, b=5, L=flangePlate.W)

    innerflangePlateWeldL = FilletWeld(h=5, b=5, L=innerFlangePlate.L)
    innerflangePlateWeldW = FilletWeld(h=5, b=5, L=innerFlangePlate.W)

    webPlateWeldL = FilletWeld(h=5, b=5, L=webPlate.L)
    webPlateWeldW = FilletWeld(h=5, b=5, L=webPlate.W)

    CCSpliceCoverPlateCAD = CCSpliceCoverPlateWeldedCAD(column, flangePlate, innerFlangePlate, webPlate, gap,
                                                        flangePlateWeldL, flangePlateWeldW, innerflangePlateWeldL,
                                                        innerflangePlateWeldW, webPlateWeldL, webPlateWeldW)

    CCSpliceCoverPlateCAD.create_3DModel()
    column = CCSpliceCoverPlateCAD.get_column_models()
    plates = CCSpliceCoverPlateCAD.get_plate_models()
    welds = CCSpliceCoverPlateCAD.get_welded_modules()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    # display.View.Rotate(45, 90, 45)
    display.DisplayShape(column, update=True)
    display.DisplayShape(plates, color='BLUE', update=True)
    display.DisplayShape(welds, color='RED', update=True)

    display.DisableAntiAliasing()
    start_display()
