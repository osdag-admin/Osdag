
"""
created on 09-03-2020

@author: Anand Swaroop

This file is for creating CAD model for cover baseplate bolted moment connection for connectivity Beam-Beam

"""

import numpy
import copy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse

class BasePlateCad(object):
    def __init__(self, column, nut_bolt_array, bolthight, baseplate, weldAbvFlang, weldBelwFlang, weldSideWeb, concrete):

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
        self.nut_bolt_array = nut_bolt_array
        self.bolthight = bolthight
        self.baseplate = baseplate
        self.weldAbvFlang = weldAbvFlang
        self.weldBelwFlang = weldBelwFlang
        self.weldSideWeb = weldSideWeb
        self.concrete = concrete


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

    def create_3DModel(self):
        """

        :return: CAD model of each of the followings.
        """

        self.createColumnGeometry()
        self.createBasePlateGeometry()
        self.createWeldGeometry()
        self.createConcreteGeometry()
        self.create_nut_bolt_array()

        self.columnModel = self.column.create_model()
        self.baseplateModel = self.baseplate.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()

        self.weldAbvFlang_11Model = self.weldAbvFlang_11.create_model()
        self.weldAbvFlang_12Model = self.weldAbvFlang_12.create_model()

        self.weldBelwFlang_11Model = self.weldBelwFlang_11.create_model()
        self.weldBelwFlang_12Model = self.weldBelwFlang_12.create_model()
        self.weldBelwFlang_13Model = self.weldBelwFlang_13.create_model()
        self.weldBelwFlang_14Model = self.weldBelwFlang_14.create_model()

        self.weldSideWeb_11Model = self.weldSideWeb_11.create_model()
        self.weldSideWeb_12Model = self.weldSideWeb_12.create_model()

        self.concreteModel = self.concrete.create_model()


    def createColumnGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        columnOriginL = numpy.array([0.0, 0.0, 0.0])
        columnL_uDir = numpy.array([1.0, 0.0, 0.0])
        columnL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.column.place(columnOriginL, columnL_uDir, columnL_wDir)

    def createBasePlateGeometry(self):
        baseplateOriginL = numpy.array([-self.baseplate.W/2, 0.0 , -self.baseplate.T/2])
        baseplateL_uDir = numpy.array([0.0, 0.0, 1.0])
        baseplateL_wDir = numpy.array([1.0, 0.0, 0.0])
        self.baseplate.place(baseplateOriginL, baseplateL_uDir, baseplateL_wDir)


    def createWeldGeometry(self):

        # weld above flange
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
        weldSideWebOrigin_11 = numpy.array([-self.column.t / 2, self.weldSideWeb_11.L/2, 0.0])
        uDirWeb_11 = numpy.array([0, 0.0, 1.0])
        wDirWeb_11 = numpy.array([0, -1.0, 0.0])
        self.weldSideWeb_11.place(weldSideWebOrigin_11, uDirWeb_11, wDirWeb_11)

        weldSideWebOrigin_12 = numpy.array([self.column.t / 2, -self.weldSideWeb_12.L/2,  0.0])
        uDirWeb_12 = numpy.array([0, 0.0, 1.0])
        wDirWeb_12 = numpy.array([0, 1.0, 0.0])
        self.weldSideWeb_12.place(weldSideWebOrigin_12, uDirWeb_12, wDirWeb_12)

    def create_nut_bolt_array(self):
        """

        :return: Geometric Orientation of this component
        """
        # nutboltArrayOrigin = self.baseplate.sec_origin + numpy.array([0.0, 0.0, self.baseplate.T /2+ 100])
        nutboltArrayOrigin = numpy.array([ -self.baseplate.W/2 , self.baseplate.L/2, self.bolthight ])
        gaugeDir = numpy.array([1.0, 0, 0])
        pitchDir = numpy.array([0, -1.0, 0])
        boltDir = numpy.array([0, 0, 1.0])
        self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    def createConcreteGeometry(self):
        """

        :return: Geometric Orientation of concrete
        """
        concreteOrigin = numpy.array([-self.concrete.W/2, 0.0 , -self.baseplate.T - self.concrete.T/2])
        # concrete_uDir = numpy.array([1.0, 0.0, 0.0])
        # concrete_wDir = numpy.array([0.0, 0.0, 1.0])
        concrete_uDir = numpy.array([0.0, 0.0, 1.0])
        concrete_wDir = numpy.array([1.0, 0.0, 0.0])
        self.concrete.place(concreteOrigin, concrete_uDir, concrete_wDir)

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

        welded_sec = [self.weldAbvFlang_11Model, self.weldAbvFlang_12Model, self.weldBelwFlang_11Model, self.weldBelwFlang_12Model,
                      self.weldBelwFlang_13Model, self.weldBelwFlang_14Model, self.weldSideWeb_11Model, self.weldSideWeb_12Model]
        welds = welded_sec[0]

        for comp in welded_sec[1:]:
            welds = BRepAlgoAPI_Fuse(comp, welds).Shape()

        return welds

    def get_plate_connector_models(self):
        plate = self.baseplateModel
        return plate

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

        CAD_list = [column, plate_connectors, welds, nut_bolt_array, conc] #, welds, nut_bolt_array]
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
    from cad.items.concrete import Concrete
    from cad.BasePlateCad.nutBoltPlacement import NutBoltArray
    from cad.items.anchor_bolt import *
    from cad.items.nut import Nut
    # from design_type.connection.base_plate_connection import BasePlateConnection as BP

    import OCC.Core.V3d
    from OCC.Core.Quantity import Quantity_NOC_SADDLEBROWN, Quantity_NOC_BLUE1
    from OCC.Core.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
    from utilities import osdag_display_shape
    # from cad.common_logic import CommonDesignLogic

    from OCC.gp import gp_Pnt
    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    # cal = BP.design_gusset_plate()
    column = ISection(B=250, T=13.7, D=450, t=9.8, R1= 14.0, R2= 7.0, alpha= 94, length= 1500, notchObj= None)
    baseplate = Plate(L=650, W=500, T=30)
    weldAbvFlang = FilletWeld(b=3, h=3, L= 250)
    weldBelwFlang = FilletWeld(b=3, h=3, L= 100)
    weldSideWeb = FilletWeld(b=3, h=3, L= 420)
    # concrete = Concrete(L= baseplate.W*1.5, W= baseplate.L*1.5, T= baseplate.T*10)
    concrete = Plate(L= baseplate.L*1.5, W= baseplate.W*1.5, T= baseplate.T*10)

    #Todo: Make this class in another file


    ex_length = (50 + 24 + baseplate.T)  # nut.T = 24
    bolt = AnchorBolt_A(l= 250, c= 125, a= 75, r= 12, ex= ex_length)
    # bolt = AnchorBolt_B(l= 250, c= 125, a= 75, r= 12)
    # bolt = AnchorBolt_Endplate(l= 250, c= 125, a= 75, r= 12)
    nut = Nut(R= bolt.r*3, T= 24, H= 30, innerR1= bolt.r)
    numberOfBolts = 4
    nutSpace = bolt.c + baseplate.T
    bolthight = nut.T + 50

    nut_bolt_array = NutBoltArray(column, baseplate,  nut, bolt, numberOfBolts, nutSpace)

    basePlate = BasePlateCad(column, nut_bolt_array, bolthight, baseplate, weldAbvFlang, weldBelwFlang, weldSideWeb, concrete)

    basePlate.create_3DModel()
    prism = basePlate.get_models()
    column = basePlate.get_column_model()
    plate = basePlate.get_plate_connector_models()
    weld = basePlate.get_welded_models()
    nut_bolt = basePlate.get_nut_bolt_array_models()
    conc = basePlate.get_concrete_models()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    # p2 = gp_Pnt(0.0, -baseplate.W/2, -baseplate.T/2)
    # display.DisplayMessage(p2, "BasePlate")

    # display.DisplayShape(prism, update=True)
    display.DisplayShape(column, update=True)
    display.DisplayColoredShape(plate, color='BLUE', update=True)
    display.DisplayColoredShape(weld, color='RED', update=True)
    display.DisplayColoredShape(nut_bolt, color='YELLOW', update=True)
    display.DisplayShape(conc, color='CYAN', transparency=0.5,  update=True)
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