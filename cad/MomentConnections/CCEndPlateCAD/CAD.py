"""
created on 14-04-2020

"""

import numpy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
import copy


class CCEndPlateCAD(object):
    def __init__(self, column, endPlate, flangeWeld, webWeld):
        self.endPlate = endPlate
        self.column = column
        self.flangeWeld = flangeWeld
        self.webWeld = webWeld

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

    def createWeldGeometry(self):
        flangeWeldT1Origin = numpy.array(
            [-self.endPlate.W / 2, -self.column.D / 2 + self.flangeWeld.b / 2, self.endPlate.T + self.flangeWeld.h / 2])
        flangeWeldT1_uDir = numpy.array([0.0, 1.0, 0.0])
        flangeWeldT1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.flangeWeldT1.place(flangeWeldT1Origin, flangeWeldT1_uDir, flangeWeldT1_wDir)

        self.flangeWeldT1Model = self.flangeWeldT1.create_model()

        flangeWeldT2Origin = numpy.array([-self.endPlate.W / 2, -(-self.column.D / 2 + self.flangeWeld.b / 2),
                                          (self.endPlate.T + self.flangeWeld.h / 2)])
        flangeWeldT2_uDir = numpy.array([0.0, 1.0, 0.0])
        flangeWeldT2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.flangeWeldT2.place(flangeWeldT2Origin, flangeWeldT2_uDir, flangeWeldT2_wDir)

        self.flangeWeldT2Model = self.flangeWeldT2.create_model()

        flangeWeldB1Origin = numpy.array([-self.endPlate.W / 2, (-self.column.D / 2 + self.flangeWeld.b / 2),
                                          -(self.endPlate.T + self.flangeWeld.h / 2)])
        flangeWeldB1_uDir = numpy.array([0.0, 1.0, 0.0])
        flangeWeldB1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.flangeWeldB1.place(flangeWeldB1Origin, flangeWeldB1_uDir, flangeWeldB1_wDir)

        self.flangeWeldB1Model = self.flangeWeldB1.create_model()

        flangeWeldB2Origin = numpy.array([-self.endPlate.W / 2, -(-self.column.D / 2 + self.flangeWeld.b / 2),
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
    from cad.items.filletweld import FilletWeld
    from cad.items.groove_weld import GrooveWeld

    import OCC.Core.V3d

    from OCC.gp import gp_Pnt
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    column = ISection(B=250, T=10.6, D=300, t=7.6, R1=11, R2=5.5, alpha=94, length=1000, notchObj=None)
    endPlate = Plate(L=300, W=250, T=28)
    flangeWeld = GrooveWeld(b=column.T, h=20, L=column.B)
    webWeld = GrooveWeld(b=column.t, h=20, L=column.D - 2 * column.T)

    CCEndPlate = CCEndPlateCAD(column, endPlate, flangeWeld, webWeld)

    CCEndPlate.create_3DModel()
    column = CCEndPlate.get_column_models()
    plates = CCEndPlate.get_plate_models()
    welds = CCEndPlate.get_weld_models()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    # display.View.Rotate(45, 90, 45)
    display.DisplayShape(column, update=True)
    display.DisplayColoredShape(plates, color='BLUE', update=True)
    display.DisplayShape(welds, color='RED', update=True)

    display.DisableAntiAliasing()
    start_display()
