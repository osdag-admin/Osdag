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
    def create_Flex3DModel(self):
        """

        """
        self.createcolumnFlexGeometry()

    def createcolumnGeometry(self):
        """
        Ensures the column is always vertical along the z-axis.

        :return: Geometric orientation of this component
        """
        # The origin of the column
        columnOriginL = numpy.array([0.0, 0.0, 0.0])

        # Set the column's local u-direction and w-direction

        uDir = numpy.array([1.0, 0.0, 0.0])  # Along x-axis
        wDir = numpy.array([0.0, 0.0, 1.0])  # Along z-axis (vertical)

        # Place the section at the specified origin with the orientation defined
        self.sec.place(columnOriginL, uDir, wDir)

        # Create the column model based on the section and orientation
        self.columnModel = self.sec.create_model()

    def createcolumnFlexGeometry(self):
        """
        Ensures the column is always horizontal along the x-axis.

        :return: Geometric orientation of this component
        """
        # The origin of the column
        columnOriginL = numpy.array([0.0, 0.0, 0.0])

        # Set the column's local u-direction and w-direction

        uDir = numpy.array([1.0, 0.0, 0.0])  # Along x-axis
        wDir = numpy.array([0.0, 1.0, 0.0])  # Along y-axis (horizontal)

        # Place the section at the specified origin with the new orientation
        self.sec.place(columnOriginL, uDir, wDir)

        # Create the column model based on the section and orientation
        self.columnModel = self.sec.create_model()
