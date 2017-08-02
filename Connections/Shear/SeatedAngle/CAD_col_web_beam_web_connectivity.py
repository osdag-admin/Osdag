'''
Created on 11-May-2015

@author: deepa
'''
import numpy
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut
import math

"""
+----------------------------------------------------------------------------------------------+
|                                                                                              |
|                                                                                              |
|                                                                                              |
|                           ^     ^ +---^                                                      |
|                           |     | |   |                                                      |
|                           |     | |   | topangle-column-end-dist                             |
|                           |     | |   |                                                      |
|                           |     | |   |                                                      |
|                           |     v +------+                                                   |
|                           |   bpos|   |     Topclip Angle                                    |
|                                   |   |                                                      |
|                           A       |   |                                                      |
|                                   |   |                                                      |
|                           |       |   |                                                      |
|                           |       |   |              +    topangle-beam-end-dist             |
|                           |       |   |       apos   <--------+                              |
|                           |       |   +-----------------------+                              |
|                           |       |                  |        |                              |
|                           v       +---------------------------^                              |
|                                                      |                                       |
|                                                      +                                       |
|                                   <---------- B  ---- --------->                             |
|                                                      +                                       |
|                            ^    + +---------------------------+                              |
|                            |    | |                  |        |                              |
|          Seatedangle-col-end-dist |   +-----------------------+                              |
|                            |    | |   |              <--------+ Seatedangle-beam-end-dist    |
|                            |    v |   |              +                                       |
|                            | apos |   |        bpos                                          |
|                            |    +--------+                                                   |
|                                   |   |                                                      |
|                            A      |   |                                                      |
|                                   |   |                                                      |
|                            |    +--------+                                                   |
|                            |      |   |                                                      |
|                            |      |   |                                                      |
|                            |      |   |                                                      |
|                            |      |   |                                                      |
|                            v      +---+                                                      |
|                                                                                              |
+----------------------------------------------------------------------------------------------+

"""

class ColWebBeamWeb(object):
    """

    """
    
    def __init__(self,column,beam,angle,topclipangle,nutBoltArray,gap):
        self.column = column
        self.beam = beam
        self.angle = angle
        self.topclipangle = topclipangle
        self.nut_bolt_array = nutBoltArray
        self.gap = gap
        self.columnModel = None
        self.beamModel = None
        self.angleModel= None
        self.topclipangleModel = None
        self.clearDist = 20.0 # This distance between edge of the column web/flange and beam cross section
        
    def create_3dmodel(self):
        self.creatColumGeometry()
        self.createBeamGeometry()
        self.createAngleGeometry()
        self.createNutBoltArray()
        
        # Call for createModel
        self.columnModel = self.column.create_model()
        self.beamModel = self.beam.create_model()
        self.angleModel = self.angle.create_model()
        self.topclipangleModel = self.topclipangle.create_model()
        self.nutboltArrayModels = self.nut_bolt_array.createModel()
        
    def creatColumGeometry(self):
        columnOrigin = numpy.array([0, 0, 0])
        column_uDir = numpy.array([1.0, 0, 0])
        wDir1 = numpy.array([0.0, 0, 1.0])
        self.column.place(columnOrigin, column_uDir, wDir1)
                
    def createBeamGeometry(self):
        beamorigin = self.column.sec_origin + (self.column.t/2 * self.column.uDir) + \
                     (self.column.length/2 * self.column.wDir) + (self.gap * self.column.uDir)
        uDir = numpy.array([0, 1.0, 0])
        wDir = numpy.array([1.0, 0, 0.0])
        self.beam.place(beamorigin, uDir, wDir)
        
    def createAngleGeometry(self):
        angleOrigin =((self.column.sec_origin +self.column.t/2 + 0.05)*self.column.uDir)+\
                     ((self.column.length/2 - self.beam.D/2 + 0.05) * self.column.wDir)+\
                     (self.angle.L/2 * (-self.column.vDir))

        wDir = numpy.array([0.0, 1.0, 0.0])
        uDir = numpy.array([1.0, 0.0, 0.0])
        self.angle.place(angleOrigin, uDir, wDir)
                 
        topclipangleOrigin =((self.column.sec_origin + self.column.t/2 + 0.05)*self.column.uDir)+\
                            ((self.column.length/2 + self.beam.D/2 + 0.05) * self.column.wDir)+\
                            (self.topclipangle.L/2 * (self.column.vDir))

        wDir = numpy.array([0.0, -1.0, 0.0])
        uDir = numpy.array([1.0, 0.0, 0.0])
        self.topclipangle.place(topclipangleOrigin, uDir, wDir)
                 
    
    def createNutBoltArray(self):
    
        gaugeDir = self.angle.wDir
        pitchDir = -self.angle.vDir
        boltDir = -self.angle.uDir
        
        #=======================================================================

        root2 = math.sqrt(2)
        nutboltArrayOrigin = self.angle.sec_origin
        nutboltArrayOrigin = nutboltArrayOrigin + self.angle.A * self.angle.vDir
        nutboltArrayOrigin = nutboltArrayOrigin + self.angle.T * self.angle.uDir
        #nutboltArrayOrigin = nutboltArrayOrigin + self.angle.R2 * (1 - 1 / root2) * self.angle.uDir
        nutboltArrayOrigin = nutboltArrayOrigin - self.angle.R2 / root2 * self.angle.vDir
        
        bgaugeDir = self.angle.wDir
        bpitchDir = -self.angle.uDir
        bboltDir = -self.angle.vDir
        
        bnutboltArrayOrigin = self.angle.sec_origin + self.angle.B * self.angle.uDir
        bnutboltArrayOrigin = bnutboltArrayOrigin + self.angle.T * self.angle.vDir 
        #bnutboltArrayOrigin = bnutboltArrayOrigin + self.angle.R2*(1-1/root2) * self.angle.vDir
        bnutboltArrayOrigin = bnutboltArrayOrigin - self.angle.R2/root2*self.angle.uDir
        
        #=======================================================================
        topclipgaugeDir = -self.topclipangle.wDir
        topclippitchDir = -self.topclipangle.uDir
        topclipboltDir = -self.topclipangle.vDir
        
        topclipnutboltArrayOrigin = self.topclipangle.sec_origin
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.B * self.topclipangle.uDir 
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.T * self.topclipangle.vDir 
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin - self.topclipangle.R2/root2 * self.topclipangle.uDir 
        #topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.R2*(1-1/root2)*self.topclipangle.vDir
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.L * self.topclipangle.wDir
        
        #=======================================================================
        topclipbgaugeDir = -self.topclipangle.wDir
        topclipbpitchDir = -self.topclipangle.vDir
        topclipbboltDir = -self.topclipangle.uDir
        
        topclipbnutboltArrayOrigin = self.topclipangle.sec_origin
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.A * self.topclipangle.vDir 
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.T * self.topclipangle.uDir 
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin - self.topclipangle.R2/root2 * self.topclipangle.vDir 
        #topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin+ self.topclipangle.R2*(1-1/root2)*self.topclipangle.uDir
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.L * self.topclipangle.wDir
        
        #=======================================================================
        self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir, bnutboltArrayOrigin, bgaugeDir, bpitchDir,
                                bboltDir, topclipnutboltArrayOrigin, topclipgaugeDir, topclippitchDir, topclipboltDir, topclipbnutboltArrayOrigin,
                                topclipbgaugeDir, topclipbpitchDir, topclipbboltDir)
      
    def get_models(self):
        '''Returning 3D models
        '''
        return [self.columnModel,self.beamModel,self.angleModel,self.topclipangleModel] + self.nut_bolt_array.get_models()
        
                
    def get_nutboltmodels(self):
        return self.nut_bolt_array.get_models()
    
    def get_beamModel(self):
        finalbeam = self.beamModel
        nutBoltlist = self.nut_bolt_array.get_beam_bolts()
        for bolt in nutBoltlist:
            finalbeam = BRepAlgoAPI_Cut(finalbeam,bolt).Shape()
        return finalbeam
    
    def get_angleModel(self):
        finalAngle = self.angleModel
        return finalAngle
    
    def get_columnModel(self):
        finalcol = self.columnModel
        nutBoltlist = self.nut_bolt_array.get_column_bolts()
        for bolt in nutBoltlist:
            finalcol = BRepAlgoAPI_Cut(finalcol,bolt).Shape()
        return finalcol
