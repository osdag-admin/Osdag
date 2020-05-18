"""
created on 14-04-2020

"""

import numpy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
import copy

class CCEndPlateCAD(object):
    def __init__(self,column, endPlate):
        self.endPlate = endPlate
        self.column = column



        self.column1 = copy.deepcopy(self.column)
        self.column2 = copy.deepcopy(self.column)

        self.endPlate1 = copy.deepcopy(self.endPlate)
        self.endPlate2 = copy.deepcopy(self.endPlate)


    def create_3DModel(self):
        '''
        :return:  CAD model of each of the followings. Debugging each command below would give give clear picture
        '''

        self.createColumnGeometry()
        self.createPlateGeometry()

        self.column1Model = self.column1.create_model()
        self.column2Model = self.column2.create_model()

        self.endPlate1Model = self.endPlate1.create_model()
        self.endPlate2Model = self.endPlate2.create_model()



    def createColumnGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        column1Origin = numpy.array([0.0, 0.0, self.endPlate.T])
        column1_uDir = numpy.array([1.0, 0.0, 0.0])
        column1_wDir = numpy.array([0.0, 0.0, 1.0])
        self.column1.place(column1Origin, column1_uDir, column1_wDir)

        column2Origin = numpy.array([0.0, 0.0, -self.endPlate.T])
        column2_uDir = numpy.array([1.0, 0.0, 0.0])
        column2_wDir = numpy.array([0.0, 0.0, -1.0])
        self.column2.place(column2Origin, column2_uDir, column2_wDir)


    def createPlateGeometry(self):
        endPlate1Origin = numpy.array([-self.endPlate.W/2, 0.0, self.endPlate.T/2])
        endPlate1_uDir = numpy.array([0.0, 0.0, 1.0])
        endPlate1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.endPlate1.place(endPlate1Origin, endPlate1_uDir, endPlate1_wDir)

        endPlate2Origin = numpy.array([-self.endPlate.W/2, 0.0, -self.endPlate.T/2])
        endPlate2_uDir = numpy.array([0.0, 0.0, 1.0])
        endPlate2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.endPlate2.place(endPlate2Origin, endPlate2_uDir, endPlate2_wDir)



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

    column = ISection(B= 250, T= 10.6,D= 300, t= 7.6, R1= 11, R2= 5.5, alpha= 94, length= 1000, notchObj= None)
    endPlate = Plate(L= 300, W= 250, T= 28)

    CCEndPlate = CCEndPlateCAD(column, endPlate)

    CCEndPlate.create_3DModel()
    column = CCEndPlate.get_column_models()
    plates = CCEndPlate.get_plate_models()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    # display.View.Rotate(45, 90, 45)
    display.DisplayShape(column, update=True)
    display.DisplayColoredShape(plates, color='BLUE', update=True)

    display.DisableAntiAliasing()
    start_display()