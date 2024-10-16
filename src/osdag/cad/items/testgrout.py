"""
created on 09-03-2020

@author: Anand Swaroop

This file is for creating CAD model for cover baseplate bolted moment connection for connectivity Beam-Beam

"""

import numpy
import copy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse


class BasePlateCad(object):
    def __init__(self, column, nut_bolt_array, bolthight, baseplate, weldAbvFlang, weldBelwFlang, weldSideWeb,
                 concrete, gusset, stiffener, grout):

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
        self.gusset = gusset
        self.stiffener = stiffener
        self.grout = grout

        self.weldType = 'Groove'  # 'Fillet'

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

        self.gusset1 = copy.deepcopy(self.gusset)
        self.gusset2 = copy.deepcopy(self.gusset)

        self.stiffener1 = copy.deepcopy(self.stiffener)
        self.stiffener2 = copy.deepcopy(self.stiffener)
        self.stiffener3 = copy.deepcopy(self.stiffener)
        self.stiffener4 = copy.deepcopy(self.stiffener)

    def create_3DModel(self):
        """

        :return: CAD model of each of the followings.
        """

        self.createColumnGeometry()
        self.createBasePlateGeometry()
        self.createFilletWeldGeometry()
        self.createConcreteGeometry()
        self.create_nut_bolt_array()
        self.createGroutGeometry()
        self.createGrooveWeldGeometry()

    def createColumnGeometry(self):
        """

        :return: Geometric Orientation of this component
        """

        if self.weldType == 'Fillet':
            columnOriginL = numpy.array([0.0, 0.0, 0.0])

        else:
            columnOriginL = numpy.array([0.0, 0.0, self.weldSideWeb.h])

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

        # if self.BP.gusset_along_flange == 'Yes':
        gusset1OriginL = numpy.array([0.0, self.column.D / 2, self.gusset.W / 2])
        gusset1L_uDir = numpy.array([-1.0, 0.0, 0.0])
        gusset1L_wDir = numpy.array([0.0, 1.0, 0.0])
        self.gusset1.place(gusset1OriginL, gusset1L_uDir, gusset1L_wDir)

        self.gusset1Model = self.gusset1.create_model()

        gusset2OriginL = numpy.array([0.0, -self.column.D / 2 - self.gusset.T, self.gusset.W / 2])
        gusset2L_uDir = numpy.array([-1.0, 0.0, 0.0])
        gusset2L_wDir = numpy.array([0.0, 1.0, 0.0])
        self.gusset2.place(gusset2OriginL, gusset2L_uDir, gusset2L_wDir)

        self.gusset2Model = self.gusset2.create_model()

        stiffener_gap = self.column.B * 0.4
        stiffener1OriginL = numpy.array(
            [self.stiffener.T / 2 + stiffener_gap, self.column.D / 2 + self.stiffener.L / 2 + self.gusset.T,
             self.stiffener.W / 2])
        stiffener1L_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1L_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.stiffener1.place(stiffener1OriginL, stiffener1L_uDir, stiffener1L_wDir)

        self.stiffener1Model = self.stiffener1.create_model()

        stiffener2OriginL = numpy.array(
            [self.stiffener.T / 2 - stiffener_gap, self.column.D / 2 + self.stiffener.L / 2 + self.gusset.T,
             self.stiffener.W / 2])
        stiffener2L_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener2L_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.stiffener2.place(stiffener2OriginL, stiffener2L_uDir, stiffener2L_wDir)

        self.stiffener2Model = self.stiffener2.create_model()

        stiffener3OriginL = numpy.array(
            [-self.stiffener.T / 2 + stiffener_gap, -(self.column.D / 2 + self.stiffener.L / 2 + self.gusset.T),
             self.stiffener.W / 2])
        stiffener3L_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener3L_wDir = numpy.array([1.0, 0.0, 0.0])
        self.stiffener3.place(stiffener3OriginL, stiffener3L_uDir, stiffener3L_wDir)

        self.stiffener3Model = self.stiffener3.create_model()

        stiffener4OriginL = numpy.array(
            [-self.stiffener.T / 2 - stiffener_gap, -(self.column.D / 2 + self.stiffener.L / 2 + self.gusset.T),
             self.stiffener.W / 2])
        stiffener4L_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener4L_wDir = numpy.array([1.0, 0.0, 0.0])
        self.stiffener4.place(stiffener4OriginL, stiffener4L_uDir, stiffener4L_wDir)

        self.stiffener4Model = self.stiffener4.create_model()

    def createFilletWeldGeometry(self):

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
        weldBelwFlangOrigin_11 = numpy.array(
            [self.column.R2 - self.column.B / 2, -(self.column.D / 2 - self.column.T), 0.0])
        uDirBelw_11 = numpy.array([0, 1.0, 0])
        wDirBelw_11 = numpy.array([1.0, 0, 0])
        self.weldBelwFlang_11.place(weldBelwFlangOrigin_11, uDirBelw_11, wDirBelw_11)

        weldBelwFlangOrigin_12 = numpy.array(
            [self.column.R1 + self.column.t / 2, -(self.column.D / 2 - self.column.T), 0.0])
        uDirBelw_12 = numpy.array([0, 1.0, 0])
        wDirBelw_12 = numpy.array([1.0, 0, 0])
        self.weldBelwFlang_12.place(weldBelwFlangOrigin_12, uDirBelw_12, wDirBelw_12)

        weldBelwFlangOrigin_13 = numpy.array(
            [-self.column.R1 - self.column.t / 2, (self.column.D / 2 - self.column.T), 0.0])
        uDirBelw_13 = numpy.array([0, -1.0, 0])
        wDirBelw_13 = numpy.array([-1.0, 0, 0])
        self.weldBelwFlang_13.place(weldBelwFlangOrigin_13, uDirBelw_13, wDirBelw_13)

        weldBelwFlangOrigin_14 = numpy.array(
            [-self.column.R2 + self.column.B / 2, (self.column.D / 2 - self.column.T), 0.0])
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

    def createGrooveWeldGeometry(self):
        pass
        # weld below flange
        weldAbvFlangOrigin = numpy.array(
            [self.column.B / 2, -self.column.D / 2 + self.weldAbvFlang.b / 2, self.weldAbvFlang.h / 2])
        uDirAbv = numpy.array([0, -1.0, 0])
        wDirAbv = numpy.array([-1.0, 0, 0])
        self.weldAbvFlang.place(weldAbvFlangOrigin, uDirAbv, wDirAbv)

        self.weldAbvFlangModel = self.weldAbvFlang.create_model()

        # weld below flange
        weldBelwFlangOrigin = numpy.array(
            [-self.column.B / 2, self.column.D / 2 - self.weldBelwFlang.b / 2, self.weldBelwFlang.h / 2])
        uDirBelw = numpy.array([0, 1.0, 0])
        wDirBelw = numpy.array([1.0, 0, 0])
        self.weldBelwFlang.place(weldBelwFlangOrigin, uDirBelw, wDirBelw)

        self.weldBelwFlangModel = self.weldBelwFlang.create_model()

        # Weld side web
        weldSideWebOrigin = numpy.array(
            [-self.column.t / 2 + self.weldSideWeb.b / 2, self.weldSideWeb.L / 2, self.weldSideWeb.h / 2])
        uDirWeb = numpy.array([0, 0.0, 1.0])
        wDirWeb = numpy.array([0, -1.0, 0.0])
        self.weldSideWeb.place(weldSideWebOrigin, uDirWeb, wDirWeb)

        self.weldSideWebModel = self.weldSideWeb.create_model()

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

        if self.weldType == 'Fillet':
            welded_sec = [self.weldAbvFlang_11Model, self.weldAbvFlang_12Model, self.weldBelwFlang_11Model,
                          self.weldBelwFlang_12Model,
                          self.weldBelwFlang_13Model, self.weldBelwFlang_14Model, self.weldSideWeb_11Model,
                          self.weldSideWeb_12Model]
        else:
            welded_sec = [self.weldAbvFlangModel, self.weldBelwFlangModel, self.weldSideWebModel]

        welds = welded_sec[0]

        for comp in welded_sec[1:]:
            welds = BRepAlgoAPI_Fuse(comp, welds).Shape()

        return welds

    def get_plate_connector_models(self):

        # if self.BP.gusset_along_flange == 'Yes':
        plate_list = [self.baseplateModel, self.gusset1Model, self.gusset2Model, self.stiffener1Model,
                      self.stiffener2Model, self.stiffener3Model, self.stiffener4Model]
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


if __name__ == '__main__':

    from cad.items.bolt import Bolt
    from cad.items.nut import Nut
    from cad.items.plate import Plate
    from cad.items.ISection import ISection
    from cad.items.filletweld import FilletWeld
    from cad.items.groove_weld import GrooveWeld
    from cad.items.concrete import Concrete
    from cad.BasePlateCad.nutBoltPlacement import NutBoltArray
    from cad.items.anchor_bolt import *
    from cad.items.nut import Nut
    from cad.items.stiffener_plate import StiffenerPlate
    from cad.items.concrete import Concrete
    from cad.items.grout import Grout

    import OCC.Core.V3d
    from OCC.Core.Quantity import Quantity_NOC_SADDLEBROWN, Quantity_NOC_BLUE1
    from OCC.Core.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
    from utilities import osdag_display_shape
    # from cad.common_logic import CommonDesignLogic

    # from OCC.Core.Graphic3d import Quantity_NOC_GRAY as GRAY
    from OCC.Core.Quantity import Quantity_NOC_GRAY25 as GRAY
    from OCC.gp import gp_Pnt
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    column = ISection(B=250, T=13.7, D=450, t=9.8, R1=15.0, R2=7.5, alpha=94, length=1500, notchObj=None)
    baseplate = Plate(L=650, W=415, T=45)

    weldType = 'Groove'  # 'Fillet'

    if weldType == 'Fillet':
        weldAbvFlang = FilletWeld(b=10, h=10, L=250)
        weldBelwFlang = FilletWeld(b=10, h=10, L=100)
        weldSideWeb = FilletWeld(b=10, h=10, L=420)

    else:
        weldAbvFlang = GrooveWeld(b=column.T, h=10, L=column.B)
        weldBelwFlang = GrooveWeld(b=column.T, h=10, L=column.B)
        weldSideWeb = GrooveWeld(b=column.t, h=10, L=column.D)
    # concrete = Concrete(L= baseplate.W*1.5, W= baseplate.L*1.5, T= baseplate.T*10)
    concrete = Plate(L=baseplate.L * 1.5, W=baseplate.W * 1.5, T=baseplate.T * 10)
    grout = Grout(L=concrete.L, W=concrete.W, T=50)

    gusset = StiffenerPlate(L=baseplate.W, W=200, T=14, L11=(baseplate.W - (column.B + 100)) / 2, L12=200 - 100,
                            R11=(baseplate.W - (column.B + 100)) / 2, R12=200 - 100)
    stiffener = StiffenerPlate(L=(baseplate.L - column.D - 2 * gusset.T) / 2, W=gusset.W, T=gusset.T,
                               L11=(baseplate.L - column.D - 2 * gusset.T) / 2 - 50, L12=gusset.W - 100)

    type = 'gusset'  # 'no_gusset'

    ex_length = (50 + 24 + baseplate.T)  # nut.T = 24
    bolt = AnchorBolt_A(l=250, c=125, a=75, r=12, ex=ex_length)
    # bolt = AnchorBolt_B(l= 250, c= 125, a= 75, r= 12)
    # bolt = AnchorBolt_Endplate(l= 250, c= 125, a= 75, r= 12)
    nut = Nut(R=bolt.r * 3, T=24, H=30, innerR1=bolt.r)
    numberOfBolts = 4
    nutSpace = bolt.c + baseplate.T
    bolthight = nut.T + 50

    nut_bolt_array = NutBoltArray(column, baseplate, nut, bolt, numberOfBolts, nutSpace)

    basePlate = BasePlateCad(column, nut_bolt_array, bolthight, baseplate, weldAbvFlang, weldBelwFlang, weldSideWeb,
                             concrete, gusset, stiffener, grout)

    basePlate.create_3DModel()
    prism = basePlate.get_models()
    column = basePlate.get_column_model()
    plate = basePlate.get_plate_connector_models()
    weld = basePlate.get_welded_models()
    nut_bolt = basePlate.get_nut_bolt_array_models()
    conc = basePlate.get_concrete_models()
    grt = basePlate.get_grout_models()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    # p2 = gp_Pnt(0.0, -baseplate.W/2, -baseplate.T/2)
    # display.DisplayMessage(p2, "BasePlate")

    # display.DisplayShape(prism, update=True)
    display.DisplayShape(column, update=True)
    display.DisplayShape(plate, color='BLUE', update=True)
    display.DisplayShape(weld, color='RED', update=True)
    display.DisplayShape(nut_bolt, color='YELLOW', update=True)
    display.DisplayShape(conc, color=GRAY, transparency=0.5, update=True)
    display.DisplayShape(grt, color=GRAY, transparency=0.5, update=True)
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
