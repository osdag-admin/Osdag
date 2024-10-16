import numpy
import copy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from cad.items.ISection import *


class CompressionMemberCAD(object):
    def __init__(self, sec):
        self.sec = sec

    def create_3DModel(self):
        """

        """
        self.createcolumnGeometry()

    def createcolumnGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        columnOriginL = numpy.array([0.0, 0.0, 0.0])
        columnL_uDir = numpy.array([1.0, 0.0, 0.0])
        columnL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.sec.place(columnOriginL, columnL_uDir, columnL_wDir)

        self.columnModel = self.sec.create_model()

