"""
created on 14-04-2020

"""

import numpy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
import copy

class CCSpliceCoverPlateBoltedCAD(object):
    def __init__(self, C, column, flangePlate, innerFlangePlate, webPlate,  nut_bolt_array_AF, nut_bolt_array_BF, nut_bolt_array_Web):

        self.C = C
        self.column = column
        self.flangePlate = flangePlate
        self.innerFlangePlate = innerFlangePlate
        self.webPlate = webPlate
        self.nut_bolt_array_AF = nut_bolt_array_AF
        self.nut_bolt_array_BF = nut_bolt_array_BF
        self.nut_bolt_array_Web = nut_bolt_array_Web

        self.gap = float(self.C.flange_plate.gap)


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

    def create_3DModel(self):
        '''
        :return:  CAD model of each of the followings. Debugging each command below would give give clear picture
        '''

        self.createColumnGeometry()
        self.createPlateGeometry()
        self.create_nut_bolt_array()

    def createColumnGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        column1Origin = numpy.array([0.0, 0.0, self.gap/2])
        column1_uDir = numpy.array([1.0, 0.0, 0.0])
        column1_wDir = numpy.array([0.0, 0.0, 1.0])
        self.column1.place(column1Origin, column1_uDir, column1_wDir)

        self.column1Model = self.column1.create_model()

        column2Origin = numpy.array([0.0, 0.0, -self.gap/2])
        column2_uDir = numpy.array([1.0, 0.0, 0.0])
        column2_wDir = numpy.array([0.0, 0.0, -1.0])
        self.column2.place(column2Origin, column2_uDir, column2_wDir)

        self.column2Model = self.column2.create_model()

    def createPlateGeometry(self):
        flangePlate1Origin = numpy.array([-self.flangePlate.W/2, (self.column.D + self.flangePlate.T)/2, 0.0])
        flangePlate1_uDir = numpy.array([0.0, 1.0, 0.0])
        flangePlate1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.flangePlate1.place(flangePlate1Origin, flangePlate1_uDir, flangePlate1_wDir)

        self.flangePlate1Model = self.flangePlate1.create_model()

        flangePlate2Origin = numpy.array([-self.flangePlate.W/2, -(self.column.D + self.flangePlate.T)/2, 0.0])
        flangePlate2_uDir = numpy.array([0.0, 1.0, 0.0])
        flangePlate2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.flangePlate2.place(flangePlate2Origin, flangePlate2_uDir, flangePlate2_wDir)

        self.flangePlate2Model = self.flangePlate2.create_model()

        webPlate1Origin = numpy.array([(self.column.t + self.webPlate.T)/2, -self.webPlate.W/2, 0.0])
        webPlate1_uDir = numpy.array([1.0, 0.0, 0.0])
        webPlate1_wDir = numpy.array([0.0, 1.0, 0.0])
        self.webPlate1.place(webPlate1Origin, webPlate1_uDir, webPlate1_wDir)

        self.webPlate1Model = self.webPlate1.create_model()

        webPlate2Origin = numpy.array([-(self.column.t + self.webPlate.T)/2, -self.webPlate.W/2, 0.0])
        webPlate2_uDir = numpy.array([1.0, 0.0, 0.0])
        webPlate2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.webPlate2.place(webPlate2Origin, webPlate2_uDir, webPlate2_wDir)

        self.webPlate2Model = self.webPlate2.create_model()

        if self.C.preference != 'Outside':
            innerFlangePlatespacing = self.column.B/2 - self.innerFlangePlate.W
            innerFlangePlate1Origin = numpy.array([innerFlangePlatespacing,  (self.column.D - self.innerFlangePlate.T)/2 - self.column.T, 0.0])
            innerFlangePlate1_uDir = numpy.array([0.0, 1.0, 0.0])
            innerFlangePlate1_wDir = numpy.array([1.0, 0.0, 0.0])
            self.innerFlangePlate1.place(innerFlangePlate1Origin, innerFlangePlate1_uDir, innerFlangePlate1_wDir)

            self.innerFlangePlate1Model = self.innerFlangePlate1.create_model()

            innerFlangePlate2Origin = numpy.array([innerFlangePlatespacing, -(self.column.D - self.innerFlangePlate.T)/2 + self.column.T, 0.0])
            innerFlangePlate2_uDir = numpy.array([0.0, 1.0, 0.0])
            innerFlangePlate2_wDir = numpy.array([1.0, 0.0, 0.0])
            self.innerFlangePlate2.place(innerFlangePlate2Origin, innerFlangePlate2_uDir, innerFlangePlate2_wDir)

            self.innerFlangePlate2Model = self.innerFlangePlate2.create_model()

            innerFlangePlate3Origin = numpy.array([-innerFlangePlatespacing, -(self.column.D --- self.innerFlangePlate.T)/2 + self.column.T, 0.0])
            innerFlangePlate3_uDir = numpy.array([0.0, 1.0, 0.0])
            innerFlangePlate3_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.innerFlangePlate3.place(innerFlangePlate3Origin, innerFlangePlate3_uDir, innerFlangePlate3_wDir)

            self.innerFlangePlate3Model = self.innerFlangePlate3.create_model()

            innerFlangePlate4Origin = numpy.array([-innerFlangePlatespacing, (self.column.D - self.innerFlangePlate.T)/2 - self.column.T, 0.0])
            innerFlangePlate4_uDir = numpy.array([0.0, 1.0, 0.0])
            innerFlangePlate4_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.innerFlangePlate4.place(innerFlangePlate4Origin, innerFlangePlate4_uDir, innerFlangePlate4_wDir)

            self.innerFlangePlate4Model = self.innerFlangePlate4.create_model()


    def create_nut_bolt_array(self):

        nutBoltOriginAF = self.flangePlate1.sec_origin + numpy.array([0.0,  self.flangePlate.T/2, -self.flangePlate.L/2])

        gaugeDirAF = numpy.array([1.0, 0, 0])
        pitchDirAF = numpy.array([0, 0.0, 1.0])
        boltDirAF = numpy.array([0, -1.0, 0.0])
        width = self.column.B
        self.nut_bolt_array_AF.placeAF(nutBoltOriginAF, gaugeDirAF, pitchDirAF, boltDirAF, width)
        self.nut_bolt_array_AF.create_modelAF()

        nutBoltOriginBF = self.flangePlate2.sec_origin + numpy.array([0.0, -self.flangePlate.T/2, -self.flangePlate.L/2])

        gaugeDirBF = numpy.array([1.0, 0, 0])
        pitchDirBF = numpy.array([0, 0.0, 1.0])
        boltDirBF = numpy.array([0, 1.0, 0.0])
        width = self.column.B
        self.nut_bolt_array_BF.placeBF(nutBoltOriginBF, gaugeDirBF, pitchDirBF, boltDirBF, width)
        self.nut_bolt_array_BF.create_modelBF()

        boltWeb_X = self.webPlate.T / 2
        boltWeb_Y = self.webPlate.W
        nutBoltOriginW = self.webPlate1.sec_origin + numpy.array([boltWeb_X, boltWeb_Y, -self.webPlate.L/2])
        gaugeDirW = numpy.array([0, 0.0, 1.0])
        pitchDirW = numpy.array([0, -1.0, .0])
        boltDirW = numpy.array([-1.0, 0, 0])
        self.nut_bolt_array_Web.placeW(nutBoltOriginW, gaugeDirW, pitchDirW, boltDirW)
        self.nut_bolt_array_Web.create_modelW()

        return nutBoltOriginAF


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

    def get_nut_bolt_models(self):
        """
            :return: CAD model for all nut_bolt_arrangments
        """
        nut_bolts_AF = self.nut_bolt_array_AF.get_modelsAF()
        array_AF = nut_bolts_AF[0]
        for comp in nut_bolts_AF:
            array_AF = BRepAlgoAPI_Fuse(comp, array_AF).Shape()

        nut_bolts_BF = self.nut_bolt_array_BF.get_modelsBF()
        array_BF = nut_bolts_BF[0]
        for comp in nut_bolts_BF:
            array_BF = BRepAlgoAPI_Fuse(comp, array_BF).Shape()

        nut_bolts_W = self.nut_bolt_array_Web.get_modelsW()
        array_W = nut_bolts_W[0]
        for comp in nut_bolts_W:
            array_W = BRepAlgoAPI_Fuse(comp, array_W).Shape()

        nut_bolts_array = BRepAlgoAPI_Fuse(array_AF, array_BF).Shape()
        nut_bolts_array = BRepAlgoAPI_Fuse(nut_bolts_array, array_W).Shape()

        return nut_bolts_array

    def get_only_column_models(self):
        columns = self.get_column_models()
        nutbolt = self.get_nut_bolt_models()

        onlycolumn = BRepAlgoAPI_Cut(columns, nutbolt).Shape()

        return onlycolumn

    def get_models(self):
        columns = self.get_column_models()
        plate_conectors = self.get_plate_models()

        CAD = BRepAlgoAPI_Fuse(columns, plate_conectors).Shape()

        return CAD

if __name__ == '__main__':
    from cad.items.ISection import ISection
    from cad.items.plate import Plate
    from cad.items.bolt import Bolt
    from cad.items.nut import Nut
    from cad.MomentConnections.CCSpliceCoverPlateCAD.nutBoltPlacement_AF import NutBoltArray_AF
    from cad.MomentConnections.CCSpliceCoverPlateCAD.nutBoltPlacement_BF import NutBoltArray_BF
    from cad.MomentConnections.CCSpliceCoverPlateCAD.nutBoltPlacement_Web import NutBoltArray_Web
    import numpy

    import OCC.Core.V3d

    from OCC.gp import gp_Pnt
    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    column = ISection(B= 206.4, T= 17.3, D= 215.8, t= 10, R1= 15, R2= 75, alpha= 94, length= 1000, notchObj= None)
    flangePlate = Plate(L= 240, W= 203.6, T= 10)
    innerFlangePlate = Plate(L= 240, W= 85, T= 10)
    webPlate = Plate(L= 600, W= 120, T= 8)
    gap = 10

    bolt = Bolt(R=12, T=5, H=6, r=6)
    nut = Nut(R=bolt.R, T=bolt.T, H=bolt.T + 1, innerR1=bolt.r)
    nut_space = 2*flangePlate.T + column.T
    Obj = '6'
    numOfboltsF = 24
    plateAbvFlangeL = 100

    nut_bolt_array_AF = NutBoltArray_AF(Obj, nut, bolt, numOfboltsF, nut_space)
    nut_bolt_array_BF = NutBoltArray_BF(Obj, nut, bolt, numOfboltsF, nut_space)
    numOfboltsF = 24
    nut_space = 2 * webPlate.T + column.t
    nut_bolt_array_Web = NutBoltArray_Web(Obj, nut, bolt, numOfboltsF, nut_space)

    CCSpliceCoverPlateCAD = CCSpliceCoverPlateBoltedCAD(column, flangePlate, innerFlangePlate, webPlate, gap, nut_bolt_array_AF, nut_bolt_array_BF, nut_bolt_array_Web)

    CCSpliceCoverPlateCAD.create_3DModel()
    column = CCSpliceCoverPlateCAD.get_column_models()
    plates = CCSpliceCoverPlateCAD.get_plate_models()
    nut_bolt_array = CCSpliceCoverPlateCAD.get_nut_bolt_models()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")


    # display.View.Rotate(45, 90, 45)
    display.DisplayShape(column, update=True)
    display.DisplayColoredShape(plates, color='BLUE', update=True)
    display.DisplayShape(nut_bolt_array, color='YELLOW', update=True)

    display.DisableAntiAliasing()
    start_display()