'''
Created on 19-March-2020

@author : Anand Swaroop
'''

from cad.items.anchor_bolt import *
from cad.items.nut import Nut
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from cad.items.ModelUtils import getGpPt
import copy

class NutBoltArray():
    """
    add a diagram here
    """

    def __init__(self, column, baseplate, nut, bolt, numberOfBolts, nutSpace):


        self.baseplate = baseplate
        self.column = column
        self.nut = nut
        self.bolt = bolt
        self.numberOfBolts = numberOfBolts
        self.gap = nutSpace
        self.origin = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir = None

        self.ab1 = copy.deepcopy(self.bolt)
        self.ab2 = copy.deepcopy(self.bolt)
        self.ab3 = copy.deepcopy(self.bolt)
        self.ab4 = copy.deepcopy(self.bolt)

        self.nt1 = copy.deepcopy(self.nut)
        self.nt2 = copy.deepcopy(self.nut)
        self.nt3 = copy.deepcopy(self.nut)
        self.nt4 = copy.deepcopy(self.nut)


        # self.initBoltPlaceParam(plateObj)
        self.initBoltPlaceParam()

        self.bolts = []
        self.nuts = []

        self.positions = []

        self.models = []

        self.enddist = 50
        self.edgedist = 50
        self.clearence = 50


        self.initialiseNutBolts()

    def initialiseNutBolts(self):
        """
        Initializing the Nut and Bolt
        :return:
        """
        pass
        # b = self.bolt
        # n = self.nut
        # for i in range(self.row*self.col):
        #     bolt_len_required = float(self.gap)
        #     # b.H = bolt_len_required + (5-bolt_len_required) % 5 #Todo : enter the length fo the anchor bolt
        #     self.bolts.append(AnchorBolt_A(b.l, b.c, b.a, b.r))         #Todo: change this with respect to anchor bolt parameters)
        #     self.nuts.append(Nut(n.R, n.T, n.H, n.r1))

    def initBoltPlaceParam(self):

        self.enddist = 50
        self.edgedist = 50
        self.clearence = 50

        self.pitch = self.baseplate.L - 2*self.enddist
        self.gauge = self.baseplate.W - 2*self.edgedist
        # self.edge = 100
        # self.plateedge = 50
        # self.end = 50
        self.row = 2
        self.col = 2

    def calculatePositions(self):
        pass
        # self.positions = []
        # # pos = self.origin
        #
        # # self.pitch1 = 400
        # # self.gauge1 = 100
        #
        # pos1 =  pos + self.edgedist * self.gaugeDir
        # pos2 = pos1 + self.gauge * self.gaugeDir
        # pos3 = pos2 + self.pitch * self.pitchDir
        # pos4 = pos3 - self.gauge * self.gaugeDir
        # positions = [pos1, pos2, pos3, pos4]

        # for rw in range(self.col):
        #     for col in range(self.row):
        #         pos = self.origin
        #         pos = pos + self.edgedist*self.gaugeDir
        #         pos = pos + self.enddist*self.pitchDir
        #
        #         self.positions.append(pos)

        # for pos in positions:
        #     self.positions.append(pos)

        # self.positions = [pos1, pos2, pos3, pos4]

    def place(self, origin, gaugeDir, pitchDir, boltDir):
        self.origin = origin
        self.gaugeDir = gaugeDir
        self.pitchDir = pitchDir
        self.boltDir = boltDir

        # self.calculatePositions()
        pos = self.origin
        pos1 = pos + self.edgedist * self.gaugeDir + self.enddist * self.pitchDir
        pos2 = pos1 + self.gauge * self.gaugeDir
        pos3 = pos2 + self.pitch * self.pitchDir
        pos4 = pos3 - self.gauge * self.gaugeDir

        self.ab1.place(pos1 - (self.bolt.ex )*numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
        self.ab2.place(pos2 - (self.bolt.ex )*numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
        self.ab3.place(pos3 - (self.bolt.ex )*numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
        self.ab4.place(pos4 - (self.bolt.ex )*numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

        self.nt1.place(pos1 - (self.nt1.T+50)*numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
        self.nt2.place(pos2 - (self.nt1.T+50)*numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
        self.nt3.place(pos3 - (self.nt1.T+50)*numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
        self.nt4.place(pos4 - (self.nt1.T+50)*numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

        # for index, pos in enumerate(self.positions):
        #     self.bolt[index].place(pos, gaugeDir, boltDir)
        #     self.nut[index].place((pos+self.gap*boltDir), gaugeDir, -boltDir)

    def create_model(self):
        # for bolt in self.bolts:
        #     self.models.append(bolt.create_model())

        self.ab1Model = self.ab1.create_model()
        self.ab2Model = self.ab2.create_model()
        self.ab3Model = self.ab3.create_model()
        self.ab4Model = self.ab4.create_model()

        self.nt1Model = self.nt1.create_model()
        self.nt2Model = self.nt2.create_model()
        self.nt3Model = self.nt3.create_model()
        self.nt4Model = self.nt4.create_model()

        self.models = [self.ab1Model, self.ab2Model, self.ab3Model, self.ab4Model, self.nt1Model, self.nt2Model, self.nt3Model, self.nt4Model]

        # for nut in self.nuts:
        #     self.models.append(nut.create_model())

    #     dbg =  self.dbgSphere(self.origin)
    #     self.models.append(dbg)
    #
    # def dbgSphere(self, pt):
    #     return BRepPrimAPI_MakeSphere(getGpPt(pt), 0.1).Shape()

    def get_models(self):
        return self.models


if __name__ == '__main__':
    
    from cad.items.anchor_bolt import *
    from cad.items.nut import Nut
    from cad.items.ISection import ISection
    from cad.items.plate import Plate

    
    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    nutboltArrayOrigin = numpy.array([0., 0., 0.])
    gaugeDir = numpy.array([1.0, 0, 0])
    pitchDir = numpy.array([0, 1.0, 0])
    boltDir = numpy.array([0, 0, 1.0])



    numberOfBolts = 4
    column = ISection(B=250, T=13.7, D=450, t=9.8, R1= 14.0, R2= 7.0, alpha= 94, length= 1500, notchObj= None)
    baseplate = Plate(L=650, W=500, T=30)

    l = 550
    c = 225
    a = 175
    r = 24
    ex_length = (50 + 24 + baseplate.T)  # nut.T = 24
    bolt = AnchorBolt_A(l= 250, c= 125, a= 75, r= 12, ex= ex_length)
    # bolt = AnchorBolt_B(l= 250, c= 125, a= 75, r= 12)
    # bolt = AnchorBolt_Endplate(l= 250, c= 125, a= 75, r= 12)

    nut = Nut(R= bolt.r*3, T= 24, H= 30, innerR1= bolt.r)

    nutSpace = bolt.c + baseplate.T


    nut_bolt_array = NutBoltArray(column, baseplate,  nut, bolt, numberOfBolts, nutSpace)



    place = nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    nut_bolt_array_Model = nut_bolt_array.create_model()

    nut_bolts = nut_bolt_array.get_models()
    array = nut_bolts[0]
    for comp in nut_bolts:
        array = BRepAlgoAPI_Fuse(comp, array).Shape()


    display.DisplayShape(array, update=True)
    display.DisableAntiAliasing()
    start_display()

