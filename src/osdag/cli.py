from osdag.design_type.connection.fin_plate_connection import FinPlateConnection
from osdag.design_type.connection.cleat_angle_connection import CleatAngleConnection
from osdag.design_type.connection.seated_angle_connection import SeatedAngleConnection
from osdag.design_type.connection.end_plate_connection import EndPlateConnection
from osdag.design_type.connection.base_plate_connection import BasePlateConnection
from osdag.design_type.connection.beam_cover_plate import BeamCoverPlate
from osdag.design_type.connection.beam_cover_plate_weld import BeamCoverPlateWeld
from osdag.design_type.connection.column_cover_plate_weld import ColumnCoverPlateWeld
from osdag.design_type.tension_member.tension_bolted import Tension_bolted
from osdag.design_type.tension_member.tension_welded import Tension_welded
from osdag.design_type.connection.beam_beam_end_plate_splice import BeamBeamEndPlateSplice
from osdag.design_type.connection.beam_column_end_plate import BeamColumnEndPlate
from osdag.design_type.connection.column_cover_plate import ColumnCoverPlate
from osdag.design_type.connection.column_end_plate import ColumnEndPlate
from osdag.design_type.compression_member.compression import Compression
from osdag.design_type.main import Main
from osdag.Common import TYPE_TEXTBOX, TYPE_OUT_BUTTON
from osdag.Common import (
    # Shear Connection
    KEY_DISP_FINPLATE,
    KEY_DISP_ENDPLATE,
    KEY_DISP_CLEATANGLE,
    KEY_DISP_SEATED_ANGLE,

    # Base Plate Connection
    KEY_DISP_BASE_PLATE,

    # Moment Connection
    KEY_DISP_BEAMCOVERPLATE,
    KEY_DISP_COLUMNCOVERPLATE,
    KEY_DISP_BEAMCOVERPLATEWELD,
    KEY_DISP_COLUMNCOVERPLATEWELD,
    KEY_DISP_BB_EP_SPLICE,
    KEY_DISP_COLUMNENDPLATE,
    KEY_DISP_BCENDPLATE,

    # Tension Member
    KEY_DISP_TENSION_BOLTED,
    KEY_DISP_TENSION_WELDED,

    # Compression Member
    KEY_DISP_COMPRESSION

)


available_modules = {
    KEY_DISP_BASE_PLATE:BasePlateConnection, 
    KEY_DISP_BEAMCOVERPLATE:BeamCoverPlate, 
    KEY_DISP_CLEATANGLE:CleatAngleConnection,
    KEY_DISP_COLUMNCOVERPLATE:ColumnCoverPlate, 
    KEY_DISP_COLUMNENDPLATE:ColumnEndPlate, 
    KEY_DISP_ENDPLATE:EndPlateConnection,
    KEY_DISP_FINPLATE:FinPlateConnection, 
    KEY_DISP_SEATED_ANGLE:SeatedAngleConnection, 
    KEY_DISP_TENSION_BOLTED:Tension_bolted,
    KEY_DISP_TENSION_WELDED:Tension_welded, 
    KEY_DISP_COMPRESSION:Compression, 
    KEY_DISP_BEAMCOVERPLATEWELD:BeamCoverPlateWeld,
    KEY_DISP_COLUMNCOVERPLATEWELD:ColumnCoverPlateWeld, 
    KEY_DISP_BB_EP_SPLICE:BeamBeamEndPlateSplice,
    KEY_DISP_BCENDPLATE:BeamColumnEndPlate,
}
