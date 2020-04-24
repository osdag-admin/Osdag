"""
created on 14-04-2020

"""

import numpy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
import copy

class CCSpliceCoverPlateWeldedCAD(object):
    def __init__(self,column, flangePlate, innerFlangePlate, webPlate, gap):
        self.column = column
        self.flangePlate = flangePlate
        self.innerFlangePlate = innerFlangePlate
        self.webPlate = webPlate
        self.gap = gap

        self.flangespace = 15
        self.webspace = 15

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

        self.column1Model = self.column1.create_model()
        self.column2Model = self.column2.create_model()

        self.flangePlate1Model = self.flangePlate1.create_model()
        self.flangePlate2Model = self.flangePlate2.create_model()

        self.innerFlangePlate1Model = self.innerFlangePlate1.create_model()
        self.innerFlangePlate2Model = self.innerFlangePlate2.create_model()
        self.innerFlangePlate3Model = self.innerFlangePlate3.create_model()
        self.innerFlangePlate4Model = self.innerFlangePlate4.create_model()

        self.webPlate1Model = self.webPlate1.create_model()
        self.webPlate2Model = self.webPlate2.create_model()

    def createColumnGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        column1Origin = numpy.array([0.0, 0.0, self.gap/2])
        column1_uDir = numpy.array([1.0, 0.0, 0.0])
        column1_wDir = numpy.array([0.0, 0.0, 1.0])
        self.column1.place(column1Origin, column1_uDir, column1_wDir)

        column2Origin = numpy.array([0.0, 0.0, -self.gap/2])
        column2_uDir = numpy.array([1.0, 0.0, 0.0])
        column2_wDir = numpy.array([0.0, 0.0, -1.0])
        self.column2.place(column2Origin, column2_uDir, column2_wDir)


    def createPlateGeometry(self):
        flangePlate1Origin = numpy.array([-self.flangePlate.W/2, (self.column.D + self.flangePlate.T)/2, 0.0])
        flangePlate1_uDir = numpy.array([0.0, 1.0, 0.0])
        flangePlate1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.flangePlate1.place(flangePlate1Origin, flangePlate1_uDir, flangePlate1_wDir)

        flangePlate2Origin = numpy.array([-self.flangePlate.W/2, -(self.column.D + self.flangePlate.T)/2, 0.0])
        flangePlate2_uDir = numpy.array([0.0, 1.0, 0.0])
        flangePlate2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.flangePlate2.place(flangePlate2Origin, flangePlate2_uDir, flangePlate2_wDir)

        innerFlangePlatespacing = self.flangespace + self.column.t/2 + self.column.R1
        innerFlangePlate1Origin = numpy.array([innerFlangePlatespacing,  (self.column.D - self.innerFlangePlate.T)/2 - self.column.T, 0.0])
        innerFlangePlate1_uDir = numpy.array([0.0, 1.0, 0.0])
        innerFlangePlate1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.innerFlangePlate1.place(innerFlangePlate1Origin, innerFlangePlate1_uDir, innerFlangePlate1_wDir)

        innerFlangePlate2Origin = numpy.array([innerFlangePlatespacing, -(self.column.D - self.innerFlangePlate.T)/2 + self.column.T, 0.0])
        innerFlangePlate2_uDir = numpy.array([0.0, 1.0, 0.0])
        innerFlangePlate2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.innerFlangePlate2.place(innerFlangePlate2Origin, innerFlangePlate2_uDir, innerFlangePlate2_wDir)

        innerFlangePlate3Origin = numpy.array([-innerFlangePlatespacing, -(self.column.D --- self.innerFlangePlate.T)/2 + self.column.T, 0.0])
        innerFlangePlate3_uDir = numpy.array([0.0, 1.0, 0.0])
        innerFlangePlate3_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.innerFlangePlate3.place(innerFlangePlate3Origin, innerFlangePlate3_uDir, innerFlangePlate3_wDir)

        innerFlangePlate4Origin = numpy.array([-innerFlangePlatespacing, (self.column.D - self.innerFlangePlate.T)/2 - self.column.T, 0.0])
        innerFlangePlate4_uDir = numpy.array([0.0, 1.0, 0.0])
        innerFlangePlate4_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.innerFlangePlate4.place(innerFlangePlate4Origin, innerFlangePlate4_uDir, innerFlangePlate4_wDir)

        webPlate1Origin = numpy.array([(self.column.t + self.webPlate.T)/2, -self.webPlate.W/2, 0.0])
        webPlate1_uDir = numpy.array([1.0, 0.0, 0.0])
        webPlate1_wDir = numpy.array([0.0, 1.0, 0.0])
        self.webPlate1.place(webPlate1Origin, webPlate1_uDir, webPlate1_wDir)

        webPlate2Origin = numpy.array([-(self.column.t + self.webPlate.T)/2, -self.webPlate.W/2, 0.0])
        webPlate2_uDir = numpy.array([1.0, 0.0, 0.0])
        webPlate2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.webPlate2.place(webPlate2Origin, webPlate2_uDir, webPlate2_wDir)

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
        plates_sec = [self.flangePlate1Model, self.flangePlate2Model, self.innerFlangePlate1Model, self.innerFlangePlate2Model, self.innerFlangePlate3Model, self.innerFlangePlate4Model, self.webPlate1Model, self.webPlate2Model]

        plates = plates_sec[0]

        for comp in plates_sec[1:]:
            plates = BRepAlgoAPI_Fuse(comp, plates).Shape()

        return plates

    def get_models(self):
        columns = self.get_column_models()
        plate_conectors = self.get_plate_models()

        CAD = BRepAlgoAPI_Fuse(columns, plate_conectors).Shape()

        return CAD

if __name__ == '__main__':
    from cad.items.ISection import ISection
    from cad.items.plate import Plate
    from cad.items.filletweld import FilletWeld

    import OCC.Core.V3d

    from OCC.gp import gp_Pnt
    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    column = ISection(B= 250, T= 13.5,D= 450, t= 9.8, R1= 15, R2= 75, alpha= 94, length= 1000, notchObj= None)
    flangePlate = Plate(L= 550, W= 210, T= 14)
    innerFlangePlate = Plate(L= 550, W= 80, T= 14)
    webPlate = Plate(L= 365, W= 170, T= 8)
    gap = 10

    CCSpliceCoverPlateCAD = CCSpliceCoverPlateWeldedCAD(column, flangePlate, innerFlangePlate, webPlate, gap)

    CCSpliceCoverPlateCAD.create_3DModel()
    column = CCSpliceCoverPlateCAD.get_column_models()
    plates = CCSpliceCoverPlateCAD.get_plate_models()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    # display.View.Rotate(45, 90, 45)
    display.DisplayShape(column, update=True)
    display.DisplayColoredShape(plates, color='BLUE', update=True)

    display.DisableAntiAliasing()
    start_display()