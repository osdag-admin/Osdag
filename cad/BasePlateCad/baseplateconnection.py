"""
created on 09-03-2020

@author: Anand Swaroop

This file is for creating CAD model for cover baseplate bolted moment connection for connectivity Beam-Beam

"""

import numpy
import copy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse

class BasePlateCad(object):
    def __init__(self, column, basebaseplate, weldAbvFlang, weldBelwFlang, weldSideWeb, nut_bolt_array, alist ):

        """

        :param column: column
        :param basebaseplate:  basebaseplate
        :param weldAbvFlang: Weld surface on the outer side of flange
        :param weldBelwFlang: Weld surface on the inner side of flange
        :param weldSideWeb: Weld surface on the sides of the web
        :param nut_bolt_array:  Bolt placement on the end baseplates
        :param alist: input and output values
        """

        self.column = column
        self.baseplate = basebaseplate
        self.weldAbvFlang = weldAbvFlang
        self.weldBelwFlang = weldBelwFlang
        self.weldSideWeb = weldSideWeb
        self.nut_bolt_array = nut_bolt_array
        self.alist = alist




        # Weld above flange for left and right column
        self.weldAbvFlang_11 = copy.deepcopy(weldAbvFlang)    # column upper side
        self.weldAbvFlang_12 = copy.deepcopy(weldAbvFlang)      # column lower side

        self.weldBelwFlang_11 = copy.deepcopy(weldBelwFlang)    # column, upper, left
        self.weldBelwFlang_12 = copy.deepcopy(weldBelwFlang)    # column, upper, right
        self.weldBelwFlang_13 = copy.deepcopy(weldBelwFlang)    # column, lower, left
        self.weldBelwFlang_14 = copy.deepcopy(weldBelwFlang)    # column, lower, right


        self.weldSideWeb_11 = copy.deepcopy(weldSideWeb)        # column, left of Web
        self.weldSideWeb_12 = copy.deepcopy(weldSideWeb)        # column, right of Web


    def create_3DModel(self):
        """

        :return: CAD model of each of the followings.
        """

        self.createColumnGeometry()
        self.createBasePlateGeometry()
        self.createWeldGeometry()
        self.create_nut_bolt_array()
        
        self.columnModel = self.column.create_model()
        self.baseplateModel = self.baseplate.create_model()

        self.weldAbvFlang_11Model = self.weldAbvFlang_11.create_model()
        self.weldAbvFlang_12Model = self.weldAbvFlang_12.create_model()

        self.weldBelwFlang_11Model = self.weldBelwFlang_11.create_model()
        self.weldBelwFlang_12Model = self.weldBelwFlang_12.create_model()
        self.weldBelwFlang_13Model = self.weldBelwFlang_13.create_model()
        self.weldBelwFlang_14Model = self.weldBelwFlang_14.create_model()

        self.weldSideWeb_11Model = self.weldSideWeb_11.create_model()
        self.weldSideWeb_12Model = self.weldSideWeb_12.create_model()

    def createColumnGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        columnOriginL = numpy.array([0.0, 0.0, 0.0])
        columnL_uDir = numpy.array([1.0, 0.0, 0.0])
        columnL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.column.place(columnOriginL, columnL_uDir, columnL_wDir)

    def createBasePlateGeometry(self):
        baseplateOriginL = numpy.array(([0.0, 0.0, 0.0])
        baseplateL_uDir = numpy.array([0.0, 1.0, 0.0])
        baseplateL_wDir = numpy.array([1.0, 0.0, 0.0])
        self.baseplate.place(baseplateOriginL, baseplateL_uDir, baseplateL_wDir)
 
    def createWeldGeometry(self):
        
        # weld above flange
        weldAbvFlangOrigin_11 = numpy.array([self.column.B / 2, self.column.length, self.column.D / 2])
        uDirAbv_11 = numpy.array([0, -1.0, 0])
        wDirAbv_11 = numpy.array([-1.0, 0, 0])
        self.weldAbvFlang_11.place(weldAbvFlangOrigin_11, uDirAbv_11, wDirAbv_11)

        weldAbvFlangOrigin_12 = numpy.array([-self.column.B / 2, self.column.length, -self.column.D / 2])
        uDirAbv_12 = numpy.array([0, -1.0, 0])
        wDirAbv_12 = numpy.array([1.0, 0, 0])
        self.weldAbvFlang_12.place(weldAbvFlangOrigin_12, uDirAbv_12, wDirAbv_12)

        # weld below flange
        weldBelwFlangOrigin_11 = numpy.array([self.column.R2 -self.column.B / 2, self.column.length, (self.column.D / 2) - self.column.T])
        uDirBelw_11 = numpy.array([0, -1.0, 0])
        wDirBelw_11 = numpy.array([1.0, 0, 0])
        self.weldBelwFlang_11.place(weldBelwFlangOrigin_11, uDirBelw_11, wDirBelw_11)

        weldBelwFlangOrigin_12 = numpy.array([self.column.R1 + self.column.t / 2, self.column.length, (self.column.D / 2) - self.column.T])
        uDirBelw_12 = numpy.array([0, -1.0, 0])
        wDirBelw_12 = numpy.array([1.0, 0, 0])
        self.weldBelwFlang_12.place(weldBelwFlangOrigin_12, uDirBelw_12, wDirBelw_12)

        weldBelwFlangOrigin_13 = numpy.array([-self.column.R1-self.column.t / 2, self.column.length, -(self.column.D / 2) + self.column.T])
        uDirBelw_13 = numpy.array([0, -1.0, 0])
        wDirBelw_13 = numpy.array([-1.0, 0, 0])
        self.weldBelwFlang_13.place(weldBelwFlangOrigin_13, uDirBelw_13, wDirBelw_13)

        weldBelwFlangOrigin_14 = numpy.array([-self.column.R2+self.column.B / 2, self.column.length, -(self.column.D / 2) + self.column.T])
        uDirBelw_14 = numpy.array([0, -1.0, 0])
        wDirBelw_14 = numpy.array([-1.0, 0, 0])
        self.weldBelwFlang_14.place(weldBelwFlangOrigin_14, uDirBelw_14, wDirBelw_14)

        # Weld side web
        weldSideWebOrigin_11 = numpy.array([-self.column.t/2, self.column.length, self.weldSideWeb_21.L / 2])
        uDirWeb_11 = numpy.array([0, -1.0, 0])
        wDirWeb_11 = numpy.array([0, 0, -1.0])
        self.weldSideWeb_11.place(weldSideWebOrigin_11, uDirWeb_11, wDirWeb_11)

        weldSideWebOrigin_12 = numpy.array([self.column.t / 2, self.column.length, -self.weldSideWeb_21.L / 2])
        uDirWeb_12 = numpy.array([0, -1.0, 0])
        wDirWeb_12 = numpy.array([0, 0, 1.0])
        self.weldSideWeb_12.place(weldSideWebOrigin_12, uDirWeb_12, wDirWeb_12)


    def create_nut_bolt_array(self):
        """

        :return: Geometric Orientation of this component
        """
        nutboltArrayOrigin = self.baseplate.sec_origin + numpy.array(
            [0.0, -0.5 * self.baseplate.T, self.baseplate.L / 2])
        gaugeDir = numpy.array([1.0, 0, 0])
        pitchDir = numpy.array([0, 0, -1.0])
        boltDir = numpy.array([0, 1.0, 0])
        self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

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

        welded_sec = [self.weldAbvFlang_11, self.weldAbvFlang_12, self.weldBelwFlang_11, self.weldBelwFlang_12, self.weldBelwFlang_13, self.weldBelwFlang_14, self.weldSideWeb_11, self.weldSideWeb_12]
        welds = welded_sec
        for comp in welded_sec[1:]:
            welds = BRepAlgoAPI_Fuse(comp, welds).Shape()

        return welds

    def get_plate_connector_models(self):
        plate = self.baseplateModel
        return plate

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

        CAD_list = [column, plate_connectors, welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD
        

# if __name__ == '__main__':
#     axis()
#     start_display()