"""
created on 14-04-2020

"""

import numpy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
import copy


class CCEndPlateCAD(object):
    def __init__(self, Obj, column, endPlate, flangeWeld, webWeld, nut_bolt_array):
        self.Obj = Obj
        self.endPlate = endPlate
        self.column = column
        self.flangeWeld = flangeWeld
        self.webWeld = webWeld
        self.nut_bolt_array = nut_bolt_array

        self.column1 = copy.deepcopy(self.column)
        self.column2 = copy.deepcopy(self.column)

        self.endPlate1 = copy.deepcopy(self.endPlate)
        self.endPlate2 = copy.deepcopy(self.endPlate)

        self.flangeWeldT1 = copy.deepcopy(self.flangeWeld)
        self.flangeWeldT2 = copy.deepcopy(self.flangeWeld)
        self.flangeWeldB1 = copy.deepcopy(self.flangeWeld)
        self.flangeWeldB2 = copy.deepcopy(self.flangeWeld)

        self.webWeldT1 = copy.deepcopy(self.webWeld)
        self.webWeldB1 = copy.deepcopy(self.webWeld)

    def create_3DModel(self):
        '''
        :return:  CAD model of each of the followings. Debugging each command below would give give clear picture
        '''

        self.createColumnGeometry()
        self.createPlateGeometry()
        self.createNutBoltArray()
        self.createWeldGeometry()

    def createColumnGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        column1Origin = numpy.array([0.0, 0.0, self.endPlate.T + self.webWeld.h])
        column1_uDir = numpy.array([1.0, 0.0, 0.0])
        column1_wDir = numpy.array([0.0, 0.0, 1.0])
        self.column1.place(column1Origin, column1_uDir, column1_wDir)

        self.column1Model = self.column1.create_model()

        column2Origin = numpy.array([0.0, 0.0, -(self.endPlate.T + self.webWeld.h)])
        column2_uDir = numpy.array([1.0, 0.0, 0.0])
        column2_wDir = numpy.array([0.0, 0.0, -1.0])
        self.column2.place(column2Origin, column2_uDir, column2_wDir)

        self.column2Model = self.column2.create_model()

    def createPlateGeometry(self):
        endPlate1Origin = numpy.array([-self.endPlate.W / 2, 0.0, self.endPlate.T / 2])
        endPlate1_uDir = numpy.array([0.0, 0.0, 1.0])
        endPlate1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.endPlate1.place(endPlate1Origin, endPlate1_uDir, endPlate1_wDir)

        self.endPlate1Model = self.endPlate1.create_model()

        endPlate2Origin = numpy.array([-self.endPlate.W / 2, 0.0, -self.endPlate.T / 2])
        endPlate2_uDir = numpy.array([0.0, 0.0, 1.0])
        endPlate2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.endPlate2.place(endPlate2Origin, endPlate2_uDir, endPlate2_wDir)

        self.endPlate2Model = self.endPlate2.create_model()

    def createNutBoltArray(self):
        nut_bolt_arrayOrigin = numpy.array([-self.endPlate.W / 2, -self.endPlate.L / 2, -self.endPlate.T])
        gaugeDir = numpy.array([0.0, 1.0, 0])
        pitchDir = numpy.array([1.0, 0.0, 0])
        boltDir = numpy.array([0, 0, 1.0])
        self.nut_bolt_array.place(nut_bolt_arrayOrigin, pitchDir, gaugeDir, boltDir)

        self.nut_bolt_arrayModel = self.nut_bolt_array.create_model()

    def createWeldGeometry(self):
        flangeWeldT1Origin = numpy.array([-self.flangeWeld.L / 2, -self.column.D / 2 + self.flangeWeld.b / 2,
                                          self.endPlate.T + self.flangeWeld.h / 2])
        flangeWeldT1_uDir = numpy.array([0.0, 1.0, 0.0])
        flangeWeldT1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.flangeWeldT1.place(flangeWeldT1Origin, flangeWeldT1_uDir, flangeWeldT1_wDir)

        self.flangeWeldT1Model = self.flangeWeldT1.create_model()

        flangeWeldT2Origin = numpy.array([-self.flangeWeld.L / 2, -(-self.column.D / 2 + self.flangeWeld.b / 2),
                                          (self.endPlate.T + self.flangeWeld.h / 2)])
        flangeWeldT2_uDir = numpy.array([0.0, 1.0, 0.0])
        flangeWeldT2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.flangeWeldT2.place(flangeWeldT2Origin, flangeWeldT2_uDir, flangeWeldT2_wDir)

        self.flangeWeldT2Model = self.flangeWeldT2.create_model()

        flangeWeldB1Origin = numpy.array([-self.flangeWeld.L / 2, (-self.column.D / 2 + self.flangeWeld.b / 2),
                                          -(self.endPlate.T + self.flangeWeld.h / 2)])
        flangeWeldB1_uDir = numpy.array([0.0, 1.0, 0.0])
        flangeWeldB1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.flangeWeldB1.place(flangeWeldB1Origin, flangeWeldB1_uDir, flangeWeldB1_wDir)

        self.flangeWeldB1Model = self.flangeWeldB1.create_model()

        flangeWeldB2Origin = numpy.array([-self.flangeWeld.L / 2, -(-self.column.D / 2 + self.flangeWeld.b / 2),
                                          -(self.endPlate.T + self.flangeWeld.h / 2)])
        flangeWeldB2_uDir = numpy.array([0.0, 1.0, 0.0])
        flangeWeldB2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.flangeWeldB2.place(flangeWeldB2Origin, flangeWeldB2_uDir, flangeWeldB2_wDir)

        self.flangeWeldB2Model = self.flangeWeldB2.create_model()

        webWeldT1Origin = numpy.array([00, -self.webWeld.L / 2, (self.endPlate.T + self.flangeWeld.h / 2)])
        webWeldT1_uDir = numpy.array([1.0, 0.0, 0.0])
        webWeldT1_wDir = numpy.array([0.0, 1.0, 0.0])
        self.webWeldT1.place(webWeldT1Origin, webWeldT1_uDir, webWeldT1_wDir)

        self.webWeldT1Model = self.webWeldT1.create_model()

        webWeldB1Origin = numpy.array([0.0, -self.webWeld.L / 2, -(self.endPlate.T + self.flangeWeld.h / 2)])
        webWeldB1_uDir = numpy.array([1.0, 0.0, 0.0])
        webWeldB1_wDir = numpy.array([0.0, 1.0, 0.0])
        self.webWeldB1.place(webWeldB1Origin, webWeldB1_uDir, webWeldB1_wDir)

        self.webWeldB1Model = self.webWeldB1.create_model()

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
        # plates_sec = [self.endPlate1Model, self.endPlate2Model]

        # plates = plates_sec[0]
        #
        # for comp in plates_sec[1:]:
        #     plates = BRepAlgoAPI_Fuse(comp, plates).Shape()

        plates = BRepAlgoAPI_Fuse(self.endPlate1Model, self.endPlate2Model).Shape()

        return plates

    def get_nut_bolt_models(self):
        """
        :return: CAD model for all the nut bolt arrangement
        """
        return self.nut_bolt_arrayModel

    def get_weld_models(self):
        """
        :return: CAD model for all the welds
        """
        welded_sec = [self.flangeWeldT1Model, self.flangeWeldT2Model, self.flangeWeldB1Model, self.flangeWeldB2Model,
                      self.webWeldT1Model, self.webWeldB1Model]
        welds = welded_sec[0]
        for comp in welded_sec[1:]:
            welds = BRepAlgoAPI_Fuse(comp, welds).Shape()
        return welds

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
    from cad.items.filletweld import FilletWeld
    from cad.items.groove_weld import GrooveWeld
    from cad.MomentConnections.CCEndPlateCAD.nutBoltPlacement import NutBoltArray

    import OCC.Core.V3d

    from OCC.gp import gp_Pnt
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    column = ISection(B=250, T=12.7, D=400, t=9.1, R1=11, R2=5.5, alpha=94, length=1000, notchObj=None)
    endPlate = Plate(L=column.D, W=column.B, T=45)
    flangeWeld = GrooveWeld(b=column.T, h=20, L=column.B)
    webWeld = GrooveWeld(b=column.t, h=20, L=column.D - 2 * column.T)

    bolt = Bolt(R=14, T=10, H=13, r=8)
    nut = Nut(R=bolt.R, T=bolt.T, H=bolt.T + 1, innerR1=bolt.r)
    nut_space = 2 * endPlate.T + nut.T  # member.T + plate.T + nut.T
    Obj = '6'

    nut_bolt_array = NutBoltArray(Obj, nut, bolt, nut_space)

    CCEndPlate = CCEndPlateCAD(column, endPlate, flangeWeld, webWeld, nut_bolt_array)

    CCEndPlate.create_3DModel()
    column = CCEndPlate.get_column_models()
    plates = CCEndPlate.get_plate_models()
    welds = CCEndPlate.get_weld_models()
    nutBolts = CCEndPlate.get_nut_bolt_models()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    # display.View.Rotate(45, 90, 45)
    display.DisplayShape(column, update=True)
    display.DisplayColoredShape(plates, color='BLUE', update=True)
    display.DisplayShape(welds, color='RED', update=True)
    display.DisplayShape(nutBolts, color='YELLOW', update=True)

    display.DisableAntiAliasing()
    start_display()
