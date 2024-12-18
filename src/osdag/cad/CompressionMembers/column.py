import numpy
import copy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from ..items.ISection import *


class CompressionMemberCAD(object):
    def __init__(self, sec):
        self.sec = sec

    def create_3DModel(self):
        """

        """
        self.createcolumnGeometry()

    def createcolumnGeometry(self):
        """
        Ensures the column is always vertical along the z-axis.

        :return: Geometric orientation of this component
        """
        # The origin of the column
        columnOriginL = numpy.array([0.0, 0.0, 0.0])

        # Set the column's local u-direction and w-direction
        # Since the column is vertical along z-axis, its w-direction is along z-axis
        # The u-direction must be perpendicular to w-direction, choose x-axis
        uDir = numpy.array([1.0, 0.0, 0.0])  # Along x-axis
        wDir = numpy.array([0.0, 0.0, 1.0])  # Along z-axis (vertical)

        # Place the section at the specified origin with the orientation defined
        self.sec.place(columnOriginL, uDir, wDir)

        # Create the column model based on the section and orientation
        self.columnModel = self.sec.create_model()

        