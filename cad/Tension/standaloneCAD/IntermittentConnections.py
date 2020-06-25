'''
Created on 28- May-2020

@author : Anand Swaroop
'''

from cad.items.bolt import Bolt
from cad.items.nut import Nut
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from cad.items.ModelUtils import getGpPt
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from cad.items.filletweld import FilletWeld
from cad.items.plate import Plate


class IntermittentNutBoltPlateArray():
    """
    add a diagram here
    """

    def __init__(self, Obj, nut, bolt, intermittentPlate, nut_space):
        self.Obj = Obj
        self.nut = nut
        self.bolt = bolt
        self.intermittentPlate = intermittentPlate
        self.gap = nut_space

        self.origin = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir = None

        self.initBoltPlaceParams()

        self.bolts = []
        self.nuts = []
        self.boltsabv = []
        self.nutsabv = []
        self.plates = []
        self.initialiseNutBolts()

        self.positions = []
        self.platePositions = []

        self.models = []

        self.platemodels = []

    def initialiseNutBolts(self):
        b = self.bolt
        n = self.nut
        p = self.intermittentPlate
        for i in range(self.row * self.no_intermitent_connections):
            bolt_len_required = float(self.gap)
            b.H = bolt_len_required + 10
            self.bolts.append(Bolt(b.R, b.T, b.H, b.r))
            self.nuts.append(Nut(n.R, n.T, n.H, n.r1))
            self.boltsabv.append(Bolt(b.R, b.T, b.H, b.r))
            self.nutsabv.append(Nut(n.R, n.T, n.H, n.r1))
        for i in range(self.no_intermitent_connections):
            self.plates.append(Plate(p.L, p.W, p.T))

    def initBoltPlaceParams(self):

        self.pitch = 45
        self.spacing = 200
        self.gauge = 35
        self.edge = 35
        self.end = 35
        self.row = 2
        self.col = 1
        self.no_intermitent_connections = 3
        self.memberdeepth = 90
        self.member_thickness = 10
        self.member_web_thickness = 10
        self.root_radius = 6

    def calculatePositions(self):
        """
        Calculate the exact position for nut, bolts and plates.
        """
        self.positions = []
        self.origin = self.origin + (self.spacing - 2*self.end)*self.pitchDir
        for connec in range(self.no_intermitent_connections):
            pltpos = self.origin
            pltpos = pltpos + (connec * self.spacing) * self.pitchDir
            pltpos = pltpos + (self.intermittentPlate.T/2) * self.boltDir
            pltpos = pltpos

            self.platePositions.append(pltpos)
            for rw in range(self.row):
                for col in range(self.col):
                    pos = self.origin +(self.member_thickness + self.root_radius - self.memberdeepth/2) * self.gaugeDir
                    # pos = pos + 5 * self.gaugeDir
                    pos = pos + self.edge * self.gaugeDir
                    pos = pos + col * self.pitch * self.pitchDir
                    pos = pos + self.end * self.pitchDir
                    pos = pos + rw * self.gauge * self.gaugeDir
                    pos = pos + connec * self.spacing * self.pitchDir
                    pos = pos - self.member_web_thickness * self.boltDir

                    self.positions.append(pos)

    def place(self, origin, gaugeDir, pitchDir, boltDir):

        self.origin = origin
        self.gaugeDir = gaugeDir
        self.pitchDir = pitchDir
        self.boltDir = boltDir

        self.calculatePositions()

        if self.Obj == 'Star Angles':
            for index, pos in enumerate(self.positions):
                self.bolts[index].place(pos + self.memberdeepth/2 * self.gaugeDir , self.gaugeDir, self.boltDir)
                self.nuts[index].place((pos + (self.gap) * self.boltDir + self.memberdeepth/2 * self.gaugeDir), self.gaugeDir, -self.boltDir)
                self.boltsabv[index].place(pos + (self.gap + self.bolt.T) * self.boltDir - self.memberdeepth/2 * self.gaugeDir, self.gaugeDir, -self.boltDir)
                self.nutsabv[index].place((pos + (self.bolt.T) * self.boltDir- self.memberdeepth/2 * self.gaugeDir), self.gaugeDir, self.boltDir)

            for index, pltpos in enumerate(self.platePositions):
                self.plates[index].place(pltpos, self.boltDir, self.pitchDir)

        else:
            for index, pos in enumerate(self.positions):
                self.bolts[index].place(pos, gaugeDir, boltDir)
                self.nuts[index].place((pos + self.gap * boltDir), gaugeDir, -boltDir)

            for index, pltpos in enumerate(self.platePositions):
                self.plates[index].place(pltpos, boltDir, pitchDir)

    def create_model(self):
        for bolt in self.bolts:
            self.models.append(bolt.create_model())

        for nut in self.nuts:
            self.models.append(nut.create_model())


        if self.Obj == 'Star Angles':
            for bolt in self.boltsabv:
                self.models.append(bolt.create_model())

            for nut in self.nutsabv:
                self.models.append(nut.create_model())

        for plate in self.plates:
            self.platemodels.append(plate.create_model())
        #
        # nut_bolts = self.models
        # nbarray = nut_bolts[0]
        # for comp in nut_bolts:
        #     nbarray = BRepAlgoAPI_Fuse(comp, nbarray).Shape()
        #
        # plates = self.platemodels
        # parray = plates[0]
        # for comp in plates:
        #     parray = BRepAlgoAPI_Fuse(comp, parray).Shape()
        #
        # array = BRepAlgoAPI_Fuse(nbarray, parray).Shape()
        #
        # return array

    def get_nut_bolt_models(self):
        nut_bolts = self.models
        nbarray = nut_bolts[0]
        for comp in nut_bolts:
            nbarray = BRepAlgoAPI_Fuse(comp, nbarray).Shape()

        return nbarray

    def get_plate_models(self):
        plates = self.platemodels
        parray = plates[0]
        for comp in plates:
            parray = BRepAlgoAPI_Fuse(comp, parray).Shape()
        return parray

    def get_models(self):
        nut_bolts = self.models
        nbarray = nut_bolts[0]
        for comp in nut_bolts:
            nbarray = BRepAlgoAPI_Fuse(comp, nbarray).Shape()

        plates = self.platemodels
        parray = plates[0]
        for comp in plates:
            parray = BRepAlgoAPI_Fuse(comp, parray).Shape()

        array = BRepAlgoAPI_Fuse(nbarray, parray).Shape()

        return array


class IntermittentWelds():
    """
    add a diagram here
    """

    def __init__(self, Obj, welds, intermittentPlate):
        self.Obj = Obj
        self.welds = welds
        self.intermittentPlate = intermittentPlate

        self.origin = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir = None


        self.weldsabw = []
        self.weldsblw = []
        self.weldsabw1 = []
        self.weldsblw1 = []
        self.plates = []

        self.initWeldPlaceParams()
        self.initialiseWelds()

        self.weldabwPositions = []
        self.weldblwPositions = []
        self.platePostions = []

        self.weldmodels = []
        self.platemodels = []

    def initialiseWelds(self):
        w = self.welds
        p = self.intermittentPlate
        for i in range(self.no_intermitent_connections):
            self.weldsabw.append(FilletWeld(w.h, w.b, w.L))
            self.weldsblw.append(FilletWeld(w.h, w.b, w.L))
            self.weldsabw1.append(FilletWeld(w.h, w.b, w.L))
            self.weldsblw1.append(FilletWeld(w.h, w.b, w.L))
            self.plates.append(Plate(p.L, p.W, p.T))

    def initWeldPlaceParams(self):

        self.spacing = 300
        # todo: use if else statement to introduce long leg and short leg and channel and angle member depth
        self.memberdepth = 70
        self.no_intermitent_connections = 2

    def calculatePositions(self):
        """
        Calculate the exact position for welds and plates
        """
        self.origin = self.origin + (self.spacing)*self.uDir
        for i in range(self.no_intermitent_connections):
            pos = self.origin + i * self.spacing * self.uDir
            pos0 = pos + self.intermittentPlate.T / 2 * self.vDir
            pos1 = pos + self.memberdepth / 2 * self.wDir
            pos2 = pos1 - self.memberdepth * self.wDir + self.intermittentPlate.W * self.uDir

            self.platePostions.append(pos0)
            self.weldabwPositions.append(pos1)
            self.weldblwPositions.append(pos2)

    def place(self, origin, uDir, vDir, wDir):
        self.origin = origin
        self.uDir = uDir
        self.vDir = vDir
        self.wDir = wDir

        self.calculatePositions()
        if self.Obj == 'Star Angles':
            for index, pos0 in enumerate(self.platePostions):
                self.plates[index].place(pos0 , vDir, uDir)
            for index, pos1 in enumerate(self.weldabwPositions):
                self.weldsabw[index].place(pos1 - self.memberdepth*wDir/2, wDir, uDir)
                self.weldsabw1[index].place(pos1 + self.intermittentPlate.T * vDir + self.memberdepth*wDir/2, vDir, uDir)
            for index, pos2 in enumerate(self.weldblwPositions):
                self.weldsblw[index].place(pos2 - self.memberdepth*wDir/2, -wDir, -uDir)
                self.weldsblw1[index].place(pos2 + self.intermittentPlate.T * vDir + self.memberdepth*wDir/2, vDir, -uDir)
        else:
            for index, pos0 in enumerate(self.platePostions):
                self.plates[index].place(pos0, vDir, uDir)
            for index, pos1 in enumerate(self.weldabwPositions):
                self.weldsabw[index].place(pos1, wDir, uDir)
                self.weldsabw1[index].place(pos1 + self.intermittentPlate.T * vDir, vDir, uDir)
            for index, pos2 in enumerate(self.weldblwPositions):
                self.weldsblw[index].place(pos2, -wDir, -uDir)
                self.weldsblw1[index].place(pos2 + self.intermittentPlate.T * vDir, vDir, -uDir)

    def create_model(self):
        for weld in self.weldsabw:
            self.weldmodels.append(weld.create_model())
        for weld in self.weldsblw:
            self.weldmodels.append(weld.create_model())
        for weld in self.weldsabw1:
            self.weldmodels.append(weld.create_model())
        for weld in self.weldsblw1:
            self.weldmodels.append(weld.create_model())
        for plate in self.plates:
            self.platemodels.append(plate.create_model())

        welds = self.weldmodels
        weldarray = welds[0]
        for comp in welds:
            weldarray = BRepAlgoAPI_Fuse(comp, weldarray).Shape()

        plates = self.platemodels
        parray = plates[0]
        for comp in plates:
            parray = BRepAlgoAPI_Fuse(comp, parray).Shape()

        array = BRepAlgoAPI_Fuse(weldarray, parray).Shape()

        return array

    def get_welded_models(self):
        welds = self.weldmodels
        weldarray = welds[0]
        for comp in welds:
            weldarray = BRepAlgoAPI_Fuse(comp, weldarray).Shape()

        return weldarray

    def get_plate_models(self):
        plates = self.platemodels
        parray = plates[0]
        for comp in plates:
            parray = BRepAlgoAPI_Fuse(comp, parray).Shape()
        return parray

    def get_models(self):
        welds = self.weldmodels
        weldarray = welds[0]
        for comp in welds:
            weldarray = BRepAlgoAPI_Fuse(comp, weldarray).Shape()

        plates = self.platemodels
        parray = plates[0]
        for comp in plates:
            parray = BRepAlgoAPI_Fuse(comp, parray).Shape()

        array = BRepAlgoAPI_Fuse(weldarray, parray).Shape()

        return array


if __name__ == '__main__':
    from cad.items.bolt import Bolt
    from cad.items.nut import Nut
    from cad.items.plate import Plate
    from cad.items.filletweld import FilletWeld
    import numpy

    from OCC.gp import gp_Pnt
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    nutboltArrayOrigin = numpy.array([0., 0., 0.])
    gaugeDir = numpy.array([0.0, 1.0, 0])
    pitchDir = numpy.array([1.0, 0.0, 0])
    boltDir = numpy.array([0, 0, 1.0])

    bolt = Bolt(R=6, T=5, H=6, r=3)
    nut = Nut(R=bolt.R, T=bolt.T, H=bolt.T + 1, innerR1=bolt.r)
    nut_space = 2*5 + 5 + nut.T  # 2*member.T + plate.T + nut.T
    Obj = 'Star Angles'  #'Channels'  #'Back to Back Channels'  # ''  #'Angles'  #      or 'Back to Back Angles' 'Channels' or

    # nut_bolt_array = NutBoltArray(Obj, nut, bolt, nut_space)

    intermittentPlate = Plate(L= 2*125, W=70, T=10)
    nut_bolt_array = IntermittentNutBoltPlateArray(Obj, nut, bolt, intermittentPlate, nut_space)

    place = nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)
    nut_bolt_array_Model = nut_bolt_array.create_model()

    # welds = FilletWeld(h=5, b=5, L=intermittentPlate.W)
    # weld_plate_array = IntermittentWelds(Obj, welds, intermittentPlate)
    # place = weld_plate_array.place(nutboltArrayOrigin, pitchDir, gaugeDir, boltDir)

    # weld_plate_array.create_model()

    # welds = weld_plate_array.get_welded_models()
    # plates = weld_plate_array.get_plate_models()

    array = nut_bolt_array.get_models()
    nbarray = nut_bolt_array.get_nut_bolt_models()
    parray = nut_bolt_array.get_plate_models()
    # array = nut_bolts[0]
    # for comp in nut_bolts:
    #     array = BRepAlgoAPI_Fuse(comp, array).Shape()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    display.DisplayShape(nbarray, color= 'YELLOW' ,update=True)
    display.DisplayShape(parray, color= 'BLUE', update=True)
    # display.DisplayShape(welds, color='RED', update=True)
    # display.DisplayShape(plates, color='BLUE', update=True)
    display.DisableAntiAliasing()
    start_display()
