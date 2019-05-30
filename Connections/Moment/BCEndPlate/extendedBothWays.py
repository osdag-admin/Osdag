"""
Initialized on 23-04-2019
Commenced on 24-04-2019
@author: Anand Swaroop
"""""

import numpy

class CADFillet(object):
    def __init__(self, beamLeft, beamRight, plateRight, nut_bolt_array, bbWeldAbvFlang_21, bbWeldAbvFlang_22,
                 bbWeldBelwFlang_21, bbWeldBelwFlang_22, bbWeldBelwFlang_23, bbWeldBelwFlang_24, bbWeldSideWeb_21,
                 bbWeldSideWeb_22, contPL1Weld_U1,  contPlate_L1, contPlate_L2, contPlate_R1, contPlate_R2,beam_stiffener_1,beam_stiffener_2, endplate_type, conn_type, outputobj):

        # Initializing the arguments
        self.beamLeft = beamLeft  # beamLeft represents the column
        self.beamRight = beamRight
        self.plateRight = plateRight
        self.nut_bolt_array = nut_bolt_array
        self.beamRight.length = 1000.0
        self.contPlate_L1 = contPlate_L1
        self.contPlate_L2 = contPlate_L2
        self.contPlate_R1 = contPlate_R1
        self.contPlate_R2 = contPlate_R2
        self.beam_stiffener_1 = beam_stiffener_1
        self.beam_stiffener_2 = beam_stiffener_2

        self.endplate_type = endplate_type
        self.conn_type = conn_type                  #TODO: Remove this type if not needed
        self.outputobj = outputobj
        self.boltProjection = float(outputobj["Bolt"]['projection'])  # gives the bolt projection
        # self.Lv = float(outputobj["Bolt"]["Lv"])

        # Weld above flange for left and right beam
        self.bbWeldAbvFlang_21 = bbWeldAbvFlang_21  # Right beam upper side
        self.bbWeldAbvFlang_22 = bbWeldAbvFlang_22  # Right beam lower side

        self.bbWeldBelwFlang_21 = bbWeldBelwFlang_21  # behind bbWeldBelwFlang_11
        self.bbWeldBelwFlang_22 = bbWeldBelwFlang_22  # behind bbWeldBelwFlang_12
        self.bbWeldBelwFlang_23 = bbWeldBelwFlang_23  # behind bbWeldBelwFlang_13
        self.bbWeldBelwFlang_24 = bbWeldBelwFlang_24  # behind bbWeldBelwFlang_14

        self.bbWeldSideWeb_21 = bbWeldSideWeb_21  # Behind bbWeldSideWeb_11
        self.bbWeldSideWeb_22 = bbWeldSideWeb_22  # Behind bbWeldSideWeb_12
        self.contPL1Weld_U1 = contPL1Weld_U1

    def create_3DModel(self):
        """
        :return: CAD model of each entity such as Left beam, right beam, both end plates and so on
        """
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()
        self.create_contPlate_L1Geometry()
        self.create_contPlate_L2Geometry()
        self.create_contPlate_R1Geometry()
        self.create_contPlate_R2Geometry()
        self.create_beam_stiffener_1Geometry()
        self.create_beam_stiffener_2Geometry()

        self.create_bbWeldAbvFlang_21()  # left beam above flange weld
        self.create_bbWeldAbvFlang_22()  # left beam above 2nd (lower) flange

        self.create_bbWeldBelwFlang_21()  # right beam weld similar to left beam
        self.create_bbWeldBelwFlang_22()
        self.create_bbWeldBelwFlang_23()
        self.create_bbWeldBelwFlang_24()

        self.create_bbWeldSideWeb_21()  # right beam weld behind left beam
        self.create_bbWeldSideWeb_22()  # right beam weld behind left beam

        self.create_contPL1Weld_U1()


        # call for create_model of filletweld from Components directory
        self.beamLModel = self.beamLeft.create_model()
        self.beamRModel = self.beamRight.create_model()
        self.plateRModel = self.plateRight.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()
        self.contPlate_L1Model = self.contPlate_L1.create_model()
        self.contPlate_L2Model = self.contPlate_L2.create_model()
        self.contPlate_R1Model = self.contPlate_R1.create_model()
        self.contPlate_R2Model = self.contPlate_R2.create_model()
        self.beam_stiffener_1Model = self.beam_stiffener_1.create_model()
        self.beam_stiffener_2Model = self.beam_stiffener_2.create_model()

        self.bbWeldAbvFlang_21Model = self.bbWeldAbvFlang_21.create_model()
        self.bbWeldAbvFlang_22Model = self.bbWeldAbvFlang_22.create_model()

        self.bbWeldBelwFlang_21Model = self.bbWeldBelwFlang_21.create_model()
        self.bbWeldBelwFlang_22Model = self.bbWeldBelwFlang_22.create_model()
        self.bbWeldBelwFlang_23Model = self.bbWeldBelwFlang_23.create_model()
        self.bbWeldBelwFlang_24Model = self.bbWeldBelwFlang_24.create_model()

        self.bbWeldSideWeb_21Model = self.bbWeldSideWeb_21.create_model()
        self.bbWeldSideWeb_22Model = self.bbWeldSideWeb_22.create_model()

        self.contPL1Weld_U1Model = self.contPL1Weld_U1.create_model()


    #############################################################################################################
    #   Following functions takes inputs as origin, u direction and w direction of concerned component to place #
    #   same component at appropriate place                                                                     #
    #############################################################################################################

    def createBeamLGeometry(self):
        # if self.conn_type == 'col_flange_connectivity':
        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

        # else: #self.conn_type ==  'col_web_connectivity'
        #     beamOriginL = numpy.array([0.0, self.beamLeft.D/2, 0.0])
        #     beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        #     beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        #     self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamRGeometry(self):
        gap = self.beamLeft.D / 2 + self.plateRight.T
        beamOriginR = numpy.array([0.0, gap, self.beamLeft.length / 2])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateRGeometry(self):

        if self.endplate_type == "one_way":
            gap = 0.5 * self.plateRight.T + self.beamLeft.D / 2
            plateOriginR = numpy.array([-self.plateRight.W / 2, gap, self.beamLeft.length / 2 + (
                        self.plateRight.L / 2 - self.boltProjection - self.beamRight.D / 2)])  # TODO #Add weld thickness here
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

        else:  # self.endplate_type == "both_way" and flushed
            gap = 0.5 * self.plateRight.T + self.beamLeft.D / 2
            plateOriginR = numpy.array([-self.plateRight.W / 2, gap, self.beamLeft.length / 2])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

        # elif self.endplate_type == "flush":
        #     pass

    def create_nut_bolt_array(self):

        if self.endplate_type == "one_way":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array([0.0, self.beamLeft.T , + (self.plateRight.L / 2)])  # self.plateRight.L/2+ (self.plateRight.L/2 - (10) - self.beamRight.D /2) - 40#TODO add end distance here #self.plateRight.L/2 + (self.plateRight.L/2 - (10 + 8) - self.beamRight.D /2)
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "both_way":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array(
                [0.0, self.beamLeft.T, self.plateRight.L / 2])
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "flush":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array(
                [0.0, self.beamLeft.T, self.beamRight.D/2])  # TODO Add self.Lv instead of 25   #+ 30
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    ##############################################  Adding contPlates ########################################

    def create_contPlate_L1Geometry(self):
        beamOriginL = numpy.array([self.beamLeft.B / 2 - self.contPlate_L1.W / 2, 0.0,
                                   self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T/2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_L2Geometry(self):
        beamOriginL = numpy.array([self.beamLeft.B / 2 - self.contPlate_L2.W / 2, 0.0,
                                   self.beamLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L2.T/2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_R1Geometry(self):
        beamOriginL = numpy.array([-self.beamLeft.B / 2 + self.contPlate_R1.W / 2, 0.0,
                                   self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_R1.T/2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R1.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_R2Geometry(self):
        beamOriginL = numpy.array([-self.beamLeft.B / 2 + self.contPlate_R2.W / 2, 0.0,
                                   self.beamLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T / 2 - self.contPlate_R1.T/2 ])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R2.place(beamOriginL, beamL_uDir, beamL_wDir)

    ##############################################  Adding beam stiffeners #############################################
    def create_beam_stiffener_1Geometry(self):
        gap = self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L/2
        stiffenerOrigin1 = numpy.array([-self.beam_stiffener_1.T/2, gap, self.beamLeft.length / 2 + self.beamRight.D/2 + self.beam_stiffener_1.W/2])
        stiffener1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_1.place(stiffenerOrigin1, stiffener1_uDir, stiffener1_wDir)

    def create_beam_stiffener_2Geometry(self):
        gap = self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L/2
        stiffenerOrigin2 = numpy.array([self.beam_stiffener_1.T/2, gap, self.beamLeft.length / 2 - self.beamRight.D/2 - self.beam_stiffener_1.W/2])
        stiffener2_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener2_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_2.place(stiffenerOrigin2, stiffener2_uDir, stiffener2_wDir)

    ##############################################  creating weld sections ########################################
    def create_bbWeldAbvFlang_21(self):
        weldAbvFlangOrigin_21 = numpy.array([-self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                             self.beamLeft.length / 2 + self.beamRight.D / 2])
        uDirAbv_21 = numpy.array([0, 1.0, 0])
        wDirAbv_21 = numpy.array([1.0, 0, 0])
        self.bbWeldAbvFlang_21.place(weldAbvFlangOrigin_21, uDirAbv_21, wDirAbv_21)

    def create_bbWeldAbvFlang_22(self):
        weldAbvFlangOrigin_22 = numpy.array([self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                             self.beamLeft.length / 2 - self.beamRight.D / 2])
        uDirAbv_22 = numpy.array([0, 1.0, 0])
        wDirAbv_22 = numpy.array([-1.0, 0, 0])
        self.bbWeldAbvFlang_22.place(weldAbvFlangOrigin_22, uDirAbv_22, wDirAbv_22)

    def create_bbWeldBelwFlang_21(self):
        weldBelwFlangOrigin_21 = numpy.array([-self.beamRight.t / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2) -
                                              self.beamRight.T])
        uDirBelw_21 = numpy.array([0, 1.0, 0])
        wDirBelw_21 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_21.place(weldBelwFlangOrigin_21, uDirBelw_21, wDirBelw_21)

    def create_bbWeldBelwFlang_22(self):
        weldBelwFlangOrigin_22 = numpy.array([self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2) -
                                              self.beamRight.T])
        uDirBelw_22 = numpy.array([0, 1.0, 0])
        wDirBelw_22 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_22.place(weldBelwFlangOrigin_22, uDirBelw_22, wDirBelw_22)

    def create_bbWeldBelwFlang_23(self):
        weldBelwFlangOrigin_23 = numpy.array([-self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) +
                                              self.beamRight.T])
        uDirBelw_23 = numpy.array([0, 1.0, 0])
        wDirBelw_23 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_23.place(weldBelwFlangOrigin_23, uDirBelw_23, wDirBelw_23)

    def create_bbWeldBelwFlang_24(self):
        weldBelwFlangOrigin_24 = numpy.array([self.beamRight.t / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) +
                                              self.beamRight.T])
        uDirBelw_24 = numpy.array([0, 1.0, 0])
        wDirBelw_24 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_24.place(weldBelwFlangOrigin_24, uDirBelw_24, wDirBelw_24)

    def create_bbWeldSideWeb_21(self):
        weldSideWebOrigin_21 = numpy.array([-self.beamLeft.t / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                            self.beamLeft.length / 2 - self.bbWeldSideWeb_21.L / 2])
        uDirWeb_21 = numpy.array([0, 1.0, 0])
        wDirWeb_21 = numpy.array([0, 0, 1.0])
        self.bbWeldSideWeb_21.place(weldSideWebOrigin_21, uDirWeb_21, wDirWeb_21)

    def create_bbWeldSideWeb_22(self):
        weldSideWebOrigin_22 = numpy.array([self.beamLeft.t / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                            self.beamLeft.length / 2 + self.bbWeldSideWeb_21.L / 2])
        uDirWeb_22 = numpy.array([0, 1.0, 0])
        wDirWeb_22 = numpy.array([0, 0, -1.0])
        self.bbWeldSideWeb_22.place(weldSideWebOrigin_22, uDirWeb_22, wDirWeb_22)

    def create_contPL1Weld_U1(self):
        contPL1Weld_Origin_U1 = numpy.array([self.beamLeft.t/2 ,-self.beamLeft.D/2 + self.beamLeft.T,self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T/2])
        uDirWeb_U1 = numpy.array([0.0, 1.0, 0])
        wDirWeb_U1 = numpy.array([1.0, 0, 0.0])
        self.contPL1Weld_U1.place(contPL1Weld_Origin_U1, uDirWeb_U1, wDirWeb_U1)

    #############################################################################################################
    #   Following functions returns the CAD model to the function display_3DModel of main file                  #
    #############################################################################################################
    def get_beamLModel(self):
        return self.beamLModel

    def get_beamRModel(self):
        return self.beamRModel

    def get_plateRModel(self):
        return self.plateRModel

    def get_nutboltmodels(self):
        return self.nut_bolt_array.get_models()

    def get_contPlate_L1Model(self):
        return self.contPlate_L1Model

    def get_contPlate_L2Model(self):
        return self.contPlate_L2Model

    def get_contPlate_R1Model(self):
        return self.contPlate_R1Model

    def get_contPlate_R2Model(self):
        return self.contPlate_R2Model

    def get_beam_stiffener_1Model(self):
        return  self.beam_stiffener_1Model

    def get_beam_stiffener_2Model(self):
        return self.beam_stiffener_2Model

    def get_bbWeldAbvFlang_21Model(self):
        return self.bbWeldAbvFlang_21Model

    def get_bbWeldAbvFlang_22Model(self):
        return self.bbWeldAbvFlang_22Model

    def get_bbWeldBelwFlang_21Model(self):
        return self.bbWeldBelwFlang_21Model

    def get_bbWeldBelwFlang_22Model(self):
        return self.bbWeldBelwFlang_22Model

    def get_bbWeldBelwFlang_23Model(self):
        return self.bbWeldBelwFlang_23Model

    def get_bbWeldBelwFlang_24Model(self):
        return self.bbWeldBelwFlang_24Model

    def get_bbWeldSideWeb_21Model(self):
        return self.bbWeldSideWeb_21Model

    def get_bbWeldSideWeb_22Model(self):
        return self.bbWeldSideWeb_22Model

    def get_contPL1Weld_U1Model(self):
        return self.contPL1Weld_U1Model

class CADColWebFillet(CADFillet):

    def createBeamLGeometry(self):
        beamOriginL = numpy.array([0.0, self.beamLeft.D/2 - self.beamLeft.t/2, 0.0])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)



        ##############################################  Adding contPlates ########################################

    def create_contPlate_L1Geometry(self):
        beamOriginL = numpy.array(
            [0.0, self.beamLeft.D / 2 - self.beamLeft.t  - self.contPlate_L1.W / 2,
             self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T/2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_L2Geometry(self):
        beamOriginL = numpy.array(
            [0.0, self.beamLeft.D / 2 - self.beamLeft.t - self.contPlate_L2.W / 2,
             self.beamLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L2.T/2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)




        #############################################################################################################
        #   Following functions returns the CAD model to the function display_3DModel of main file                  #
        #############################################################################################################

    def get_beamLModel(self):
        return self.beamLModel


    def get_contPlate_L1Model(self):
        return self.contPlate_L1Model

    def get_contPlate_L2Model(self):
        return self.contPlate_L2Model

class CADGroove(object):

    def __init__(self, beamLeft, beamRight, plateRight, nut_bolt_array,  bcWeldFlang_1, bcWeldFlang_2, bcWeldWeb_3,
                 contPlate_L1,contPlate_L2,contPlate_R1,contPlate_R2,beam_stiffener_1,beam_stiffener_2, endplate_type, outputobj):

        # Initializing the arguments
        self.beamLeft = beamLeft                            # beamLeft represents the column
        self.beamRight = beamRight
        self.plateRight = plateRight
        self.nut_bolt_array = nut_bolt_array
        self.beamRight.length = 1000.0
        self.contPlate_L1 = contPlate_L1
        self.contPlate_L2 = contPlate_L2
        self.contPlate_R1 = contPlate_R1
        self.contPlate_R2 = contPlate_R2
        self.beam_stiffener_1 = beam_stiffener_1
        self.beam_stiffener_2 = beam_stiffener_2
        self.endplate_type = endplate_type
        self.outputobj = outputobj
        self.boltProjection = float(outputobj["Bolt"]['projection'])  # gives the bolt projection
        # self.Lv = float(outputobj["Bolt"]["Lv"])

        self.boltProjection = float(outputobj["Bolt"]['projection'])  # gives the bolt projection d


        # Weld above flange for left and right beam
        self.bcWeldFlang_1 = bcWeldFlang_1
        self.bcWeldFlang_2 = bcWeldFlang_2
        self.bcWeldWeb_3 = bcWeldWeb_3




    def create_3DModel(self):
        """
        :return: CAD model of each entity such as Left beam, right beam, both end plates and so on
        """
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()
        self.create_contPlate_L1Geometry()
        self.create_contPlate_L2Geometry()
        self.create_contPlate_R1Geometry()
        self.create_contPlate_R2Geometry()
        self.create_beam_stiffener_1Geometry()
        self.create_beam_stiffener_2Geometry()


        self.create_bcWeldFlang_1()
        self.create_bcWeldFlang_2()
        self.create_bcWeldWeb_3()


        # call for create_model of filletweld from Components directory
        self.beamLModel = self.beamLeft.create_model()
        self.beamRModel = self.beamRight.create_model()
        self.plateRModel = self.plateRight.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()
        self.contPlate_L1Model = self.contPlate_L1.create_model()
        self.contPlate_L2Model = self.contPlate_L2.create_model()
        self.contPlate_R1Model = self.contPlate_R1.create_model()
        self.contPlate_R2Model = self.contPlate_R2.create_model()
        self.beam_stiffener_1Model = self.beam_stiffener_1.create_model()
        self.beam_stiffener_2Model = self.beam_stiffener_2.create_model()

        self.bcWeldFlang_1Model =  self.bcWeldFlang_1.create_model()
        self.bcWeldFlang_2Model = self.bcWeldFlang_2.create_model()
        self.bcWeldWeb_3Model = self.bcWeldWeb_3.create_model()

#############################################################################################################
#   Following functions takes inputs as origin, u direction and w direction of concerned component to place #
#   same component at appropriate place                                                                     #
#############################################################################################################

    def createBeamLGeometry(self):
        beamOriginL = numpy.array([0.0,0.0,0.0 ])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamRGeometry(self):
        gap = self.beamLeft.D /2  +  self.plateRight.T +  self.bcWeldWeb_3.b /2
        beamOriginR = numpy.array([0.0, gap, self.beamLeft.length /2 ])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateRGeometry(self):

        if self.endplate_type == "one_way":
            gap = 0.5 * self.plateRight.T + self.beamLeft.D / 2
            plateOriginR = numpy.array([-self.plateRight.W / 2, gap, self.beamLeft.length / 2 + (self.plateRight.L/2 - self.boltProjection - self.beamRight.D /2)])  #TODO #Add weld thickness here
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

        else:         #self.endplate_type == "both_way" and flushed
            gap = 0.5 * self.plateRight.T + self.beamLeft.D/2
            plateOriginR = numpy.array([-self.plateRight.W/2, gap, self.beamLeft.length /2 ])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)



    def create_nut_bolt_array(self):

        if self.endplate_type == "one_way":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array([0.0,  self.beamLeft.T,  + (self.plateRight.L/2 )])       # self.plateRight.L/2+ (self.plateRight.L/2 - (10) - self.beamRight.D /2) - 40#TODO add end distance here #self.plateRight.L/2 + (self.plateRight.L/2 - (10 + 8) - self.beamRight.D /2)
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "both_way":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array([0.0, self.beamLeft.T , self.plateRight.L /2])
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "flush":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array([0.0, self.beamLeft.T, self.beamRight.D/2])       #TODO Add self.Lv instead of 25
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    ##############################################  Adding contPlates ########################################

    def create_contPlate_L1Geometry(self):
        beamOriginL = numpy.array([self.beamLeft.B/2 - self.contPlate_L1.W/2, 0.0, self.beamLeft.length/2 + self.beamRight.D/2 - self.beamRight.T/2 + self.contPlate_L1.T/2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_L2Geometry(self):
        beamOriginL = numpy.array([self.beamLeft.B/2 - self.contPlate_L2.W/2, 0.0, self.beamLeft.length/2 - self.beamRight.D/2 + self.beamRight.T/2 + self.contPlate_L2.T/2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_R1Geometry(self):
        beamOriginL = numpy.array([-self.beamLeft.B/2 + self.contPlate_R1.W/2, 0.0, self.beamLeft.length/2 + self.beamRight.D/2 - self.beamRight.T/2 - self.contPlate_R1.T/2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R1.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_R2Geometry(self):
        beamOriginL = numpy.array([-self.beamLeft.B/2 + self.contPlate_R2.W/2, 0.0, self.beamLeft.length/2 - self.beamRight.D/2 + self.beamRight.T/2 - self.contPlate_R2.T/2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R2.place(beamOriginL, beamL_uDir, beamL_wDir)

    ##############################################  Adding beam stiffeners #############################################
    def create_beam_stiffener_1Geometry(self):
        gap = self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L/2
        stiffenerOrigin1 = numpy.array([-self.beam_stiffener_1.T/2, gap, self.beamLeft.length / 2 + self.beamRight.D/2 + self.beam_stiffener_1.W/2])
        stiffener1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_1.place(stiffenerOrigin1, stiffener1_uDir, stiffener1_wDir)

    def create_beam_stiffener_2Geometry(self):
        gap = self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L/2
        stiffenerOrigin2 = numpy.array([self.beam_stiffener_1.T/2, gap, self.beamLeft.length / 2 - self.beamRight.D/2 - self.beam_stiffener_1.W/2])
        stiffener2_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener2_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_2.place(stiffenerOrigin2, stiffener2_uDir, stiffener2_wDir)

    ##############################################  creating weld sections ########################################

    def create_bcWeldFlang_1(self):
        weldFlangOrigin_1 = numpy.array([-self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                             self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T/2])
        uDir_1 = numpy.array([0, 1.0, 0])
        wDir_1 = numpy.array([1.0, 0, 0])
        self.bcWeldFlang_1.place(weldFlangOrigin_1, uDir_1, wDir_1)
    def create_bcWeldFlang_2(self):
        weldFlangOrigin_2 = numpy.array([self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                             self.beamLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T/2])
        uDir_2 = numpy.array([0, 1.0, 0])
        wDir_2 = numpy.array([-1.0, 0, 0])
        self.bcWeldFlang_2.place(weldFlangOrigin_2, uDir_2, wDir_2)
    def create_bcWeldWeb_3(self):
        weldWebOrigin_3 = numpy.array([0.0, self.beamLeft.D / 2 + self.plateRight.T,
                                            self.beamLeft.length / 2 - self.bcWeldWeb_3.L / 2])
        uDirWeb_3 = numpy.array([0, 1.0, 0])
        wDirWeb_3 = numpy.array([0, 0, 1.0])
        self.bcWeldWeb_3.place(weldWebOrigin_3, uDirWeb_3, wDirWeb_3)


#############################################################################################################
#   Following functions returns the CAD model to the function display_3DModel of main file                  #
#############################################################################################################
    def get_beamLModel(self):
        return self.beamLModel

    def get_beamRModel(self):
        return self.beamRModel

    def get_plateRModel(self):
        return self.plateRModel

    def get_nutboltmodels(self):
        return self.nut_bolt_array.get_models()

    def get_contPlate_L1Model(self):
        return self.contPlate_L1Model

    def get_contPlate_L2Model(self):
        return self.contPlate_L2Model

    def get_contPlate_R1Model(self):
        return self.contPlate_R1Model

    def get_contPlate_R2Model(self):
        return self.contPlate_R2Model

    def get_beam_stiffener_1Model(self):
        return  self.beam_stiffener_1Model

    def get_beam_stiffener_2Model(self):
        return self.beam_stiffener_2Model

    def get_bcWeldFlang_1Model(self):
        return self.bcWeldFlang_1Model

    def get_bcWeldFlang_2Model(self):
        return self.bcWeldFlang_2Model

    def get_bcWeldWeb_3Model(self):
        return self.bcWeldWeb_3Model


class CADcolwebGroove(CADGroove):
    def createBeamLGeometry(self):
        beamOriginL = numpy.array([0.0, self.beamLeft.D/2 - self.beamLeft.t/2, 0.0])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)



        ##############################################  Adding contPlates ########################################

    def create_contPlate_L1Geometry(self):
        beamOriginL = numpy.array(
            [0.0, self.beamLeft.D/2 - self.beamLeft.t - self.contPlate_L1.W/2, self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T/2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_L2Geometry(self):
        beamOriginL = numpy.array(
            [0.0,  self.beamLeft.D/2 - self.beamLeft.t - self.contPlate_L2.W/2, self.beamLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L2.T/2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)