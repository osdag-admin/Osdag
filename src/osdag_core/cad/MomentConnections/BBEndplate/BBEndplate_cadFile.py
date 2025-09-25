"""
Initialized on 22-01-2018
Commenced on 16-02-2018
@author: Siddhesh S. Chavan, Rahul Benal
modified : Anand Swaroop
modified : Darshan Vishwakarma (12-09-2020)
"""""

import numpy
import copy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse

class CADFillet(object): # not used in the current version as groove weld is preferred best practice.

    def __init__(self, module, beamLeft, beamRight, plateLeft, plateRight, nut_bolt_array,bbWeldAbvFlang, bbWeldBelwFlang, bbWeldSideWeb,bbWeldFlushstiffHeight, bbWeldFlushstiffLength,
                 bbWeldStiffHeight,bbWeldStiffLength,beam_stiffeners,beam_stiffenerFlush,alist, outputobj):
        """

        :param beamLeft: Left beam
        :param beamRight: Right beam
        :param plateLeft: Plate welded to left beam
        :param plateRight: Plate welded to Right beam
        :param nut_bolt_array:  Bolt placement on the end plates
        :param bbWeldAbvFlang: Weld surface on the outer side of flange
        :param bbWeldBelwFlang: Weld surface on the inner side of flange
        :param bbWeldSideWeb: Weld surface on the sides of the web
        :param bbWeldFlushstiffHeight: Weld surface along the height of the stiffeners for the flush end plate type
        :param bbWeldFlushstiffLength: Weld surface along the length of the stiffeners for the flush end plate type
        :param bbWeldStiffHeight: Weld surface along the height of the stiffeners for the extended and one-way end plate type
        :param bbWeldStiffLength: Weld surface along the length of the stiffeners for the extended and one-way end plate type
        :param beam_stiffeners: Stiffeners for the enxtended and one-way endplate
        :param beam_stiffenerFlush: Stiffeners for the flush endplate
        :param alist: Input dictionary
        :param outputobj: Output dictionary
        """


        # Initializing the arguments
        self.beamLeft = beamLeft
        self.beamRight = beamRight
        self.plateLeft = plateLeft
        self.plateRight = plateRight
        self.nut_bolt_array = nut_bolt_array
        self.beam_stiffener_1 = beam_stiffeners
        self.beam_stiffener_2 = copy.deepcopy(beam_stiffeners)
        self.beam_stiffener_3 = copy.deepcopy(beam_stiffeners)
        self.beam_stiffener_4 = copy.deepcopy(beam_stiffeners)

        self.beam_stiffener_F1 = beam_stiffenerFlush
        self.beam_stiffener_F2 = copy.deepcopy(beam_stiffenerFlush)
        self.beam_stiffener_F3 = copy.deepcopy(beam_stiffenerFlush)
        self.beam_stiffener_F4 = copy.deepcopy(beam_stiffenerFlush)
        # self.alist = alist
        # self.outputobj = outputobj
        self.boltProjection = float(outputobj['Plate']['Projection'])
        self.beamLModel = None
        self.beamRModel = None
        self.plateLModel = None
        self.plateRModel = None


        if self.module.endplate_type == 'Flushed - Reversible Moment':
            self.loc = float(outputobj['Stiffener']['Location'])

        else:
            self.loc = 0
        # self.boltProjection = float(outputobj["Bolt"]['projection'])          #TODO: ask danish to edit it into dictionary

        self.bbWeldAbvFlang_11Model = None
        self.bbWeldAbvFlang_12Model = None
        self.bbWeldAbvFlang_21Model = None
        self.bbWeldAbvFlang_22Model = None

        self.bbWeldBelwFlang_11Model = None
        self.bbWeldBelwFlang_12Model = None
        self.bbWeldBelwFlang_13Model = None
        self.bbWeldBelwFlang_14Model = None
        self.bbWeldBelwFlang_21Model = None
        self.bbWeldBelwFlang_22Model = None
        self.bbWeldBelwFlang_23Model = None
        self.bbWeldBelwFlang_24Model = None


        self.bbWeldSideWeb_11Model = None
        self.bbWeldSideWeb_12Model = None
        self.bbWeldSideWeb_21Model = None
        self.bbWeldSideWeb_22Model = None



        # Weld above flange for left and right beam
        self.bbWeldAbvFlang_11 = copy.deepcopy(bbWeldAbvFlang)    # Left beam upper side
        self.bbWeldAbvFlang_12 = copy.deepcopy(bbWeldAbvFlang)      # Left beam lower side
        self.bbWeldAbvFlang_21 = copy.deepcopy(bbWeldAbvFlang)     # Right beam upper side
        self.bbWeldAbvFlang_22 = copy.deepcopy(bbWeldAbvFlang)      # Right beam lower side

        self.bbWeldBelwFlang_11 = copy.deepcopy(bbWeldBelwFlang)    # Left beam, upper, left
        self.bbWeldBelwFlang_12 = copy.deepcopy(bbWeldBelwFlang)    # Left beam, upper, right
        self.bbWeldBelwFlang_13 = copy.deepcopy(bbWeldBelwFlang)    # Left beam, lower, left
        self.bbWeldBelwFlang_14 = copy.deepcopy(bbWeldBelwFlang)    # Left beam, lower, right
        self.bbWeldBelwFlang_21 = copy.deepcopy(bbWeldBelwFlang)    # behind bbWeldBelwFlang_11
        self.bbWeldBelwFlang_22 = copy.deepcopy(bbWeldBelwFlang)    # behind bbWeldBelwFlang_12
        self.bbWeldBelwFlang_23 = copy.deepcopy(bbWeldBelwFlang)    # behind bbWeldBelwFlang_13
        self.bbWeldBelwFlang_24 = copy.deepcopy(bbWeldBelwFlang)    # behind bbWeldBelwFlang_14


        self.bbWeldSideWeb_11 = copy.deepcopy(bbWeldSideWeb)        # Left beam, left of Web
        self.bbWeldSideWeb_12 = copy.deepcopy(bbWeldSideWeb)        # Left beam, right of Web
        self.bbWeldSideWeb_21 = copy.deepcopy(bbWeldSideWeb)       # Behind bbWeldSideWeb_11
        self.bbWeldSideWeb_22 = copy.deepcopy(bbWeldSideWeb)        # Behind bbWeldSideWeb_12

        self.bbWeldStiffHL_1 = bbWeldStiffHeight
        self.bbWeldStiffHL_2 = copy.deepcopy(bbWeldStiffHeight)
        self.bbWeldStiffHL_3 = copy.deepcopy(bbWeldStiffHeight)
        self.bbWeldStiffHL_4 = copy.deepcopy(bbWeldStiffHeight)
        self.bbWeldStiffHR_1 = copy.deepcopy(bbWeldStiffHeight)
        self.bbWeldStiffHR_2 = copy.deepcopy(bbWeldStiffHeight)
        self.bbWeldStiffHR_3 = copy.deepcopy(bbWeldStiffHeight)
        self.bbWeldStiffHR_4 = copy.deepcopy(bbWeldStiffHeight)

        self.bbWeldStiffLL_1 = bbWeldStiffLength
        self.bbWeldStiffLL_2 = copy.deepcopy(bbWeldStiffLength)
        self.bbWeldStiffLL_3 = copy.deepcopy(bbWeldStiffLength)
        self.bbWeldStiffLL_4 = copy.deepcopy(bbWeldStiffLength)
        self.bbWeldStiffLR_1 = copy.deepcopy(bbWeldStiffLength)
        self.bbWeldStiffLR_2 = copy.deepcopy(bbWeldStiffLength)
        self.bbWeldStiffLR_3 = copy.deepcopy(bbWeldStiffLength)
        self.bbWeldStiffLR_4 = copy.deepcopy(bbWeldStiffLength)

        self.bbWeldstiff1_u1 = bbWeldFlushstiffHeight
        self.bbWeldstiff1_l1 =copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff2_u1 =copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff2_l1 =copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff3_u1 =copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff3_l1 =copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff4_u1 =copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff4_l1 =copy.deepcopy(bbWeldFlushstiffHeight)

        self.bbWeldstiff1_u2 = bbWeldFlushstiffLength
        self.bbWeldstiff1_l2 =copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff2_u2 =copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff2_l2 =copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff3_u2 =copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff3_l2 =copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff4_u2 =copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff4_l2 =copy.deepcopy(bbWeldFlushstiffLength)


    def create_3DModel(self):
        '''
        call all the function which places the individual components to its location based on the connection required
        '''
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        self.createPlateLGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()
        self.createbeam_stiffenersGeometry()



        self.create_bbWeldAbvFlang()

        self.create_bbWeldBelwFlang()


        self.create_bbWeldSideWeb()

        self.create_bbWeldStiffHeight()
        self.create_bbWeldStiffLength()

        self.create_bbWeldFlushstiffHeight()
        self.create_bbWeldFlushstiffLength()


        # call for create_model of filletweld from Components directory
        self.beamLModel = self.beamLeft.create_model()
        self.beamRModel = self.beamRight.create_model()
        self.plateLModel = self.plateLeft.create_model()
        self.plateRModel = self.plateRight.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()
        self.beam_stiffener_1Model = self.beam_stiffener_1.create_model()
        self.beam_stiffener_2Model = self.beam_stiffener_2.create_model()
        self.beam_stiffener_3Model = self.beam_stiffener_3.create_model()
        self.beam_stiffener_4Model = self.beam_stiffener_4.create_model()

        self.beam_stiffener_F1Model = self.beam_stiffener_F1.create_model()
        self.beam_stiffener_F2Model = self.beam_stiffener_F2.create_model()
        self.beam_stiffener_F3Model = self.beam_stiffener_F3.create_model()
        self.beam_stiffener_F4Model = self.beam_stiffener_F4.create_model()

        self.bbWeldAbvFlang_11Model = self.bbWeldAbvFlang_11.create_model()
        self.bbWeldAbvFlang_12Model = self.bbWeldAbvFlang_12.create_model()
        self.bbWeldAbvFlang_21Model = self.bbWeldAbvFlang_21.create_model()
        self.bbWeldAbvFlang_22Model = self.bbWeldAbvFlang_22.create_model()

        self.bbWeldBelwFlang_11Model = self.bbWeldBelwFlang_11.create_model()
        self.bbWeldBelwFlang_12Model = self.bbWeldBelwFlang_12.create_model()
        self.bbWeldBelwFlang_13Model = self.bbWeldBelwFlang_13.create_model()
        self.bbWeldBelwFlang_14Model = self.bbWeldBelwFlang_14.create_model()
        self.bbWeldBelwFlang_21Model = self.bbWeldBelwFlang_21.create_model()
        self.bbWeldBelwFlang_22Model = self.bbWeldBelwFlang_22.create_model()
        self.bbWeldBelwFlang_23Model = self.bbWeldBelwFlang_23.create_model()
        self.bbWeldBelwFlang_24Model = self.bbWeldBelwFlang_24.create_model()


        self.bbWeldSideWeb_11Model = self.bbWeldSideWeb_11.create_model()
        self.bbWeldSideWeb_12Model = self.bbWeldSideWeb_12.create_model()
        self.bbWeldSideWeb_21Model = self.bbWeldSideWeb_21.create_model()
        self.bbWeldSideWeb_22Model = self.bbWeldSideWeb_22.create_model()

        self.bbWeldStiffHL_1Model = self.bbWeldStiffHL_1.create_model()
        self.bbWeldStiffHL_2Model = self.bbWeldStiffHL_2.create_model()
        self.bbWeldStiffHL_3Model = self.bbWeldStiffHL_3.create_model()
        self.bbWeldStiffHL_4Model = self.bbWeldStiffHL_4.create_model()

        self.bbWeldStiffLL_1Model = self.bbWeldStiffLL_1.create_model()
        self.bbWeldStiffLL_2Model = self.bbWeldStiffLL_2.create_model()
        self.bbWeldStiffLL_3Model = self.bbWeldStiffLL_3.create_model()
        self.bbWeldStiffLL_4Model = self.bbWeldStiffLL_4.create_model()
        self.bbWeldStiffHR_1Model = self.bbWeldStiffHR_1.create_model()
        self.bbWeldStiffHR_2Model = self.bbWeldStiffHR_2.create_model()
        self.bbWeldStiffHR_3Model = self.bbWeldStiffHR_3.create_model()
        self.bbWeldStiffHR_4Model = self.bbWeldStiffHR_4.create_model()

        self.bbWeldStiffLR_1Model = self.bbWeldStiffLR_1.create_model()
        self.bbWeldStiffLR_2Model = self.bbWeldStiffLR_2.create_model()
        self.bbWeldStiffLR_3Model = self.bbWeldStiffLR_3.create_model()
        self.bbWeldStiffLR_4Model = self.bbWeldStiffLR_4.create_model()

        self.bbWeldstiff1_u1Model = self.bbWeldstiff1_u1.create_model()
        self.bbWeldstiff1_u2Model = self.bbWeldstiff1_u2.create_model()
        self.bbWeldstiff1_l1Model = self.bbWeldstiff1_l1.create_model()
        self.bbWeldstiff1_l2Model = self.bbWeldstiff1_l2.create_model()

        self.bbWeldstiff2_u1Model = self.bbWeldstiff2_u1.create_model()
        self.bbWeldstiff2_u2Model = self.bbWeldstiff2_u2.create_model()
        self.bbWeldstiff2_l1Model = self.bbWeldstiff2_l1.create_model()
        self.bbWeldstiff2_l2Model = self.bbWeldstiff2_l2.create_model()

        self.bbWeldstiff3_u1Model = self.bbWeldstiff3_u1.create_model()
        self.bbWeldstiff3_u2Model = self.bbWeldstiff3_u2.create_model()
        self.bbWeldstiff3_l1Model = self.bbWeldstiff3_l1.create_model()
        self.bbWeldstiff3_l2Model = self.bbWeldstiff3_l2.create_model()

        self.bbWeldstiff4_u1Model = self.bbWeldstiff4_u1.create_model()
        self.bbWeldstiff4_u2Model = self.bbWeldstiff4_u2.create_model()
        self.bbWeldstiff4_l1Model = self.bbWeldstiff4_l1.create_model()
        self.bbWeldstiff4_l2Model = self.bbWeldstiff4_l2.create_model()


#############################################################################################################
#   Following functions takes inputs as origin, u direction and w direction of concerned component to place #
#   same component at appropriate place                                                                     #
#############################################################################################################

    def createBeamLGeometry(self):
        '''
        initialise the location of the left beam by defining the local origin of the component with respect to global origin
        '''
        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamRGeometry(self):
        '''
        initialise the location of the right beam by defining the local origin of the component with respect to global origin
        '''
        gap = self.beamRight.length + 2 * self.plateRight.T
        beamOriginR = numpy.array([0.0, gap, 0.0])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateLGeometry(self):
        '''
        initialise the location of the left plate by defining the local origin of the component with respect to global origin
        '''

        if self.module.endplate_type == 'Extended One Way - Irreversible Moment':
            plateOriginL = numpy.array([-self.plateLeft.W/2, self.beamRight.length + 0.5 * self.plateLeft.T, (self.plateRight.L / 2 - self.boltProjection - self.beamRight.D / 2)])
            plateL_uDir = numpy.array([0.0, 1.0, 0.0])    #TODO: self.boltProjection
            plateL_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateLeft.place(plateOriginL, plateL_uDir, plateL_wDir)

        else:
            plateOriginL = numpy.array([-self.plateLeft.W / 2, self.beamRight.length + 0.5 * self.plateLeft.T, 0.0])
            plateL_uDir = numpy.array([0.0, 1.0, 0.0])
            plateL_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateLeft.place(plateOriginL, plateL_uDir, plateL_wDir)

    def createPlateRGeometry(self):
        '''
        initialise the location of the right plate by defining the local origin of the component with respect to global origin
        '''

        if self.module.endplate_type == 'Extended One Way - Irreversible Moment':
            gap = 1.5 * self.plateRight.T + self.beamLeft.length
            plateOriginR = numpy.array([-self.plateRight.W/2, gap, (self.plateRight.L / 2 - self.boltProjection - self.beamRight.D / 2)])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

        else:
            gap = 1.5 * self.plateRight.T + self.beamLeft.length
            plateOriginR = numpy.array([-self.plateRight.W / 2, gap, 0.0])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

    def create_nut_bolt_array(self):
        '''
        initialise the location of the bolt group (top flange) by defining the local origin of the component with respect to global origin
        '''
        nutboltArrayOrigin = self.plateLeft.sec_origin + numpy.array([0.0, -0.5 * self.plateLeft.T, self.plateLeft.L/2])
        gaugeDir = numpy.array([1.0, 0, 0])
        pitchDir = numpy.array([0, 0, -1.0])
        boltDir = numpy.array([0, 1.0, 0])
        self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    def createbeam_stiffenersGeometry(self):
        '''
        initialise the location of the top and bottom stiffeners by defining the local origin of the component with respect to global origin
        '''
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_1.L / 2
        stiffenerOrigin1 = numpy.array([-self.beam_stiffener_1.T / 2, gap,
                                         self.beamRight.D / 2 + self.beam_stiffener_1.W / 2])
        stiffener1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_1.place(stiffenerOrigin1, stiffener1_uDir, stiffener1_wDir)

        gap = self.beamLeft.length + self.plateLeft.T +  self.plateRight.T+ self.beam_stiffener_1.L / 2
        stiffenerOrigin2 = numpy.array([self.beam_stiffener_1.T / 2, gap,
                                         - self.beamRight.D / 2 - self.beam_stiffener_1.W / 2])
        stiffener2_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener2_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_2.place(stiffenerOrigin2, stiffener2_uDir, stiffener2_wDir)

        gap = self.beamLeft.length - self.beam_stiffener_1.L / 2
        stiffenerOrigin3 = numpy.array([self.beam_stiffener_1.T / 2, gap,
                                         self.beamRight.D / 2 + self.beam_stiffener_1.W / 2])
        stiffener3_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener3_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_3.place(stiffenerOrigin3, stiffener3_uDir, stiffener3_wDir)

        gap = self.beamLeft.length - self.beam_stiffener_1.L / 2
        stiffenerOrigin4 = numpy.array([-self.beam_stiffener_1.T / 2, gap,
                                         - self.beamRight.D / 2 - self.beam_stiffener_1.W / 2])
        stiffener4_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener4_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_4.place(stiffenerOrigin4, stiffener4_uDir, stiffener4_wDir)

    def createbeam_stiffenerFlushGeometry(self):
        '''
        initialise the location of the side stiffeners by defining the local origin of the component with respect to global origin
        '''
        gap = self.beamLeft.length - self.beam_stiffener_F1.L / 2
        stiffenerOriginF1 = numpy.array([-self.beam_stiffener_F1.W/2 - self.beamLeft.t/2, gap,
                                         self.beamRight.D / 2 - self.loc])
        stiffenerF1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffenerF1_wDir = numpy.array([0.0, 0.0, -1.0])
        self.beam_stiffener_F1.place(stiffenerOriginF1, stiffenerF1_uDir, stiffenerF1_wDir)

        gap = self.beamLeft.length - self.beam_stiffener_F2.L / 2
        stiffenerOriginF2 = numpy.array([self.beam_stiffener_F2.W/2 + self.beamLeft.t/2 , gap,
                                         self.beamRight.D / 2 -self.beam_stiffener_2.T - self.loc])
        stiffenerF2_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffenerF2_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beam_stiffener_F2.place(stiffenerOriginF2, stiffenerF2_uDir, stiffenerF2_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L / 2
        stiffenerOriginF3 = numpy.array([-(self.beam_stiffener_F3.W/2 + self.beamRight.t/2), gap,
                                         self.beamRight.D / 2 -self.beam_stiffener_F3.T- self.loc])
        stiffenerF3_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffenerF3_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beam_stiffener_F3.place(stiffenerOriginF3, stiffenerF3_uDir, stiffenerF3_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F4.L / 2
        stiffenerOriginF4 = numpy.array([(self.beam_stiffener_F4.W/2 + self.beamRight.t/2), gap,
                                         self.beamRight.D / 2 - self.loc])
        stiffenerF4_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffenerF4_wDir = numpy.array([0.0, 0.0, -1.0])
        self.beam_stiffener_F4.place(stiffenerOriginF4, stiffenerF4_uDir, stiffenerF4_wDir)

    def create_bbWeldAbvFlang(self):
        '''
        initialise the location of the top flange weld by defining the local origin of the component with respect to global origin
        '''
        weldAbvFlangOrigin_11 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length, self.beamLeft.D / 2])
        uDirAbv_11 = numpy.array([0, -1.0, 0])
        wDirAbv_11 = numpy.array([-1.0, 0, 0])
        self.bbWeldAbvFlang_11.place(weldAbvFlangOrigin_11, uDirAbv_11, wDirAbv_11)

        weldAbvFlangOrigin_12 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length, -self.beamLeft.D / 2])
        uDirAbv_12 = numpy.array([0, -1.0, 0])
        wDirAbv_12 = numpy.array([1.0, 0, 0])
        self.bbWeldAbvFlang_12.place(weldAbvFlangOrigin_12, uDirAbv_12, wDirAbv_12)

        weldAbvFlangOrigin_21 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, self.beamLeft.D / 2])
        uDirAbv_21 = numpy.array([0, 1.0, 0])
        wDirAbv_21 = numpy.array([1.0, 0, 0])
        self.bbWeldAbvFlang_21.place(weldAbvFlangOrigin_21, uDirAbv_21, wDirAbv_21)

        weldAbvFlangOrigin_22 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, -self.beamLeft.D / 2])
        uDirAbv_22 = numpy.array([0, 1.0, 0])
        wDirAbv_22 = numpy.array([-1.0, 0, 0])
        self.bbWeldAbvFlang_22.place(weldAbvFlangOrigin_22, uDirAbv_22, wDirAbv_22)

    def create_bbWeldBelwFlang(self):
        '''
        initialise the location of the bottom flange weld by defining the local origin of the component with respect to global origin
        '''
        weldBelwFlangOrigin_11 = numpy.array([self.beamLeft.R2 -self.beamLeft.B / 2, self.beamLeft.length, (self.beamLeft.D / 2) - self.beamLeft.T])
        uDirBelw_11 = numpy.array([0, -1.0, 0])
        wDirBelw_11 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_11.place(weldBelwFlangOrigin_11, uDirBelw_11, wDirBelw_11)

        weldBelwFlangOrigin_12 = numpy.array([self.beamLeft.R1 + self.beamLeft.t / 2, self.beamLeft.length, (self.beamLeft.D / 2) - self.beamLeft.T])
        uDirBelw_12 = numpy.array([0, -1.0, 0])
        wDirBelw_12 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_12.place(weldBelwFlangOrigin_12, uDirBelw_12, wDirBelw_12)

        weldBelwFlangOrigin_13 = numpy.array([-self.beamLeft.R1-self.beamLeft.t / 2, self.beamLeft.length, -(self.beamLeft.D / 2) + self.beamLeft.T])
        uDirBelw_13 = numpy.array([0, -1.0, 0])
        wDirBelw_13 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_13.place(weldBelwFlangOrigin_13, uDirBelw_13, wDirBelw_13)

        weldBelwFlangOrigin_14 = numpy.array([-self.beamLeft.R2+self.beamLeft.B / 2, self.beamLeft.length, -(self.beamLeft.D / 2) + self.beamLeft.T])
        uDirBelw_14 = numpy.array([0, -1.0, 0])
        wDirBelw_14 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_14.place(weldBelwFlangOrigin_14, uDirBelw_14, wDirBelw_14)

        weldBelwFlangOrigin_21 = numpy.array([-self.beamLeft.R1-self.beamLeft.t / 2, self.beamLeft.length + 2 * self.plateLeft.T, (self.beamLeft.D / 2) -
                                              self.beamLeft.T])
        uDirBelw_21 = numpy.array([0, 1.0, 0])
        wDirBelw_21 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_21.place(weldBelwFlangOrigin_21, uDirBelw_21, wDirBelw_21)

        weldBelwFlangOrigin_22 = numpy.array([-self.beamLeft.R2+self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, (self.beamLeft.D / 2) -
                                              self.beamLeft.T])
        uDirBelw_22 = numpy.array([0, 1.0, 0])
        wDirBelw_22 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_22.place(weldBelwFlangOrigin_22, uDirBelw_22, wDirBelw_22)

        weldBelwFlangOrigin_23 = numpy.array([self.beamLeft.R2-self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, -(self.beamLeft.D / 2) +
                                              self.beamLeft.T])
        uDirBelw_23 = numpy.array([0, 1.0, 0])
        wDirBelw_23 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_23.place(weldBelwFlangOrigin_23, uDirBelw_23, wDirBelw_23)

        weldBelwFlangOrigin_24 = numpy.array([self.beamLeft.R1+self.beamLeft.t / 2, self.beamLeft.length + 2 * self.plateLeft.T, -(self.beamLeft.D / 2) +
                                              self.beamLeft.T])
        uDirBelw_24 = numpy.array([0, 1.0, 0])
        wDirBelw_24 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_24.place(weldBelwFlangOrigin_24, uDirBelw_24, wDirBelw_24)

    def create_bbWeldSideWeb(self):
        '''
        initialise the location of the web weld by defining the local origin of the component with respect to global origin
        '''
        weldSideWebOrigin_11 = numpy.array([-self.beamLeft.t/2, self.beamLeft.length, self.bbWeldSideWeb_21.L / 2])
        uDirWeb_11 = numpy.array([0, -1.0, 0])
        wDirWeb_11 = numpy.array([0, 0, -1.0])
        self.bbWeldSideWeb_11.place(weldSideWebOrigin_11, uDirWeb_11, wDirWeb_11)

        weldSideWebOrigin_12 = numpy.array([self.beamLeft.t / 2, self.beamLeft.length, -self.bbWeldSideWeb_21.L / 2])
        uDirWeb_12 = numpy.array([0, -1.0, 0])
        wDirWeb_12 = numpy.array([0, 0, 1.0])
        self.bbWeldSideWeb_12.place(weldSideWebOrigin_12, uDirWeb_12, wDirWeb_12)

        weldSideWebOrigin_21 = numpy.array([-self.beamLeft.t / 2, self.beamLeft.length + 2 * self.plateLeft.T, -self.bbWeldSideWeb_21.L / 2])
        uDirWeb_21 = numpy.array([0, 1.0, 0])
        wDirWeb_21 = numpy.array([0, 0, 1.0])
        self.bbWeldSideWeb_21.place(weldSideWebOrigin_21, uDirWeb_21, wDirWeb_21)

        weldSideWebOrigin_22 = numpy.array([self.beamLeft.t / 2, self.beamLeft.length + 2 * self.plateLeft.T, self.bbWeldSideWeb_21.L / 2])
        uDirWeb_22 = numpy.array([0, 1.0, 0])
        wDirWeb_22 = numpy.array([0, 0, -1.0])
        self.bbWeldSideWeb_22.place(weldSideWebOrigin_22, uDirWeb_22, wDirWeb_22)

    def create_bbWeldFlushstiffHeight(self):
        '''
        initialise the location of the side stiffener weld along the height by defining the local origin of the component with respect to global origin
        '''
        gap = self.beamLeft.length
        stiffenerOrigin1_u1 = numpy.array([-self.beam_stiffener_F1.L22 - self.beamLeft.t / 2, gap,
                                         self.beamRight.D / 2 - self.loc])
        stiffener1_u1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff1_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

        gap = self.beamLeft.length
        stiffenerOrigin1_l1 = numpy.array([-self.beam_stiffener_F1.W - self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff1_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

        gap = self.beamLeft.length
        stiffenerOrigin1_u1 = numpy.array([(self.beam_stiffener_F1.W + self.beamLeft.t / 2), gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff2_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

        gap = self.beamLeft.length
        stiffenerOrigin1_l1 = numpy.array([(self.beam_stiffener_F1.L22 + self.beamLeft.t / 2), gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff2_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T
        stiffenerOrigin1_u1 = numpy.array([-self.beam_stiffener_F1.W - self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff3_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T
        stiffenerOrigin1_l1 = numpy.array([-self.beam_stiffener_F1.L22 - self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff3_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T
        stiffenerOrigin1_u1 = numpy.array([self.beam_stiffener_F1.L22 + self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff4_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T
        stiffenerOrigin1_l1 = numpy.array([self.beam_stiffener_F1.W + self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff4_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)


    def create_bbWeldFlushstiffLength(self):
        '''
        initialise the location of the side stiffener weld along the length by defining the local origin of the component with respect to global origin
        '''

        gap = self.beamLeft.length - self.beam_stiffener_F1.L
        stiffenerOrigin1_u2 = numpy.array([-self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff1_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

        gap = self.beamLeft.length - self.beam_stiffener_F1.L22
        stiffenerOrigin1_l2 = numpy.array([-self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff1_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)

        gap = self.beamLeft.length - self.beam_stiffener_F1.L
        stiffenerOrigin1_u2 = numpy.array([self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u2_uDir = numpy.array([0.0, 0.0, 1.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff2_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

        gap = self.beamLeft.length - self.beam_stiffener_F1.L22
        stiffenerOrigin1_l2 = numpy.array([self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l2_uDir = numpy.array([0.0, 0.0, -1.0])
        stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff2_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L22
        stiffenerOrigin1_u2 = numpy.array([-self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff3_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L
        stiffenerOrigin3_l2 = numpy.array([-self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener3_l2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener3_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff3_l2.place(stiffenerOrigin3_l2, stiffener3_l2_uDir, stiffener3_l2_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L22
        stiffenerOrigin1_u2 = numpy.array([self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u2_uDir = numpy.array([0.0, 0.0, 1.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff4_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L
        stiffenerOrigin1_l2 = numpy.array([self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l2_uDir = numpy.array([0.0, 0.0, -1.0])
        stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff4_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)


    ################################################# Welding Beam Stiffeners ###################################################


    def create_bbWeldStiffHeight(self):
        '''
        initialise the location of the stiffener weld along the height by defining the local origin of the component with respect to global origin
        '''
        weldstiffOriginH_1 = numpy.array([-self.beam_stiffener_1.T/2, self.beamLeft.length , self.beamLeft.D/2 + self.beam_stiffener_1.W ])
        uDirstiffH_1 = numpy.array([0, -1.0, 0])
        wDirstiffH_1 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHL_1.place(weldstiffOriginH_1, uDirstiffH_1, wDirstiffH_1)

        weldstiffOriginH_2 = numpy.array(
            [self.beam_stiffener_2.T / 2, self.beamLeft.length, -(self.beamLeft.D / 2 + self.beam_stiffener_3.W)])
        uDirstiffH_2 = numpy.array([0, -1.0, 0])
        wDirstiffH_2 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHL_2.place(weldstiffOriginH_2, uDirstiffH_2, wDirstiffH_2)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T
        weldstiffOriginH_3 = numpy.array(
            [self.beam_stiffener_3.T / 2, gap, self.beamLeft.D / 2 + self.beam_stiffener_3.W])
        uDirstiffH_3 = numpy.array([0, 1.0, 0])
        wDirstiffH_3 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHL_3.place(weldstiffOriginH_3, uDirstiffH_3, wDirstiffH_3)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T
        weldstiffOriginH_4 = numpy.array(
            [-self.beam_stiffener_3.T / 2, gap, -(self.beamLeft.D / 2 + self.beam_stiffener_4.W)])
        uDirstiffH_4 = numpy.array([0, 1.0, 0])
        wDirstiffH_4 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHL_4.place(weldstiffOriginH_4, uDirstiffH_4, wDirstiffH_4)

        weldstiffOriginH_1 = numpy.array(
            [self.beam_stiffener_1.T / 2, self.beamLeft.length, self.beamLeft.D / 2 + self.beam_stiffener_1.L21])
        uDirstiffH_1 = numpy.array([0, -1.0, 0])
        wDirstiffH_1 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHR_1.place(weldstiffOriginH_1, uDirstiffH_1, wDirstiffH_1)

        weldstiffOriginH_2 = numpy.array(
            [-self.beam_stiffener_2.T / 2, self.beamLeft.length, -(self.beamLeft.D / 2 + self.beam_stiffener_2.L21)])
        uDirstiffH_2 = numpy.array([0, -1.0, 0])
        wDirstiffH_2 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHR_2.place(weldstiffOriginH_2, uDirstiffH_2, wDirstiffH_2)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T
        weldstiffOriginH_3 = numpy.array(
            [-self.beam_stiffener_3.T / 2, gap, self.beamLeft.D / 2 + self.beam_stiffener_3.L21])
        uDirstiffH_3 = numpy.array([0, 1.0, 0])
        wDirstiffH_3 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHR_3.place(weldstiffOriginH_3, uDirstiffH_3, wDirstiffH_3)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T
        weldstiffOriginH_4 = numpy.array(
            [self.beam_stiffener_4.T / 2, gap, -(self.beamLeft.D / 2 + self.beam_stiffener_4.L21)])
        uDirstiffH_4 = numpy.array([0, 1.0, 0])
        wDirstiffH_4 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHR_4.place(weldstiffOriginH_4, uDirstiffH_4, wDirstiffH_4)

    def create_bbWeldStiffLength(self):
        '''
        initialise the location of the stiffener weld along the length by defining the local origin of the component with respect to global origin
        '''
        weldstiffOriginL_1 = numpy.array([-self.beam_stiffener_1.T/2, self.beamLeft.length - self.beam_stiffener_1.L22, self.beamLeft.D/2])
        uDirstiffL_1 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_1 = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldStiffLL_1.place(weldstiffOriginL_1, uDirstiffL_1, wDirstiffL_1)

        weldstiffOriginL_2 = numpy.array(
            [self.beamLeft.t / 2, self.beamLeft.length - self.beam_stiffener_1.L22, -self.beamLeft.D / 2])
        uDirstiffL_2 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_2 = numpy.array([0, -1.0, 0.0])
        self.bbWeldStiffLL_2.place(weldstiffOriginL_2, uDirstiffL_2, wDirstiffL_2)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22 + self.bbWeldStiffLL_3.L
        weldstiffOriginL_3 = numpy.array([-self.beam_stiffener_3.T / 2, gap, self.beamLeft.D / 2])
        uDirstiffL_3 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_3 = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldStiffLL_3.place(weldstiffOriginL_3, uDirstiffL_3, wDirstiffL_3)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22 + self.bbWeldStiffLL_3.L
        weldstiffOriginL_4 = numpy.array([self.beamLeft.t / 2, gap, -self.beamLeft.D / 2])
        uDirstiffL_4 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_4 = numpy.array([0, -1.0, 0.0])
        self.bbWeldStiffLL_4.place(weldstiffOriginL_4, uDirstiffL_4, wDirstiffL_4)

        weldstiffOriginL_1 = numpy.array(
            [self.beamLeft.t / 2, self.beamLeft.length - self.beam_stiffener_2.L, self.beamLeft.D / 2])
        uDirstiffL_1 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldStiffLR_1.place(weldstiffOriginL_1, uDirstiffL_1, wDirstiffL_1)

        weldstiffOriginL_2 = numpy.array(
            [-self.beam_stiffener_2.T / 2, self.beamLeft.length - self.beam_stiffener_2.L, -self.beamLeft.D / 2])
        uDirstiffL_2 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_2 = numpy.array([0, 1.0, 0.0])
        self.bbWeldStiffLR_2.place(weldstiffOriginL_2, uDirstiffL_2, wDirstiffL_2)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22
        weldstiffOriginL_3 = numpy.array([self.beamLeft.t / 2, gap, self.beamLeft.D / 2])
        uDirstiffL_3 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_3 = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldStiffLR_3.place(weldstiffOriginL_3, uDirstiffL_3, wDirstiffL_3)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22
        weldstiffOriginL_4 = numpy.array([-self.beamLeft.t / 2, gap, -self.beamLeft.D / 2])
        uDirstiffL_4 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_4 = numpy.array([0, 1.0, 0.0])
        self.bbWeldStiffLR_4.place(weldstiffOriginL_4, uDirstiffL_4, wDirstiffL_4)


#############################################################################################################
#   Following functions returns the CAD model to the function display_3DModel of main file                  #
#############################################################################################################


    def get_beam_models(self):
        """

        :return: CAD model of both left and right beam
        """

        beams = BRepAlgoAPI_Fuse(self.beamLModel, self.beamRModel).Shape()
        return beams

    def get_plate_connector_models(self):
        """

        :return: CAD model of extended end plate and stiffeners
        """

        if self.module.endplate_type == 'Extended One Way - Irreversible Moment':
            connector_plate = [self.plateLModel, self.plateRModel, self.beam_stiffener_1Model,
                    self.beam_stiffener_3Model]

        elif self.module.endplate_type == 'Extended Both Ways - Reversible Moment':
            connector_plate = [self.plateLModel, self.plateRModel,  self.beam_stiffener_1Model,
                    self.beam_stiffener_2Model, self.beam_stiffener_3Model,
                    self.beam_stiffener_4Model]

        elif self.module.endplate_type == 'Flushed - Reversible Moment':
            connector_plate = [self.plateLModel, self.plateRModel, self.beam_stiffener_F1Model, self.beam_stiffener_F2Model,
                    self.beam_stiffener_F3Model,self.beam_stiffener_F4Model]

        plates = connector_plate[0]
        for comp in connector_plate[1:]:
            plates = BRepAlgoAPI_Fuse(comp, plates).Shape()

        return plates

    def get_welded_models(self):
        """

        :return: CAD model for all the welds
        """

        if self.module.endplate_type == 'Extended One Way - Irreversible Moment':
            welded_sec = [self.bbWeldAbvFlang_11Model, self.bbWeldAbvFlang_12Model,
                    self.bbWeldAbvFlang_21Model,
                    self.bbWeldAbvFlang_22Model,
                    self.bbWeldBelwFlang_11Model, self.bbWeldBelwFlang_12Model, self.bbWeldBelwFlang_13Model,
                    self.bbWeldBelwFlang_14Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_11Model, self.bbWeldSideWeb_12Model, self.bbWeldSideWeb_21Model,
                    self.bbWeldSideWeb_22Model, self.bbWeldStiffHL_1Model,
                    self.bbWeldStiffLL_1Model, self.bbWeldStiffHL_3Model, self.bbWeldStiffLL_3Model,
                     self.bbWeldStiffHR_1Model,
                    self.bbWeldStiffLR_1Model, self.bbWeldStiffHR_3Model,
                    self.bbWeldStiffLR_3Model]

        elif self.module.endplate_type == 'Extended Both Ways - Reversible Moment':
            welded_sec = [self.bbWeldAbvFlang_11Model, self.bbWeldAbvFlang_12Model,
                    self.bbWeldAbvFlang_21Model,
                    self.bbWeldAbvFlang_22Model,
                    self.bbWeldBelwFlang_11Model, self.bbWeldBelwFlang_12Model, self.bbWeldBelwFlang_13Model,
                    self.bbWeldBelwFlang_14Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_11Model, self.bbWeldSideWeb_12Model, self.bbWeldSideWeb_21Model,
                    self.bbWeldSideWeb_22Model, self.bbWeldStiffHL_1Model,
                    self.bbWeldStiffLL_1Model, self.bbWeldStiffHL_3Model, self.bbWeldStiffLL_3Model,
                    self.bbWeldStiffHL_2Model, self.bbWeldStiffLL_2Model,
                    self.bbWeldStiffHL_4Model, self.bbWeldStiffLL_4Model, self.bbWeldStiffHR_1Model,
                    self.bbWeldStiffLR_1Model, self.bbWeldStiffHR_3Model,
                    self.bbWeldStiffLR_3Model, self.bbWeldStiffHR_2Model, self.bbWeldStiffLR_2Model,
                    self.bbWeldStiffHR_4Model, self.bbWeldStiffLR_4Model]

        elif self.module.endplate_type == 'Flushed - Reversible Moment':
            welded_sec = [self.bbWeldAbvFlang_11Model, self.bbWeldAbvFlang_12Model,
                    self.bbWeldAbvFlang_21Model,
                    self.bbWeldAbvFlang_22Model,
                    self.bbWeldBelwFlang_11Model, self.bbWeldBelwFlang_12Model, self.bbWeldBelwFlang_13Model,
                    self.bbWeldBelwFlang_14Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_11Model, self.bbWeldSideWeb_12Model, self.bbWeldSideWeb_21Model,
                    self.bbWeldSideWeb_22Model,
                    self.bbWeldstiff1_u1Model, self.bbWeldstiff1_u2Model, self.bbWeldstiff1_l1Model,
                    self.bbWeldstiff1_l2Model, self.bbWeldstiff2_u1Model,
                    self.bbWeldstiff2_u2Model, self.bbWeldstiff2_l1Model, self.bbWeldstiff2_l2Model,
                    self.bbWeldstiff3_u1Model, self.bbWeldstiff3_u2Model,
                    self.bbWeldstiff3_l1Model, self.bbWeldstiff3_l2Model, self.bbWeldstiff4_u1Model,
                    self.bbWeldstiff4_u2Model, self.bbWeldstiff4_l1Model,
                    self.bbWeldstiff4_l2Model]

        welds = welded_sec[0]
        for comp in welded_sec[1:]:
            welds = BRepAlgoAPI_Fuse(comp, welds).Shape()

        return welds

    def get_nut_bolt_array_models(self):
        """

        :return: CAD model for nut bolt array
        """

        nut_bolts = self.nut_bolt_array.get_models()
        array = nut_bolts[0]
        for comp in nut_bolts:
            array = BRepAlgoAPI_Fuse(comp, array).Shape()

        return array

    def get_connector_models(self):
        """

        :return: CAD models of the connecting components
        """

        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()

        CAD_list = [plate_connectors, welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD

    def get_models(self):
        """

        :return: complete CAD model
        """

        beams = self.get_beam_models()
        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()

        CAD_list = [beams, plate_connectors, welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD


class CADGroove(object):

    def __init__(self, module, beamLeft, beamRight, plateLeft, plateRight, nut_bolt_array,bbWeldFlang, bbWeldWeb,beam_stiffeners,beam_stiffenerFlush, bbWeldStiffHeight,bbWeldStiffLength,bbWeldFlushstiffHeight, bbWeldFlushstiffLength):
        """

        :param beamLeft: Left beam
        :param beamRight: Right beam
        :param plateLeft: Plate welded to left beam
        :param plateRight: Plate welded to Right beam
        :param nut_bolt_array: Bolt placement on the end plates
        :param bbWeldFlang: Welded surface connecting beam flange to the plate
        :param bbWeldWeb:  Welded surface connecting beam web to the plate
        :param bbWeldStiffHeight: Weld surface along the height of the stiffeners for the extended and one-way end plate type
        :param bbWeldStiffLength: Weld surface along the length of the stiffeners for the extended and one-way end plate type
        :param bbWeldFlushstiffHeight: Weld surface along the height of the stiffeners for the flush end plate type
        :param bbWeldFlushstiffLength: Weld surface along the length of the stiffeners for the flush end plate type
        :param beam_stiffeners: Stiffeners for the enxtended and one-way endplate
        :param beam_stiffenerFlush: Stiffeners for the flush endplate
        :param alist: Input dictionary
        :param outputobj: Output dictionary
        """

        self.beamLeft = beamLeft
        self.beamRight = beamRight
        self.plateLeft = plateLeft
        self.plateRight = plateRight
        self.nut_bolt_array = nut_bolt_array
        self.beamLModel = None
        self.beamRModel = None
        self.plateLModel = None
        self.plateRModel = None
        self.beam_stiffener_1 = beam_stiffeners
        self.beam_stiffener_2 = copy.deepcopy(beam_stiffeners)
        self.beam_stiffener_3 = copy.deepcopy(beam_stiffeners)
        self.beam_stiffener_4 = copy.deepcopy(beam_stiffeners)
        self.module = module

        #flush stiffener#
        # self.beam_stiffener_F1 = beam_stiffenerFlush
        # self.beam_stiffener_F2 = copy.deepcopy(beam_stiffenerFlush)
        # self.beam_stiffener_F3 = copy.deepcopy(beam_stiffenerFlush)
        # self.beam_stiffener_F4 = copy.deepcopy(beam_stiffenerFlush)
        # self.beam_stiffener_F5 = copy.deepcopy(beam_stiffenerFlush)
        # self.beam_stiffener_F6 = copy.deepcopy(beam_stiffenerFlush)
        # self.beam_stiffener_F7 = copy.deepcopy(beam_stiffenerFlush)
        # self.beam_stiffener_F8 = copy.deepcopy(beam_stiffenerFlush)

        self.plateProjection = self.module.projection
        if self.module.endplate_type == 'Flushed - Reversible Moment' and self.module.bolt_row_web ==0:
            self.loc1 = float(self.module.beam_D/2 - self.module.stiffener_thickness/2)
            self.loc2 = None
        else:
            self.loc1 = float(self.module.beam_D / 2 - self.module.stiffener_thickness / 2 - self.module.pitch_distance_web/2)
            self.loc2 = float(self.module.beam_D / 2 - self.module.stiffener_thickness / 2 + self.module.pitch_distance_web/2)
        self.bbWeldFlang_R1 = bbWeldFlang
        self.bbWeldFlang_R2 = copy.deepcopy(bbWeldFlang)
        self.bbWeldFlang_L1 = copy.deepcopy(bbWeldFlang)
        self.bbWeldFlang_L2 = copy.deepcopy(bbWeldFlang)
        self.bbWeldWeb_R3 =  bbWeldWeb
        self.bbWeldWeb_L3 = copy.deepcopy(bbWeldWeb)
        #


        #Fillet weld

        self.bbWeldStiffHL_1 = bbWeldStiffHeight
        self.bbWeldStiffHL_2 = copy.deepcopy(bbWeldStiffHeight)
        self.bbWeldStiffHL_3 = copy.deepcopy(bbWeldStiffHeight)
        self.bbWeldStiffHL_4 = copy.deepcopy(bbWeldStiffHeight)
        self.bbWeldStiffHR_1 = copy.deepcopy(bbWeldStiffHeight)
        self.bbWeldStiffHR_2 = copy.deepcopy(bbWeldStiffHeight)
        self.bbWeldStiffHR_3 = copy.deepcopy(bbWeldStiffHeight)
        self.bbWeldStiffHR_4 = copy.deepcopy(bbWeldStiffHeight)

        self.bbWeldStiffLL_1 = bbWeldStiffLength
        self.bbWeldStiffLL_2 = copy.deepcopy(bbWeldStiffLength)
        self.bbWeldStiffLL_3 = copy.deepcopy(bbWeldStiffLength)
        self.bbWeldStiffLL_4 = copy.deepcopy(bbWeldStiffLength)
        self.bbWeldStiffLR_1 = copy.deepcopy(bbWeldStiffLength)
        self.bbWeldStiffLR_2 = copy.deepcopy(bbWeldStiffLength)
        self.bbWeldStiffLR_3 = copy.deepcopy(bbWeldStiffLength)
        self.bbWeldStiffLR_4 = copy.deepcopy(bbWeldStiffLength)
        #
        self.bbWeldstiff1_u1 = bbWeldFlushstiffHeight
        self.bbWeldstiff1_l1 = copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff2_u1 = copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff2_l1 = copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff3_u1 = copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff3_l1 = copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff4_u1 = copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff4_l1 = copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff5_u1 = bbWeldFlushstiffHeight
        self.bbWeldstiff5_l1 = copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff6_u1 = copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff6_l1 = copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff7_u1 = copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff7_l1 = copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff8_u1 = copy.deepcopy(bbWeldFlushstiffHeight)
        self.bbWeldstiff8_l1 = copy.deepcopy(bbWeldFlushstiffHeight)
        #
        self.bbWeldstiff1_u2 = bbWeldFlushstiffLength
        self.bbWeldstiff1_l2 = copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff2_u2 = copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff2_l2 = copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff3_u2 = copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff3_l2 = copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff4_u2 = copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff4_l2 = copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff5_u2 = bbWeldFlushstiffLength
        self.bbWeldstiff5_l2 = copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff6_u2 = copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff6_l2 = copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff7_u2 = copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff7_l2 = copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff8_u2 = copy.deepcopy(bbWeldFlushstiffLength)
        self.bbWeldstiff8_l2 = copy.deepcopy(bbWeldFlushstiffLength)

    def create_3DModel(self):
        """
        :return: CAD model of each entity such as Left beam, right beam, both end plates and so on
        """
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        self.createPlateLGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()

        self.createbeam_stiffenersGeometry()
        #
        # flush stiffener#
        # self.createbeam_stiffenerFlushGeometry()
        #
        self.create_bbWeldFlangGeometry()
        self.create_bbWeldWebGeometry()
        #
        # #Fillet weld
        self.create_bbWeldStiffHeight()
        self.create_bbWeldStiffLength()

        # flush stiffener#
        # self.create_bbWeldFlushstiffHeight()
        # self.create_bbWeldFlushstiffLength()


        # call for create_model of filletweld from Components directory
        self.beamLModel = self.beamLeft.create_model()
        self.beamRModel = self.beamRight.create_model()
        self.plateLModel = self.plateLeft.create_model()
        self.plateRModel = self.plateRight.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()

        self.beam_stiffener_1Model = self.beam_stiffener_1.create_model()
        self.beam_stiffener_2Model = self.beam_stiffener_2.create_model()
        self.beam_stiffener_3Model = self.beam_stiffener_3.create_model()
        self.beam_stiffener_4Model = self.beam_stiffener_4.create_model()

        # flush stiffener#
        # self.beam_stiffener_F1Model = self.beam_stiffener_F1.create_model()
        # self.beam_stiffener_F2Model = self.beam_stiffener_F2.create_model()
        # self.beam_stiffener_F3Model = self.beam_stiffener_F3.create_model()
        # self.beam_stiffener_F4Model = self.beam_stiffener_F4.create_model()
        # if self.loc2 != None:
        #     self.beam_stiffener_F5Model = self.beam_stiffener_F5.create_model()
        #     self.beam_stiffener_F6Model = self.beam_stiffener_F6.create_model()
        #     self.beam_stiffener_F7Model = self.beam_stiffener_F7.create_model()
        #     self.beam_stiffener_F8Model = self.beam_stiffener_F8.create_model()
        #
        self.bbWeldFlang_R1Model = self.bbWeldFlang_R1.create_model()
        self.bbWeldFlang_R2Model = self.bbWeldFlang_R2.create_model()
        self.bbWeldFlang_L1Model = self.bbWeldFlang_L1.create_model()
        self.bbWeldFlang_L2Model = self.bbWeldFlang_L2.create_model()
        self.bbWeldWeb_R3Model = self.bbWeldWeb_R3.create_model()
        self.bbWeldWeb_L3Model = self.bbWeldWeb_L3.create_model()
        #
        # #Fillet weld
        self.bbWeldStiffHL_1Model = self.bbWeldStiffHL_1.create_model()
        self.bbWeldStiffHL_2Model = self.bbWeldStiffHL_2.create_model()
        self.bbWeldStiffHL_3Model = self.bbWeldStiffHL_3.create_model()
        self.bbWeldStiffHL_4Model = self.bbWeldStiffHL_4.create_model()
        #
        self.bbWeldStiffLL_1Model = self.bbWeldStiffLL_1.create_model()
        self.bbWeldStiffLL_2Model = self.bbWeldStiffLL_2.create_model()
        self.bbWeldStiffLL_3Model = self.bbWeldStiffLL_3.create_model()
        self.bbWeldStiffLL_4Model = self.bbWeldStiffLL_4.create_model()
        self.bbWeldStiffHR_1Model = self.bbWeldStiffHR_1.create_model()
        self.bbWeldStiffHR_2Model = self.bbWeldStiffHR_2.create_model()
        self.bbWeldStiffHR_3Model = self.bbWeldStiffHR_3.create_model()
        self.bbWeldStiffHR_4Model = self.bbWeldStiffHR_4.create_model()
        #
        self.bbWeldStiffLR_1Model = self.bbWeldStiffLR_1.create_model()
        self.bbWeldStiffLR_2Model = self.bbWeldStiffLR_2.create_model()
        self.bbWeldStiffLR_3Model = self.bbWeldStiffLR_3.create_model()
        self.bbWeldStiffLR_4Model = self.bbWeldStiffLR_4.create_model()
        #
        #
        #
        # flush stiffener#
        # self.bbWeldstiff1_u1Model = self.bbWeldstiff1_u1.create_model()
        # self.bbWeldstiff1_u2Model = self.bbWeldstiff1_u2.create_model()
        # self.bbWeldstiff1_l1Model = self.bbWeldstiff1_l1.create_model()
        # self.bbWeldstiff1_l2Model = self.bbWeldstiff1_l2.create_model()
        # #
        # self.bbWeldstiff2_u1Model = self.bbWeldstiff2_u1.create_model()
        # self.bbWeldstiff2_u2Model = self.bbWeldstiff2_u2.create_model()
        # self.bbWeldstiff2_l1Model = self.bbWeldstiff2_l1.create_model()
        # self.bbWeldstiff2_l2Model = self.bbWeldstiff2_l2.create_model()
        # #
        # self.bbWeldstiff3_u1Model = self.bbWeldstiff3_u1.create_model()
        # self.bbWeldstiff3_u2Model = self.bbWeldstiff3_u2.create_model()
        # self.bbWeldstiff3_l1Model = self.bbWeldstiff3_l1.create_model()
        # self.bbWeldstiff3_l2Model = self.bbWeldstiff3_l2.create_model()
        # #
        # self.bbWeldstiff4_u1Model = self.bbWeldstiff4_u1.create_model()
        # self.bbWeldstiff4_u2Model = self.bbWeldstiff4_u2.create_model()
        # self.bbWeldstiff4_l1Model = self.bbWeldstiff4_l1.create_model()
        # self.bbWeldstiff4_l2Model = self.bbWeldstiff4_l2.create_model()
        # #
        # if self.loc2 != None:
        #     self.bbWeldstiff5_u1Model = self.bbWeldstiff5_u1.create_model()
        #     self.bbWeldstiff5_u2Model = self.bbWeldstiff5_u2.create_model()
        #     self.bbWeldstiff5_l1Model = self.bbWeldstiff5_l1.create_model()
        #     self.bbWeldstiff5_l2Model = self.bbWeldstiff5_l2.create_model()
        #     #
        #     self.bbWeldstiff6_u1Model = self.bbWeldstiff6_u1.create_model()
        #     self.bbWeldstiff6_u2Model = self.bbWeldstiff6_u2.create_model()
        #     self.bbWeldstiff6_l1Model = self.bbWeldstiff6_l1.create_model()
        #     self.bbWeldstiff6_l2Model = self.bbWeldstiff6_l2.create_model()
        #     #
        #     self.bbWeldstiff7_u1Model = self.bbWeldstiff7_u1.create_model()
        #     self.bbWeldstiff7_u2Model = self.bbWeldstiff7_u2.create_model()
        #     self.bbWeldstiff7_l1Model = self.bbWeldstiff7_l1.create_model()
        #     self.bbWeldstiff7_l2Model = self.bbWeldstiff7_l2.create_model()
        #     #
        #     self.bbWeldstiff8_u1Model = self.bbWeldstiff8_u1.create_model()
        #     self.bbWeldstiff8_u2Model = self.bbWeldstiff8_u2.create_model()
        #     self.bbWeldstiff8_l1Model = self.bbWeldstiff8_l1.create_model()
        #     self.bbWeldstiff8_l2Model = self.bbWeldstiff8_l2.create_model()



        #############################################################################################################
        #   Following functions takes inputs as origin, u direction and w direction of concerned component to place #
        #   same component at appropriate place                                                                     #
        #############################################################################################################

    def createBeamLGeometry(self):
        '''
        initialise the location of the left beam by defining the local origin of the component with respect to global origin
        '''
        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamRGeometry(self):
        '''
        initialise the location of the right beam by defining the local origin of the component with respect to global origin
        '''
        gap = self.beamRight.length + 2 * self.plateRight.T + 2* self.bbWeldWeb_L3.b
        beamOriginR = numpy.array([0.0, gap, 0.0])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateLGeometry(self):
        '''
        initialise the location of the left plate by defining the local origin of the component with respect to global origin
        '''

        if self.module.endplate_type == 'Extended One Way - Irreversible Moment':
            plateOriginL = numpy.array([-self.plateLeft.W / 2, self.beamRight.length + 0.5 * self.plateLeft.T + self.bbWeldWeb_L3.b,
                                        (self.plateRight.L / 2 - self.plateProjection - self.beamRight.D / 2)])
            plateL_uDir = numpy.array([0.0, 1.0, 0.0])  # TODO: self.plateProjection
            plateL_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateLeft.place(plateOriginL, plateL_uDir, plateL_wDir)

        else:
            plateOriginL = numpy.array([-self.plateLeft.W / 2, self.beamRight.length + 0.5 * self.plateLeft.T + self.bbWeldWeb_L3.b, 0.0])
            plateL_uDir = numpy.array([0.0, 1.0, 0.0])
            plateL_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateLeft.place(plateOriginL, plateL_uDir, plateL_wDir)

    def createPlateRGeometry(self):
        '''
        initialise the location of the right plate by defining the local origin of the component with respect to global origin
        '''

        if self.module.endplate_type == 'Extended One Way - Irreversible Moment':
            gap = 1.5 * self.plateRight.T + self.beamLeft.length + self.bbWeldWeb_L3.b
            plateOriginR = numpy.array(
                [-self.plateRight.W / 2, gap, (self.plateRight.L / 2 - self.plateProjection - self.beamRight.D / 2)])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

        else:
            gap = 1.5 * self.plateRight.T + self.beamLeft.length + self.bbWeldWeb_L3.b
            plateOriginR = numpy.array([-self.plateRight.W / 2, gap, 0.0])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

    def create_nut_bolt_array(self):
        '''
        initialise the location of the bolt group by defining the local origin of the bolt group with respect to global origin
        '''
        nutboltArrayOrigin = self.plateLeft.sec_origin + numpy.array([0.0, -0.5 * self.plateLeft.T, self.plateLeft.L / 2])
        gaugeDir = numpy.array([1.0, 0, 0])
        pitchDir = numpy.array([0, 0, -1.0])
        boltDir = numpy.array([0, 1.0, 0])
        self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    def createbeam_stiffenersGeometry(self):
        '''
        initialise the location of the top and bottom stiffener by defining the local origin of the bolt group with respect to global origin
        '''
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_1.L / 2 + self. bbWeldWeb_L3.b
        stiffenerOrigin1 = numpy.array([-self.beam_stiffener_1.T / 2, gap,
                                        self.beamRight.D / 2 + self.beam_stiffener_1.W / 2 ])
        stiffener1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_1.place(stiffenerOrigin1, stiffener1_uDir, stiffener1_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_1.L / 2 + self. bbWeldWeb_L3.b
        stiffenerOrigin2 = numpy.array([self.beam_stiffener_1.T / 2, gap,
                                        - self.beamRight.D / 2 - self.beam_stiffener_1.W / 2 ])
        stiffener2_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener2_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_2.place(stiffenerOrigin2, stiffener2_uDir, stiffener2_wDir)

        gap = self.beamLeft.length - self.beam_stiffener_1.L / 2 + self. bbWeldWeb_L3.b
        stiffenerOrigin3 = numpy.array([self.beam_stiffener_1.T / 2, gap,
                                        self.beamRight.D / 2 + self.beam_stiffener_1.W / 2 ])
        stiffener3_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener3_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_3.place(stiffenerOrigin3, stiffener3_uDir, stiffener3_wDir)

        gap = self.beamLeft.length - self.beam_stiffener_1.L / 2 + self. bbWeldWeb_L3.b
        stiffenerOrigin4 = numpy.array([-self.beam_stiffener_1.T / 2, gap,
                                        - self.beamRight.D / 2 - self.beam_stiffener_1.W / 2 ])
        stiffener4_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener4_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_4.place(stiffenerOrigin4, stiffener4_uDir, stiffener4_wDir)


    def createbeam_stiffenerFlushGeometry(self):
        '''
        initialise the location of the side stiffener by defining the local origin of the bolt group with respect to global origin
        '''

        gap = self.beamLeft.length - self.beam_stiffener_F1.L / 2 + self.bbWeldWeb_L3.b
        stiffenerOriginF1 = numpy.array([-self.beam_stiffener_F1.W/2 - self.beamLeft.t/2, gap,
                                         self.beamRight.D / 2 - self.loc1])
        stiffenerF1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffenerF1_wDir = numpy.array([0.0, 0.0, -1.0])
        self.beam_stiffener_F1.place(stiffenerOriginF1, stiffenerF1_uDir, stiffenerF1_wDir)

        gap = self.beamLeft.length - self.beam_stiffener_F2.L / 2 + self.bbWeldWeb_L3.b
        stiffenerOriginF2 = numpy.array([self.beam_stiffener_F2.W/2 + self.beamLeft.t/2 , gap,
                                         self.beamRight.D / 2 -self.beam_stiffener_2.T - self.loc1])
        stiffenerF2_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffenerF2_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beam_stiffener_F2.place(stiffenerOriginF2, stiffenerF2_uDir, stiffenerF2_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L / 2 +  self.bbWeldWeb_L3.b
        stiffenerOriginF3 = numpy.array([-(self.beam_stiffener_F3.W/2 + self.beamRight.t/2), gap,
                                         self.beamRight.D / 2 -self.beam_stiffener_F3.T- self.loc1])
        stiffenerF3_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffenerF3_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beam_stiffener_F3.place(stiffenerOriginF3, stiffenerF3_uDir, stiffenerF3_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F4.L / 2 +  self.bbWeldWeb_L3.b
        stiffenerOriginF4 = numpy.array([(self.beam_stiffener_F4.W/2 + self.beamRight.t/2), gap,
                                         self.beamRight.D / 2 - self.loc1])
        stiffenerF4_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffenerF4_wDir = numpy.array([0.0, 0.0, -1.0])
        self.beam_stiffener_F4.place(stiffenerOriginF4, stiffenerF4_uDir, stiffenerF4_wDir)

        if self.loc2 !=None:
            gap = self.beamLeft.length - self.beam_stiffener_F5.L / 2 + self.bbWeldWeb_L3.b
            stiffenerOriginF5 = numpy.array([-self.beam_stiffener_F5.W / 2 - self.beamLeft.t / 2, gap,
                                             self.beamRight.D / 2 - self.loc2])
            stiffenerF5_uDir = numpy.array([0.0, -1.0, 0.0])
            stiffenerF5_wDir = numpy.array([0.0, 0.0, -1.0])
            self.beam_stiffener_F5.place(stiffenerOriginF5, stiffenerF5_uDir, stiffenerF5_wDir)

            gap = self.beamLeft.length - self.beam_stiffener_F6.L / 2 + self.bbWeldWeb_L3.b
            stiffenerOriginF6 = numpy.array([self.beam_stiffener_F6.W / 2 + self.beamLeft.t / 2, gap,
                                             self.beamRight.D / 2 - self.beam_stiffener_2.T - self.loc2])
            stiffenerF6_uDir = numpy.array([0.0, -1.0, 0.0])
            stiffenerF6_wDir = numpy.array([0.0, 0.0, 1.0])
            self.beam_stiffener_F6.place(stiffenerOriginF6, stiffenerF6_uDir, stiffenerF6_wDir)

            gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F7.L / 2 + self.bbWeldWeb_L3.b
            stiffenerOriginF7 = numpy.array([-(self.beam_stiffener_F7.W / 2 + self.beamRight.t / 2), gap,
                                             self.beamRight.D / 2 - self.beam_stiffener_F7.T - self.loc2])
            stiffenerF7_uDir = numpy.array([0.0, 1.0, 0.0])
            stiffenerF7_wDir = numpy.array([0.0, 0.0, 1.0])
            self.beam_stiffener_F7.place(stiffenerOriginF7, stiffenerF7_uDir, stiffenerF7_wDir)

            gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F8.L / 2 + self.bbWeldWeb_L3.b
            stiffenerOriginF8 = numpy.array([(self.beam_stiffener_F8.W / 2 + self.beamRight.t / 2), gap,
                                             self.beamRight.D / 2 - self.loc2])
            stiffenerF8_uDir = numpy.array([0.0, 1.0, 0.0])
            stiffenerF8_wDir = numpy.array([0.0, 0.0, -1.0])
            self.beam_stiffener_F8.place(stiffenerOriginF8, stiffenerF8_uDir, stiffenerF8_wDir)


    ##############################################  creating weld sections ########################################

    def create_bbWeldFlangGeometry(self):
        '''
        initialise the location of the flange weld by defining the local origin of the bolt group with respect to global origin
        '''
        gap = self.beamLeft.length + self.bbWeldWeb_L3.b + self.plateLeft.T + self.plateRight.T  + self.bbWeldWeb_L3.b/2
        weldFlangOrigin_R1 = numpy.array([- self.beamLeft.B/2, gap, self.beamLeft.D/2 - self.beamLeft.T/2])
        uDir_1 = numpy.array([0, 1.0, 0])
        wDir_1 = numpy.array([1.0, 0, 0])
        self.bbWeldFlang_R1.place(weldFlangOrigin_R1, uDir_1, wDir_1)

        gap = self.beamLeft.length + self.bbWeldWeb_L3.b + self.plateLeft.T + self.plateRight.T  + self.bbWeldWeb_L3.b / 2
        weldFlangOrigin_R2 = numpy.array([self.beamLeft.B/2, gap, -(self.beamLeft.D/2 - self.beamLeft.T/2)])
        uDir_2 = numpy.array([0, 1.0, 0])
        wDir_2 = numpy.array([-1.0, 0, 0])
        self.bbWeldFlang_R2.place(weldFlangOrigin_R2, uDir_2, wDir_2)

        weldFlangOrigin_L1 = numpy.array([ - self.beamLeft.B/2 , self.beamLeft.length + self.bbWeldWeb_L3.b/2, self.beamLeft.D/2 - self.beamLeft.T/2])
        uDir_1 = numpy.array([0, 1.0, 0])
        wDir_1 = numpy.array([1.0, 0, 0])
        self.bbWeldFlang_L1.place(weldFlangOrigin_L1, uDir_1, wDir_1)

        weldFlangOrigin_L2 = numpy.array([self.beamLeft.B/2, self.beamLeft.length + self.bbWeldWeb_L3.b/2,-(self.beamLeft.D/2 - self.beamLeft.T/2)])
        uDir_2 = numpy.array([0, 1.0, 0])
        wDir_2 = numpy.array([-1.0, 0, 0])
        self.bbWeldFlang_L2.place(weldFlangOrigin_L2, uDir_2, wDir_2)

    def create_bbWeldWebGeometry(self):
        '''
        initialise the location of the web weld by defining the local origin of the bolt group with respect to global origin
        '''
        gap = self.beamLeft.length + self.bbWeldWeb_L3.b + self.plateLeft.T + self.plateRight.T  + self.bbWeldWeb_L3.b / 2
        weldWebOrigin_R3 = numpy.array([0.0, gap,-self.bbWeldWeb_L3.L/2])
        uDirWeb_3 = numpy.array([0, 1.0, 0])
        wDirWeb_3 = numpy.array([0, 0, 1.0])
        self.bbWeldWeb_R3.place(weldWebOrigin_R3, uDirWeb_3, wDirWeb_3)

        weldWebOrigin_L3 = numpy.array([0.0, self.beamLeft.length + self.bbWeldWeb_L3.b/2, -self.bbWeldWeb_L3.L/2])
        uDirWeb_3 = numpy.array([0, 1.0, 0])
        wDirWeb_3 = numpy.array([0, 0, 1.0])
        self.bbWeldWeb_L3.place(weldWebOrigin_L3, uDirWeb_3, wDirWeb_3)

    ################################################# Welding Beam Stiffeners ###################################################


    def create_bbWeldStiffHeight(self):
        '''
        initialise the location of the stiffener weld along the height by defining the local origin of the bolt group with respect to global origin
        '''
        weldstiffOriginH_1 = numpy.array([-self.beam_stiffener_1.T/2, self.beamLeft.length + self.bbWeldWeb_L3.b, self.beamLeft.D/2 + self.beam_stiffener_1.W ])
        uDirstiffH_1 = numpy.array([0, -1.0, 0])
        wDirstiffH_1 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHL_1.place(weldstiffOriginH_1, uDirstiffH_1, wDirstiffH_1)

        weldstiffOriginH_2 = numpy.array([self.beam_stiffener_2.T/2, self.beamLeft.length+ self.bbWeldWeb_L3.b, -(self.beamLeft.D/2 + self.beam_stiffener_3.W )])
        uDirstiffH_2 = numpy.array([0, -1.0, 0])
        wDirstiffH_2 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHL_2.place(weldstiffOriginH_2, uDirstiffH_2, wDirstiffH_2)

        gap = self.beamLeft.length  + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b
        weldstiffOriginH_3 = numpy.array([self.beam_stiffener_3.T/2, gap, self.beamLeft.D/2 + self.beam_stiffener_3.W])
        uDirstiffH_3 = numpy.array([0, 1.0, 0])
        wDirstiffH_3 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHL_3.place(weldstiffOriginH_3, uDirstiffH_3, wDirstiffH_3)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b
        weldstiffOriginH_4 = numpy.array(
            [-self.beam_stiffener_3.T / 2, gap, -(self.beamLeft.D / 2 + self.beam_stiffener_4.W)])
        uDirstiffH_4 = numpy.array([0, 1.0, 0])
        wDirstiffH_4 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHL_4.place(weldstiffOriginH_4, uDirstiffH_4, wDirstiffH_4)

        weldstiffOriginH_1 = numpy.array([self.beam_stiffener_1.T/2, self.beamLeft.length+ self.bbWeldWeb_L3.b, self.beamLeft.D/2 + self.beam_stiffener_1.L21])
        uDirstiffH_1 = numpy.array([0, -1.0, 0])
        wDirstiffH_1 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHR_1.place(weldstiffOriginH_1, uDirstiffH_1, wDirstiffH_1)

        weldstiffOriginH_2 = numpy.array([-self.beam_stiffener_2.T / 2, self.beamLeft.length + self.bbWeldWeb_L3.b,
                                          -(self.beamLeft.D / 2 + self.beam_stiffener_2.L21)])
        uDirstiffH_2 = numpy.array([0, -1.0, 0])
        wDirstiffH_2 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHR_2.place(weldstiffOriginH_2, uDirstiffH_2, wDirstiffH_2)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T+ self.bbWeldWeb_L3.b
        weldstiffOriginH_3 = numpy.array([-self.beam_stiffener_3.T/2, gap, self.beamLeft.D/2 + self.beam_stiffener_3.L21 ])
        uDirstiffH_3 = numpy.array([0, 1.0, 0])
        wDirstiffH_3 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHR_3.place(weldstiffOriginH_3, uDirstiffH_3, wDirstiffH_3)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b
        weldstiffOriginH_4 = numpy.array(
            [self.beam_stiffener_4.T / 2, gap, -(self.beamLeft.D / 2 + self.beam_stiffener_4.L21)])
        uDirstiffH_4 = numpy.array([0, 1.0, 0])
        wDirstiffH_4 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHR_4.place(weldstiffOriginH_4, uDirstiffH_4, wDirstiffH_4)

    def create_bbWeldStiffLength(self):
        '''
        initialise the location of the stiffener weld along the length by defining the local origin of the bolt group with respect to global origin
        '''
        weldstiffOriginL_1 = numpy.array(
            [-self.beam_stiffener_1.T / 2, self.beamLeft.length - self.beam_stiffener_1.L22 + self.bbWeldWeb_L3.b,
             self.beamLeft.D / 2])
        uDirstiffL_1 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_1 = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldStiffLL_1.place(weldstiffOriginL_1, uDirstiffL_1, wDirstiffL_1)

        weldstiffOriginL_2 = numpy.array(
            [self.beamLeft.t / 2, self.beamLeft.length - self.beam_stiffener_1.L22 + self.bbWeldWeb_L3.b,
             -self.beamLeft.D / 2])
        uDirstiffL_2 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_2 = numpy.array([0, -1.0, 0.0])
        self.bbWeldStiffLL_2.place(weldstiffOriginL_2, uDirstiffL_2, wDirstiffL_2)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22 + self.bbWeldStiffLL_3.L + self.bbWeldWeb_L3.b
        weldstiffOriginL_3 = numpy.array([-self.beam_stiffener_3.T / 2, gap, self.beamLeft.D / 2])
        uDirstiffL_3 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_3 = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldStiffLL_3.place(weldstiffOriginL_3, uDirstiffL_3, wDirstiffL_3)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22 + self.bbWeldStiffLL_3.L + self.bbWeldWeb_L3.b
        weldstiffOriginL_4 = numpy.array([self.beamLeft.t / 2, gap, -self.beamLeft.D / 2])
        uDirstiffL_4 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_4 = numpy.array([0, -1.0, 0.0])
        self.bbWeldStiffLL_4.place(weldstiffOriginL_4, uDirstiffL_4, wDirstiffL_4)

        weldstiffOriginL_1 = numpy.array([self.beamLeft.t/2, self.beamLeft.length - self.beam_stiffener_2.L + self.bbWeldWeb_L3.b, self.beamLeft.D/2 ])
        uDirstiffL_1 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldStiffLR_1.place(weldstiffOriginL_1, uDirstiffL_1, wDirstiffL_1)

        weldstiffOriginL_2 = numpy.array([-self.beam_stiffener_2.T/2 , self.beamLeft.length - self.beam_stiffener_2.L+ self.bbWeldWeb_L3.b , -self.beamLeft.D/2])
        uDirstiffL_2 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_2 = numpy.array([0, 1.0, 0.0])
        self.bbWeldStiffLR_2.place(weldstiffOriginL_2, uDirstiffL_2, wDirstiffL_2)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22+ self.bbWeldWeb_L3.b
        weldstiffOriginL_3 = numpy.array([self.beamLeft.t/2, gap , self.beamLeft.D/2 ])
        uDirstiffL_3 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_3 = numpy.array([0.0, 1.0,0.0])
        self.bbWeldStiffLR_3.place(weldstiffOriginL_3, uDirstiffL_3, wDirstiffL_3)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22+ self.bbWeldWeb_L3.b
        weldstiffOriginL_4 = numpy.array([-self.beamLeft.t/2, gap , -self.beamLeft.D/2 ])
        uDirstiffL_4 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_4 = numpy.array([0, 1.0, 0.0])
        self.bbWeldStiffLR_4.place(weldstiffOriginL_4, uDirstiffL_4, wDirstiffL_4)

    def create_bbWeldFlushstiffHeight(self):
        '''
        initialise the location of the side stiffener weld along the height by defining the local origin of the bolt group with respect to global origin
        '''
        gap = self.beamLeft.length + self.bbWeldWeb_L3.b
        stiffenerOrigin1_u1 = numpy.array([-self.beam_stiffener_F1.L22 - self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc1])
        stiffener1_u1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff1_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

        gap = self.beamLeft.length + self.bbWeldWeb_L3.b
        stiffenerOrigin1_l1 = numpy.array([-self.beam_stiffener_F1.W - self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff1_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

        gap = self.beamLeft.length + self.bbWeldWeb_L3.b
        stiffenerOrigin1_u1 = numpy.array([(self.beam_stiffener_F1.W + self.beamLeft.t / 2), gap,
                                           self.beamRight.D / 2 - self.loc1])
        stiffener1_u1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff2_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

        gap = self.beamLeft.length + self.bbWeldWeb_L3.b
        stiffenerOrigin1_l1 = numpy.array([(self.beam_stiffener_F1.L22 + self.beamLeft.t / 2), gap,
                                           self.beamRight.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff2_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b
        stiffenerOrigin1_u1 = numpy.array([-self.beam_stiffener_F1.W - self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc1])
        stiffener1_u1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff3_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T+ self.bbWeldWeb_L3.b
        stiffenerOrigin1_l1 = numpy.array([-self.beam_stiffener_F1.L22 - self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff3_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b
        stiffenerOrigin1_u1 = numpy.array([self.beam_stiffener_F1.L22 + self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc1])
        stiffener1_u1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff4_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T+ self.bbWeldWeb_L3.b
        stiffenerOrigin1_l1 = numpy.array([self.beam_stiffener_F1.W + self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff4_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

        if self.loc2 != None:
            gap = self.beamLeft.length + self.bbWeldWeb_L3.b
            stiffenerOrigin1_u1 = numpy.array([-self.beam_stiffener_F1.L22 - self.beamLeft.t / 2, gap,
                                               self.beamRight.D / 2 - self.loc2])
            stiffener1_u1_uDir = numpy.array([0.0, -1.0, 0.0])
            stiffener1_u1_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.bbWeldstiff5_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

            gap = self.beamLeft.length + self.bbWeldWeb_L3.b
            stiffenerOrigin1_l1 = numpy.array([-self.beam_stiffener_F1.W - self.beamLeft.t / 2, gap,
                                               self.beamRight.D / 2 - self.loc2 - self.beam_stiffener_F1.T])
            stiffener1_l1_uDir = numpy.array([0.0, -1.0, 0.0])
            stiffener1_l1_wDir = numpy.array([1.0, 0.0, 0.0])
            self.bbWeldstiff5_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

            gap = self.beamLeft.length + self.bbWeldWeb_L3.b
            stiffenerOrigin1_u1 = numpy.array([(self.beam_stiffener_F1.W + self.beamLeft.t / 2), gap,
                                               self.beamRight.D / 2 - self.loc2])
            stiffener1_u1_uDir = numpy.array([0.0, -1.0, 0.0])
            stiffener1_u1_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.bbWeldstiff6_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

            gap = self.beamLeft.length + self.bbWeldWeb_L3.b
            stiffenerOrigin1_l1 = numpy.array([(self.beam_stiffener_F1.L22 + self.beamLeft.t / 2), gap,
                                               self.beamRight.D / 2 - self.loc2 - self.beam_stiffener_F1.T])
            stiffener1_l1_uDir = numpy.array([0.0, -1.0, 0.0])
            stiffener1_l1_wDir = numpy.array([1.0, 0.0, 0.0])
            self.bbWeldstiff6_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

            gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b
            stiffenerOrigin1_u1 = numpy.array([-self.beam_stiffener_F1.W - self.beamLeft.t / 2, gap,
                                               self.beamRight.D / 2 - self.loc2])
            stiffener1_u1_uDir = numpy.array([0.0, 1.0, 0.0])
            stiffener1_u1_wDir = numpy.array([1.0, 0.0, 0.0])
            self.bbWeldstiff7_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

            gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b
            stiffenerOrigin1_l1 = numpy.array([-self.beam_stiffener_F1.L22 - self.beamLeft.t / 2, gap,
                                               self.beamRight.D / 2 - self.loc2 - self.beam_stiffener_F1.T])
            stiffener1_l1_uDir = numpy.array([0.0, 1.0, 0.0])
            stiffener1_l1_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.bbWeldstiff7_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

            gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b
            stiffenerOrigin1_u1 = numpy.array([self.beam_stiffener_F1.L22 + self.beamLeft.t / 2, gap,
                                               self.beamRight.D / 2 - self.loc2])
            stiffener1_u1_uDir = numpy.array([0.0, 1.0, 0.0])
            stiffener1_u1_wDir = numpy.array([1.0, 0.0, 0.0])
            self.bbWeldstiff8_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

            gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b
            stiffenerOrigin1_l1 = numpy.array([self.beam_stiffener_F1.W + self.beamLeft.t / 2, gap,
                                               self.beamRight.D / 2 - self.loc2 - self.beam_stiffener_F1.T])
            stiffener1_l1_uDir = numpy.array([0.0, 1.0, 0.0])
            stiffener1_l1_wDir = numpy.array([-1.0, 0.0, 0.0])
            self.bbWeldstiff8_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)



    def create_bbWeldFlushstiffLength(self):
        '''
        initialise the location of the side stiffener weld along the length by defining the local origin of the bolt group with respect to global origin
        '''
        gap = self.beamLeft.length - self.beam_stiffener_F1.L + self.bbWeldWeb_L3.b
        stiffenerOrigin1_u2 = numpy.array([-self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc1])
        stiffener1_u2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff1_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

        gap = self.beamLeft.length - self.beam_stiffener_F1.L22 + self.bbWeldWeb_L3.b
        stiffenerOrigin1_l2 = numpy.array([-self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        stiffener1_l2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff1_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)

        gap = self.beamLeft.length - self.beam_stiffener_F1.L + self.bbWeldWeb_L3.b
        stiffenerOrigin1_u2 = numpy.array([self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc1])
        stiffener1_u2_uDir = numpy.array([0.0, 0.0, 1.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff2_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

        gap = self.beamLeft.length - self.beam_stiffener_F1.L22 + self.bbWeldWeb_L3.b
        stiffenerOrigin1_l2 = numpy.array([self.beamLeft.t/2, gap,
                                           self.beamRight.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        stiffener1_l2_uDir = numpy.array([0.0, 0.0, -1.0])
        stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff2_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L22+ self.bbWeldWeb_L3.b
        stiffenerOrigin1_u2 = numpy.array([-self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc1])
        stiffener1_u2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff3_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L+ self.bbWeldWeb_L3.b
        stiffenerOrigin3_l2 = numpy.array([-self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        stiffener3_l2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener3_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff3_l2.place(stiffenerOrigin3_l2, stiffener3_l2_uDir, stiffener3_l2_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L22+ self.bbWeldWeb_L3.b
        stiffenerOrigin1_u2 = numpy.array([self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc1])
        stiffener1_u2_uDir = numpy.array([0.0, 0.0, 1.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff4_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L+ self.bbWeldWeb_L3.b
        stiffenerOrigin1_l2 = numpy.array([self.beamLeft.t/2, gap,
                                           self.beamRight.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        stiffener1_l2_uDir = numpy.array([0.0, 0.0, -1.0])
        stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff4_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)

        if self.loc2 != None:
            gap = self.beamLeft.length - self.beam_stiffener_F1.L + self.bbWeldWeb_L3.b
            stiffenerOrigin1_u2 = numpy.array([-self.beamLeft.t / 2, gap,
                                               self.beamRight.D / 2 - self.loc2])
            stiffener1_u2_uDir = numpy.array([-1.0, 0.0, 0.0])
            stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
            self.bbWeldstiff5_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

            gap = self.beamLeft.length - self.beam_stiffener_F1.L22 + self.bbWeldWeb_L3.b
            stiffenerOrigin1_l2 = numpy.array([-self.beamLeft.t / 2, gap,
                                               self.beamRight.D / 2 - self.loc2 - self.beam_stiffener_F1.T])
            stiffener1_l2_uDir = numpy.array([-1.0, 0.0, 0.0])
            stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
            self.bbWeldstiff5_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)

            gap = self.beamLeft.length - self.beam_stiffener_F1.L + self.bbWeldWeb_L3.b
            stiffenerOrigin1_u2 = numpy.array([self.beamLeft.t / 2, gap,
                                               self.beamRight.D / 2 - self.loc2])
            stiffener1_u2_uDir = numpy.array([0.0, 0.0, 1.0])
            stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
            self.bbWeldstiff6_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

            gap = self.beamLeft.length - self.beam_stiffener_F1.L22 + self.bbWeldWeb_L3.b
            stiffenerOrigin1_l2 = numpy.array([self.beamLeft.t / 2, gap,
                                               self.beamRight.D / 2 - self.loc2 - self.beam_stiffener_F1.T])
            stiffener1_l2_uDir = numpy.array([0.0, 0.0, -1.0])
            stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
            self.bbWeldstiff6_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)

            gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L22 + self.bbWeldWeb_L3.b
            stiffenerOrigin1_u2 = numpy.array([-self.beamLeft.t / 2, gap,
                                               self.beamRight.D / 2 - self.loc2])
            stiffener1_u2_uDir = numpy.array([-1.0, 0.0, 0.0])
            stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
            self.bbWeldstiff7_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

            gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L + self.bbWeldWeb_L3.b
            stiffenerOrigin3_l2 = numpy.array([-self.beamLeft.t / 2, gap,
                                               self.beamRight.D / 2 - self.loc2 - self.beam_stiffener_F1.T])
            stiffener3_l2_uDir = numpy.array([-1.0, 0.0, 0.0])
            stiffener3_l2_wDir = numpy.array([0.0, -1.0, 0.0])
            self.bbWeldstiff7_l2.place(stiffenerOrigin3_l2, stiffener3_l2_uDir, stiffener3_l2_wDir)

            gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L22 + self.bbWeldWeb_L3.b
            stiffenerOrigin1_u2 = numpy.array([self.beamLeft.t / 2, gap,
                                               self.beamRight.D / 2 - self.loc2])
            stiffener1_u2_uDir = numpy.array([0.0, 0.0, 1.0])
            stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
            self.bbWeldstiff8_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

            gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L + self.bbWeldWeb_L3.b
            stiffenerOrigin1_l2 = numpy.array([self.beamLeft.t / 2, gap,
                                               self.beamRight.D / 2 - self.loc2 - self.beam_stiffener_F1.T])
            stiffener1_l2_uDir = numpy.array([0.0, 0.0, -1.0])
            stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
            self.bbWeldstiff8_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)


        #############################################################################################################
        #   Following functions returns the CAD model to the function display_3DModel of main file                  #
        #############################################################################################################


    def get_beam_models(self):
        """

        :return: CAD model of bothe left and right beam
        """
        beams = BRepAlgoAPI_Fuse(self.beamLModel, self.beamRModel).Shape()
        return beams

    def get_plate_connector_models(self):
        """

        :return: CAD model of extended end plate and stiffeners
        """

        if self.module.endplate_type == 'Extended One Way - Irreversible Moment':
            connector_plate = [self.plateLModel, self.plateRModel, self.beam_stiffener_1Model,
                    self.beam_stiffener_3Model]


        elif self.module.endplate_type == 'Extended Both Ways - Reversible Moment':
            connector_plate = [self.plateLModel, self.plateRModel, self.beam_stiffener_1Model,
                    self.beam_stiffener_2Model, self.beam_stiffener_3Model,
                    self.beam_stiffener_4Model]


        elif self.module.endplate_type == 'Flushed - Reversible Moment':
            # if self.loc2 ==None:
                connector_plate = [self.plateLModel, self.plateRModel]
            # flush stiffener#
            # else:
            #     connector_plate = [self.plateLModel, self.plateRModel, self.beam_stiffener_F1Model,
            #                        self.beam_stiffener_F2Model,
            #                        self.beam_stiffener_F3Model,
            #                        self.beam_stiffener_F4Model, self.beam_stiffener_F5Model,self.beam_stiffener_F6Model,
            #                        self.beam_stiffener_F7Model,self.beam_stiffener_F8Model]


        plates = connector_plate[0]
        for comp in connector_plate[1:]:
            plates = BRepAlgoAPI_Fuse(comp, plates).Shape()

        return plates

    def get_welded_models(self):
        """

        :return: CAD model for all the welds
        """

        if self.module.endplate_type == 'Extended One Way - Irreversible Moment':
            welded_sec = [self.bbWeldStiffHL_1Model, self.bbWeldFlang_R1Model,
                    self.bbWeldFlang_R2Model, self.bbWeldFlang_L1Model,
                    self.bbWeldFlang_L2Model, self.bbWeldWeb_R3Model, self.bbWeldWeb_L3Model,
                    self.bbWeldStiffLL_1Model, self.bbWeldStiffHL_3Model, self.bbWeldStiffLL_3Model,
                    self.bbWeldStiffHR_1Model,
                    self.bbWeldStiffLR_1Model, self.bbWeldStiffHR_3Model,
                    self.bbWeldStiffLR_3Model]

        elif self.module.endplate_type == 'Extended Both Ways - Reversible Moment':
            welded_sec = [self.bbWeldStiffHL_1Model, self.bbWeldFlang_R1Model,
                          self.bbWeldFlang_R2Model, self.bbWeldFlang_L1Model,
                          self.bbWeldFlang_L2Model, self.bbWeldWeb_R3Model, self.bbWeldWeb_L3Model,
                          self.bbWeldStiffLL_1Model, self.bbWeldStiffHL_3Model, self.bbWeldStiffLL_3Model,
                          self.bbWeldStiffHL_2Model, self.bbWeldStiffLL_2Model,
                          self.bbWeldStiffHL_4Model, self.bbWeldStiffLL_4Model, self.bbWeldStiffHR_1Model,
                          self.bbWeldStiffLR_1Model, self.bbWeldStiffHR_3Model,
                          self.bbWeldStiffLR_3Model, self.bbWeldStiffHR_2Model, self.bbWeldStiffLR_2Model,
                          self.bbWeldStiffHR_4Model, self.bbWeldStiffLR_4Model]

        elif self.module.endplate_type == 'Flushed - Reversible Moment':
            # if self.loc2 == None:
            welded_sec = [self.bbWeldFlang_R1Model,
                          self.bbWeldFlang_R2Model, self.bbWeldFlang_L1Model,
                          self.bbWeldFlang_L2Model, self.bbWeldWeb_R3Model, self.bbWeldWeb_L3Model
                          ]
            # flush stiffener#
            # else:
            #     welded_sec = [self.bbWeldFlang_R1Model,
            #                   self.bbWeldFlang_R2Model, self.bbWeldFlang_L1Model,
            #                   self.bbWeldFlang_L2Model, self.bbWeldWeb_R3Model, self.bbWeldWeb_L3Model,
            #                   self.bbWeldstiff1_u1Model, self.bbWeldstiff1_u2Model, self.bbWeldstiff1_l1Model,
            #                   self.bbWeldstiff1_l2Model, self.bbWeldstiff2_u1Model,
            #                   self.bbWeldstiff2_u2Model, self.bbWeldstiff2_l1Model, self.bbWeldstiff2_l2Model,
            #                   self.bbWeldstiff3_u1Model, self.bbWeldstiff3_u2Model,
            #                   self.bbWeldstiff3_l1Model, self.bbWeldstiff3_l2Model, self.bbWeldstiff4_u1Model,
            #                   self.bbWeldstiff4_u2Model, self.bbWeldstiff4_l1Model,
            #                   self.bbWeldstiff4_l2Model,
            #                   self.bbWeldstiff5_u1Model, self.bbWeldstiff5_u2Model, self.bbWeldstiff5_l1Model,
            #                   self.bbWeldstiff5_l2Model, self.bbWeldstiff6_u1Model,
            #                   self.bbWeldstiff6_u2Model, self.bbWeldstiff6_l1Model, self.bbWeldstiff6_l2Model,
            #                   self.bbWeldstiff7_u1Model, self.bbWeldstiff7_u2Model,
            #                   self.bbWeldstiff7_l1Model, self.bbWeldstiff7_l2Model, self.bbWeldstiff8_u1Model,
            #                   self.bbWeldstiff8_u2Model, self.bbWeldstiff8_l1Model,
            #                   self.bbWeldstiff8_l2Model
            #                   ]


        welds = welded_sec[0]
        for comp in welded_sec[1:]:
            welds = BRepAlgoAPI_Fuse(comp, welds).Shape()

        return welds

    def get_nut_bolt_array_models(self):
        """

        :return: CAD model for nut bolt array
        """

        nut_bolts = self.nut_bolt_array.get_models()
        print(nut_bolts)
        array = nut_bolts[0]
        for comp in nut_bolts:
            array = BRepAlgoAPI_Fuse(comp, array).Shape()

        return array

    def get_connector_models(self):
        """

        :return: CAD models of the connecting components
        """

        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()

        CAD_list = [plate_connectors, welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD


    def get_models(self):
        """

        :return: complete CAD model
        """

        beams = self.get_beam_models()
        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()

        CAD_list = [beams, plate_connectors, welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD



