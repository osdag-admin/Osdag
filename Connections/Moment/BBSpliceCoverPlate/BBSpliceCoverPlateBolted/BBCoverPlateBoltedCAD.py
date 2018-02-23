import numpy

class BBCoverPlateBoltedCAD(object):
    def __init__(self, beamLeft, beamRight):

        self.beamLeft = beamLeft
        self.beamRight = beamRight
        self.gap = 5.0

    def create_3DModel(self):
        self.createBeamLGeometry()
        self.createBeamRGeometry()


        self.beamLModel = self.beamLeft.create_model()
        self.beamRModel = self.beamRight.create_model()

    def createBeamLGeometry(self):
        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamRGeometry(self):
        gap = self.beamRight.length + self.gap
        beamOriginR = numpy.array([0.0, gap, 0.0])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_wDir)

    def get_beamLModel(self):
        return self.beamLModel

    def get_beamRModel(self):
        return self.beamRModel